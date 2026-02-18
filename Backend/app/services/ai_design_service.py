"""
AI Design Service using New AI Engine

This service integrates the new AI engine architecture with the design generation
workflow, providing layout-preserving interior transformations.

Features:
- Integration with AI engine strategy pattern
- Rate limiting and quota management
- Image preprocessing and validation
- Design generation with layout preservation
- Error handling and fallback strategies
"""

import asyncio
import uuid
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from app.services.ai_engine import (
    EngineFactory, 
    GenerationRequest, 
    GenerationResult,
    check_generation_rate_limit,
    RateLimitError
)
from app.services.firebase_client import get_firestore
from app.services.room_service import room_upload_service
from app.services.storage import get_storage_service

logger = logging.getLogger(__name__)


class AIDesignService:
    """
    AI Design Service using the new AI engine architecture.
    
    Handles the complete design generation workflow with rate limiting,
    image preprocessing, and layout preservation.
    """
    
    def __init__(self):
        """Initialize the AI design service."""
        self.engine = None
        self.storage_service = get_storage_service()
        self.firestore = get_firestore()
        
        # Performance tracking
        self.generation_count = 0
        self.success_count = 0
        self.error_count = 0
    
    async def _get_engine(self):
        """Get or initialize the AI engine."""
        if self.engine is None:
            self.engine = EngineFactory.get_engine_from_env()
            
            # Health check - don't fail if token is missing
            try:
                if not await self.engine.health_check():
                    logger.warning("AI engine health check failed - API token may be missing")
            except Exception as e:
                logger.warning(f"AI engine health check error: {e}")
        
        return self.engine
    
    async def _validate_room_images(self, room_id: str, user_id: str) -> Dict[str, bytes]:
        """
        Validate and retrieve room images.
        
        Args:
            room_id: Room identifier
            user_id: User identifier
            
        Returns:
            Dictionary of direction -> image bytes
        """
        # Get room data
        room = await room_upload_service.get_room(room_id, user_id)
        if not room:
            raise ValueError(f"Room {room_id} not found")
        
        # Get images
        room_images = room.get('images', {})
        if not room_images:
            raise ValueError("Room has no images")
        
        # Download images from storage
        image_bytes = {}
        for direction, image_url in room_images.items():
            if direction in ['north', 'south', 'east', 'west']:
                try:
                    # Extract filename from URL
                    if '/uploads/' in image_url:
                        filename = image_url.split('/uploads/')[-1]
                        image_bytes[direction] = await self._download_image_from_storage(filename)
                    else:
                        # Handle external URLs if needed
                        image_bytes[direction] = await self._download_image_from_url(image_url)
                except Exception as e:
                    logger.error(f"Failed to download {direction} image: {e}")
                    # Continue with other images
        
        if not image_bytes:
            raise ValueError("No valid room images found")
        
        return image_bytes
    
    async def _download_image_from_storage(self, filename: str) -> bytes:
        """
        Download image from local storage.
        
        Args:
            filename: Image filename
            
        Returns:
            Image bytes
        """
        try:
            # For local storage, read from filesystem
            import os
            file_path = os.path.join("uploads", filename)
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    return f.read()
            else:
                raise FileNotFoundError(f"Image file not found: {file_path}")
                
        except Exception as e:
            logger.error(f"Failed to download image from storage: {e}")
            raise
    
    async def _download_image_from_url(self, url: str) -> bytes:
        """
        Download image from URL.
        
        Args:
            url: Image URL
            
        Returns:
            Image bytes
        """
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        raise Exception(f"Failed to download image: {response.status}")
                        
        except Exception as e:
            logger.error(f"Failed to download image from URL: {e}")
            raise
    
    async def _load_user_usage(self, user_id: str, date: str) -> Optional[Dict[str, Any]]:
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
                return usage_doc
            
            return None
            
        except Exception as e:
            logger.warning(f"Failed to load user usage (Firebase may not be configured): {e}")
            return None
    
    async def generate_design(
        self,
        user_id: str,
        user_data: Dict[str, Any],
        room_id: str,
        room_type: str,
        furniture_style: str,
        wall_color: str,
        flooring_material: str,
        controlnet_weight: float = 1.0,
        image_strength: float = 0.4,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.0,
        resolution: Optional[tuple[int, int]] = None
    ) -> Dict[str, Any]:
        """
        Generate AI interior design with layout preservation.
        
        Args:
            user_id: User identifier
            user_data: User information for rate limiting
            room_id: Room identifier
            room_type: Type of room
            furniture_style: Furniture style preference
            wall_color: Wall color preference
            flooring_material: Flooring material preference
            controlnet_weight: ControlNet conditioning weight
            image_strength: Image transformation strength
            num_inference_steps: Number of inference steps
            guidance_scale: Guidance scale for generation
            resolution: Output resolution
            
        Returns:
            Generation result with design information
        """
        start_time = datetime.now()
        
        try:
            # Check rate limit
            allowed, error_message = await check_generation_rate_limit(user_id, user_data)
            if not allowed:
                raise RateLimitError(error_message)
            
            # Get AI engine
            engine = await self._get_engine()
            
            # Validate room images
            room_images = await self._validate_room_images(room_id, user_id)
            
            # Use north as primary image
            primary_image = room_images.get('north')
            if not primary_image:
                raise ValueError("North direction image is required")
            
            # Set default resolution
            if resolution is None:
                from app.config import get_settings
                settings = get_settings()
                resolution = settings.max_resolution_tuple
            
            # Prepare generation request
            request = GenerationRequest(
                primary_image=primary_image,
                room_images=room_images,
                room_type=room_type,
                furniture_style=furniture_style,
                wall_color=wall_color,
                flooring_material=flooring_material,
                controlnet_weight=controlnet_weight,
                image_strength=image_strength,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                resolution=resolution
            )
            
            # Generate images
            result = await engine.generate_img2img(request)
            
            # Update statistics
            self.generation_count += 1
            if result.success:
                self.success_count += 1
            else:
                self.error_count += 1
            
            if not result.success:
                raise Exception(f"AI generation failed: {result.error_message}")
            
            # Save design to Firestore
            design_id = str(uuid.uuid4())
            
            design_data = {
                'design_id': design_id,
                'room_id': room_id,
                'user_id': user_id,
                'room_type': room_type,
                'customization': {
                    'furniture_style': furniture_style,
                    'wall_color': wall_color,
                    'flooring_material': flooring_material
                },
                'generation_params': {
                    'controlnet_weight': controlnet_weight,
                    'image_strength': image_strength,
                    'num_inference_steps': num_inference_steps,
                    'guidance_scale': guidance_scale,
                    'resolution': resolution
                },
                'prompt_used': result.generation_params.get('prompt', '') if result.generation_params else '',
                'generated_images': result.generated_images,
                'seeds': result.seeds_used or [],
                'engine_used': result.engine_used,
                'model_version': result.model_version,
                'inference_time_seconds': result.inference_time_seconds,
                'created_at': start_time.isoformat(),
                'updated_at': datetime.now().isoformat(),
                'status': 'completed'
            }
            
            await self.firestore.create_design(
                design_id=design_id,
                room_id=room_id,
                user_id=user_id,
                style=furniture_style,
                customization=design_data['customization'],
                prompt_used=design_data['prompt_used'],
                generated_images=result.generated_images,
                version=1
            )
            
            logger.info(f"Design generated successfully: {design_id} for room {room_id}")
            
            return {
                'design_id': design_id,
                'status': 'completed',
                'message': 'Design generated successfully',
                'generated_images': result.generated_images,
                'generation_time_seconds': result.inference_time_seconds,
                'engine_used': result.engine_used,
                'model_version': result.model_version
            }
            
        except RateLimitError as e:
            logger.warning(f"Rate limit exceeded for user {user_id}: {e}")
            return {
                'status': 'rate_limited',
                'error_code': e.error_code,
                'message': e.message
            }
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Design generation failed: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'message': 'Design generation failed'
            }
    
    async def regenerate_design(
        self,
        user_id: str,
        user_data: Dict[str, Any],
        design_id: str,
        updates: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Regenerate a design with updated parameters.
        
        Args:
            user_id: User identifier
            user_data: User information for rate limiting
            design_id: Existing design identifier
            updates: Parameter updates
            
        Returns:
            Generation result
        """
        try:
            # Get original design
            original_design = await self.firestore.get_design(design_id, user_id)
            if not original_design:
                raise ValueError(f"Design {design_id} not found")
            
            # Extract parameters
            room_id = original_design['room_id']
            customization = original_design.get('customization', {})
            
            # Apply updates
            if updates:
                customization.update(updates)
            
            # Generate new design
            result = await self.generate_design(
                user_id=user_id,
                user_data=user_data,
                room_id=room_id,
                room_type=original_design.get('room_type', 'living'),
                furniture_style=customization.get('furniture_style', 'modern'),
                wall_color=customization.get('wall_color', 'white'),
                flooring_material=customization.get('flooring_material', 'hardwood')
            )
            
            # Link to original design
            if result.get('design_id'):
                await self.firestore.link_design_versions(
                    original_design_id=design_id,
                    new_design_id=result['design_id']
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Design regeneration failed: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'message': 'Design regeneration failed'
            }
    
    async def get_design_statistics(self) -> Dict[str, Any]:
        """
        Get design generation statistics.
        
        Returns:
            Statistics dictionary
        """
        try:
            engine = await self._get_engine()
            engine_info = engine.get_model_info()
            
            return {
                'total_generations': self.generation_count,
                'successful_generations': self.success_count,
                'failed_generations': self.error_count,
                'success_rate': self.success_count / max(1, self.generation_count),
                'engine_info': engine_info
            }
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {
                'total_generations': self.generation_count,
                'successful_generations': self.success_count,
                'failed_generations': self.error_count,
                'success_rate': self.success_count / max(1, self.generation_count),
                'engine_info': None
            }


# Global service instance
_ai_design_service: Optional[AIDesignService] = None


async def get_ai_design_service() -> AIDesignService:
    """
    Get or create global AI design service instance.
    
    Returns:
        AI design service instance
    """
    global _ai_design_service
    
    if _ai_design_service is None:
        _ai_design_service = AIDesignService()
    
    return _ai_design_service
