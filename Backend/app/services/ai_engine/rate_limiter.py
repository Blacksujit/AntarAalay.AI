"""
Rate Limiting Module for AI Generation

This module implements per-user generation quotas and global throttling
to control costs and prevent abuse of the AI generation system.

Features:
- Per-user daily generation quotas
- Global API throttling
- Usage tracking in Firestore
- Configurable limits for different user types
- Automatic quota reset at midnight
- Rate limit exceeded responses
"""

import asyncio
import time
from datetime import datetime, timezone
from typing import Dict, Optional, Any
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class UserType(Enum):
    """User types for different quota levels."""
    FREE = "free"
    AUTHENTICATED = "authenticated"
    PREMIUM = "premium"
    ADMIN = "admin"


@dataclass
class RateLimitConfig:
    """Rate limit configuration."""
    free_daily_limit: int = 3
    authenticated_daily_limit: int = 5
    premium_daily_limit: int = 20
    admin_daily_limit: int = 100
    global_requests_per_minute: int = 60
    global_requests_per_hour: int = 500
    block_duration_minutes: int = 60


@dataclass
class UsageRecord:
    """User usage record."""
    user_id: str
    date: str  # YYYY-MM-DD format
    count: int
    last_reset: datetime
    blocked_until: Optional[datetime] = None


class RateLimiter:
    """
    Rate limiter for AI generation requests.
    
    Implements per-user quotas and global throttling.
    """
    
    def __init__(self, config: RateLimitConfig):
        """
        Initialize rate limiter.
        
        Args:
            config: Rate limit configuration
        """
        self.config = config
        
        # In-memory tracking for performance
        self.user_usage: Dict[str, UsageRecord] = {}
        self.global_requests = []
        
        # Cleanup task
        self.cleanup_task = None
        
        # Lock for thread safety
        self.lock = asyncio.Lock()
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Initialized RateLimiter")
    
    async def start_cleanup_task(self):
        """Start background cleanup task."""
        if self.cleanup_task is None:
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())
            self.logger.info("Started rate limiter cleanup task")
    
    async def stop_cleanup_task(self):
        """Stop background cleanup task."""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
            self.cleanup_task = None
            self.logger.info("Stopped rate limiter cleanup task")
    
    async def _cleanup_loop(self):
        """Background cleanup loop."""
        while True:
            try:
                await asyncio.sleep(300)  # Run every 5 minutes
                await self._cleanup_expired_records()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Cleanup loop error: {e}")
    
    async def _cleanup_expired_records(self):
        """Clean up expired usage records."""
        async with self.lock:
            current_time = datetime.now(timezone.utc)
            
            # Clean up user usage records
            expired_users = []
            for user_id, record in self.user_usage.items():
                if (current_time - record.last_reset).days > 7:
                    expired_users.append(user_id)
            
            for user_id in expired_users:
                del self.user_usage[user_id]
            
            # Clean up global request tracking
            cutoff_time = current_time.timestamp() - 3600  # Keep last hour
            self.global_requests = [
                req_time for req_time in self.global_requests
                if req_time > cutoff_time
            ]
            
            if expired_users:
                self.logger.info(f"Cleaned up {len(expired_users)} expired user records")
    
    def _get_user_type(self, user_data: Dict[str, Any]) -> UserType:
        """
        Determine user type from user data.
        
        Args:
            user_data: User information
            
        Returns:
            User type
        """
        # Check for premium status
        if user_data.get('is_premium') or user_data.get('subscription') == 'premium':
            return UserType.PREMIUM
        
        # Check for admin status
        if user_data.get('is_admin') or user_data.get('role') == 'admin':
            return UserType.ADMIN
        
        # Check if authenticated (has email verified)
        if user_data.get('email_verified') or user_data.get('uid'):
            return UserType.AUTHENTICATED
        
        # Default to free user
        return UserType.FREE
    
    def _get_daily_limit(self, user_type: UserType) -> int:
        """
        Get daily generation limit for user type.
        
        Args:
            user_type: User type
            
        Returns:
            Daily limit
        """
        limits = {
            UserType.FREE: self.config.free_daily_limit,
            UserType.AUTHENTICATED: self.config.authenticated_daily_limit,
            UserType.PREMIUM: self.config.premium_daily_limit,
            UserType.ADMIN: self.config.admin_daily_limit
        }
        return limits.get(user_type, self.config.free_daily_limit)
    
    def _get_current_date(self) -> str:
        """Get current date in YYYY-MM-DD format."""
        return datetime.now(timezone.utc).strftime('%Y-%m-%d')
    
    async def _load_user_usage(self, user_id: str, date: str) -> Optional[UsageRecord]:
        """
        Load user usage from Firestore.
        
        Args:
            user_id: User identifier
            date: Date string
            
        Returns:
            Usage record or None
        """
        try:
            from app.services.firebase_client import get_firestore
            firestore = get_firestore()
            
            # Get usage document
            usage_doc = await firestore.get_user_usage(user_id, date)
            
            if usage_doc:
                return UsageRecord(
                    user_id=user_id,
                    date=date,
                    count=usage_doc.get('count', 0),
                    last_reset=datetime.fromisoformat(usage_doc.get('last_reset', datetime.now(timezone.utc).isoformat())),
                    blocked_until=datetime.fromisoformat(usage_doc['blocked_until']) if usage_doc.get('blocked_until') else None
                )
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Failed to load user usage (Firebase may not be configured): {e}")
            return None
    
    async def _save_user_usage(self, record: UsageRecord):
        """
        Save user usage to Firestore.
        
        Args:
            record: Usage record to save
        """
        try:
            from app.services.firebase_client import get_firestore
            firestore = get_firestore()
            
            usage_data = {
                'count': record.count,
                'last_reset': record.last_reset.isoformat(),
                'date': record.date
            }
            
            if record.blocked_until:
                usage_data['blocked_until'] = record.blocked_until.isoformat()
            
            await firestore.save_user_usage(record.user_id, record.date, usage_data)
            
        except Exception as e:
            self.logger.warning(f"Failed to save user usage (Firebase may not be configured): {e}")
    
    async def check_rate_limit(self, user_id: str, user_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Check if user is allowed to make a generation request.
        
        Args:
            user_id: User identifier
            user_data: User information
            
        Returns:
            Tuple of (allowed, error_message)
        """
        async with self.lock:
            current_time = datetime.now(timezone.utc)
            current_date = self._get_current_date()
            
            # Get user type and daily limit
            user_type = self._get_user_type(user_data)
            daily_limit = self._get_daily_limit(user_type)
            
            # Load or create usage record
            cache_key = f"{user_id}_{current_date}"
            if cache_key not in self.user_usage:
                # Try to load from Firestore
                record = await self._load_user_usage(user_id, current_date)
                if record is None:
                    # Create new record
                    record = UsageRecord(
                        user_id=user_id,
                        date=current_date,
                        count=0,
                        last_reset=current_time
                    )
                self.user_usage[cache_key] = record
            
            record = self.user_usage[cache_key]
            
            # Check if user is blocked
            if record.blocked_until and current_time < record.blocked_until:
                remaining_minutes = int((record.blocked_until - current_time).total_seconds() / 60)
                return False, f"Rate limit exceeded. Try again in {remaining_minutes} minutes."
            
            # Reset count if it's a new day
            if record.date != current_date:
                record.date = current_date
                record.count = 0
                record.last_reset = current_time
                record.blocked_until = None
            
            # Check daily limit
            if record.count >= daily_limit:
                # Block user for configured duration
                record.blocked_until = current_time + timedelta(minutes=self.config.block_duration_minutes)
                await self._save_user_usage(record)
                
                return False, f"Daily generation limit of {daily_limit} reached. Try again tomorrow."
            
            # Check global rate limits
            if not await self._check_global_limits():
                return False, "Server is experiencing high demand. Please try again in a few moments."
            
            # Increment usage count
            record.count += 1
            
            # Save updated usage
            await self._save_user_usage(record)
            
            # Track global request
            self.global_requests.append(current_time.timestamp())
            
            self.logger.info(f"User {user_id} generation allowed: {record.count}/{daily_limit} used today")
            return True, None
    
    async def _check_global_limits(self) -> bool:
        """
        Check global rate limits.
        
        Returns:
            True if global limits allow new request
        """
        current_time = time.time()
        
        # Check requests per minute
        minute_cutoff = current_time - 60
        requests_per_minute = len([t for t in self.global_requests if t > minute_cutoff])
        
        if requests_per_minute >= self.config.global_requests_per_minute:
            self.logger.warning(f"Global rate limit exceeded: {requests_per_minute}/minute")
            return False
        
        # Check requests per hour
        hour_cutoff = current_time - 3600
        requests_per_hour = len([t for t in self.global_requests if t > hour_cutoff])
        
        if requests_per_hour >= self.config.global_requests_per_hour:
            self.logger.warning(f"Global hourly limit exceeded: {requests_per_hour}/hour")
            return False
        
        return True
    
    async def get_user_usage(self, user_id: str) -> Dict[str, Any]:
        """
        Get current usage information for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Usage information
        """
        async with self.lock:
            current_date = self._get_current_date()
            cache_key = f"{user_id}_{current_date}"
            
            if cache_key not in self.user_usage:
                record = await self._load_user_usage(user_id, current_date)
                if record is None:
                    return {
                        'user_id': user_id,
                        'date': current_date,
                        'count': 0,
                        'limit': self.config.free_daily_limit,
                        'remaining': self.config.free_daily_limit,
                        'blocked': False
                    }
                self.user_usage[cache_key] = record
            
            record = self.user_usage[cache_key]
            
            # Determine user type and limit (simplified)
            user_type = UserType.FREE  # Would need user data to determine properly
            daily_limit = self._get_daily_limit(user_type)
            
            return {
                'user_id': user_id,
                'date': record.date,
                'count': record.count,
                'limit': daily_limit,
                'remaining': max(0, daily_limit - record.count),
                'blocked': record.blocked_until is not None and datetime.now(timezone.utc) < record.blocked_until,
                'blocked_until': record.blocked_until.isoformat() if record.blocked_until else None
            }
    
    async def reset_user_usage(self, user_id: str):
        """
        Reset usage for a specific user (admin function).
        
        Args:
            user_id: User identifier to reset
        """
        async with self.lock:
            current_date = self._get_current_date()
            cache_key = f"{user_id}_{current_date}"
            
            if cache_key in self.user_usage:
                record = self.user_usage[cache_key]
                record.count = 0
                record.blocked_until = None
                await self._save_user_usage(record)
                
                self.logger.info(f"Reset usage for user {user_id}")
    
    async def get_global_stats(self) -> Dict[str, Any]:
        """
        Get global rate limiting statistics.
        
        Returns:
            Global statistics
        """
        async with self.lock:
            current_time = time.time()
            
            # Calculate recent request rates
            minute_cutoff = current_time - 60
            hour_cutoff = current_time - 3600
            
            requests_per_minute = len([t for t in self.global_requests if t > minute_cutoff])
            requests_per_hour = len([t for t in self.global_requests if t > hour_cutoff])
            
            # Count active users today
            current_date = self._get_current_date()
            active_users = len([
                record for record in self.user_usage.values()
                if record.date == current_date and record.count > 0
            ])
            
            return {
                'requests_per_minute': requests_per_minute,
                'requests_per_hour': requests_per_hour,
                'limit_per_minute': self.config.global_requests_per_minute,
                'limit_per_hour': self.config.global_requests_per_hour,
                'active_users_today': active_users,
                'total_tracked_users': len(self.user_usage)
            }


# Global rate limiter instance
_rate_limiter: Optional[RateLimiter] = None


async def get_rate_limiter() -> RateLimiter:
    """
    Get or create global rate limiter instance.
    
    Returns:
        Rate limiter instance
    """
    global _rate_limiter
    
    if _rate_limiter is None:
        from app.config import get_settings
        settings = get_settings()
        
        config = RateLimitConfig(
            free_daily_limit=getattr(settings, 'FREE_DAILY_LIMIT', 3),
            authenticated_daily_limit=getattr(settings, 'AUTHENTICATED_DAILY_LIMIT', 5),
            premium_daily_limit=getattr(settings, 'PREMIUM_DAILY_LIMIT', 20),
            admin_daily_limit=getattr(settings, 'ADMIN_DAILY_LIMIT', 100),
            global_requests_per_minute=getattr(settings, 'GLOBAL_REQUESTS_PER_MINUTE', 60),
            global_requests_per_hour=getattr(settings, 'GLOBAL_REQUESTS_PER_HOUR', 500),
            block_duration_minutes=getattr(settings, 'BLOCK_DURATION_MINUTES', 60)
        )
        
        _rate_limiter = RateLimiter(config)
        await _rate_limiter.start_cleanup_task()
    
    return _rate_limiter


async def check_generation_rate_limit(user_id: str, user_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Check if user is allowed to make a generation request.
    
    Args:
        user_id: User identifier
        user_data: User information
        
    Returns:
        Tuple of (allowed, error_message)
    """
    rate_limiter = await get_rate_limiter()
    return await rate_limiter.check_rate_limit(user_id, user_data)


class RateLimitError(Exception):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(self, message: str, error_code: str = "RATE_LIMIT_EXCEEDED"):
        self.message = message
        self.error_code = error_code
        super().__init__(message)
