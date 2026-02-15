"""
Module 5: AI Engine

This module handles AI image generation using Stable Diffusion API.

Dependencies: Module 1 (Configuration)
"""
import requests
import uuid
import base64
import logging
from typing import List, Dict, Optional
from io import BytesIO

from app.config import get_settings, Settings

logger = logging.getLogger(__name__)


class AIEngineError(Exception):
    """Raised when AI generation fails."""
    pass


class AIEngine:
    """
    AI Engine for generating interior design variations.
    
    Integrates with Stability AI (Stable Diffusion) API to generate
    design variations from room images.
    """
    
    # Style prompts for Stable Diffusion
    STYLE_PROMPTS = {
        "modern": "Modern interior design, clean lines, neutral colors, minimalist furniture, professional photography, high quality, 4k",
        "traditional": "Traditional Indian interior design, rich colors, ethnic patterns, wooden furniture, warm lighting, professional photography, high quality, 4k",
        "minimalist": "Minimalist interior design, white and beige tones, simple furniture, uncluttered space, natural light, professional photography, high quality, 4k",
        "luxury": "Luxurious interior design, premium materials, elegant furniture, sophisticated decor, ambient lighting, professional photography, high quality, 4k",
        "bohemian": "Bohemian interior design, eclectic decor, vibrant colors, mix of patterns, cozy atmosphere, plants, professional photography, high quality, 4k",
        "industrial": "Industrial interior design, exposed brick, metal accents, rustic wood, Edison bulbs, urban style, professional photography, high quality, 4k",
        "scandinavian": "Scandinavian interior design, light wood, white walls, cozy textiles, functional furniture, hygge atmosphere, professional photography, high quality, 4k",
        "contemporary": "Contemporary interior design, sleek furniture, bold accents, geometric patterns, statement pieces, professional photography, high quality, 4k"
    }
    
    NEGATIVE_PROMPT = "blurry, low quality, distorted, deformed, bad anatomy, watermark, text, ugly, duplicate"
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize AI Engine with settings."""
        self.settings = settings or get_settings()
        self.api_key = self.settings.STABLE_DIFFUSION_API_KEY
        self.api_url = self.settings.STABLE_DIFFUSION_API_URL
        self.timeout = self.settings.STABLE_DIFFUSION_TIMEOUT
        
        if not self.api_key:
            logger.warning("STABLE_DIFFUSION_API_KEY not configured - AI generation will fail")
    
    def generate_design_variations(
        self,
        room_image_url: str,
        style: str,
        room_type: str
    ) -> List[str]:
        """
        Generate 3 design variations using Stable Diffusion.
        
        Args:
            room_image_url: URL of the room image to base designs on
            style: Design style (modern, traditional, etc.)
            room_type: Type of room (bedroom, living, etc.)
            
        Returns:
            List[str]: URLs of generated images
            
        Raises:
            AIEngineError: If generation fails
        """
        if not self.api_key:
            # Return mock URLs for development
            return self._generate_mock_urls(style)
        
        prompt = self._build_prompt(style, room_type)
        variations = [
            f"{prompt}, angle 1",
            f"{prompt}, different perspective, angle 2",
            f"{prompt}, alternate layout, angle 3"
        ]
        
        generated_urls = []
        
        for i, var_prompt in enumerate(variations):
            try:
                url = self._call_stable_diffusion(var_prompt, i)
                if url:
                    generated_urls.append(url)
            except Exception as e:
                logger.error(f"Failed to generate variation {i+1}: {e}")
                # Continue with next variation
        
        if not generated_urls:
            raise AIEngineError("Failed to generate any design variations")
        
        return generated_urls
    
    def _build_prompt(self, style: str, room_type: str) -> str:
        """Build the prompt for Stable Diffusion."""
        base_prompt = self.STYLE_PROMPTS.get(style.lower(), self.STYLE_PROMPTS["modern"])
        return f"{base_prompt.replace('interior design', f'{room_type} interior design')}"
    
    def _call_stable_diffusion(self, prompt: str, variation: int) -> Optional[str]:
        """Call Stability AI API to generate image."""
        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": prompt,
                    "negative_prompt": self.NEGATIVE_PROMPT,
                    "width": 1024,
                    "height": 1024,
                    "samples": 1,
                    "cfg_scale": 7,
                    "steps": 30
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                # Process and return URL from response
                # This is simplified - real implementation would upload to S3
                return f"https://mock-url.com/design_{variation}.png"
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def _generate_mock_urls(self, style: str) -> List[str]:
        """Generate mock URLs for development."""
        return [
            f"https://placehold.co/1024x1024/png?text={style.title()}+Design+1",
            f"https://placehold.co/1024x1024/png?text={style.title()}+Design+2",
            f"https://placehold.co/1024x1024/png?text={style.title()}+Design+3"
        ]


# Global instance
_ai_engine: Optional[AIEngine] = None


def get_ai_engine() -> AIEngine:
    """Get or create global AI engine instance."""
    global _ai_engine
    if _ai_engine is None:
        _ai_engine = AIEngine()
    return _ai_engine


__all__ = ["AIEngine", "AIEngineError", "get_ai_engine"]


"""
Module 6: Vastu Engine

This module handles Vastu Shastra analysis for room direction combinations.

Dependencies: Module 1 (Configuration)
"""
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class VastuEngineError(Exception):
    """Raised when Vastu analysis fails."""
    pass


class InvalidDirectionError(VastuEngineError):
    """Raised when direction is invalid."""
    pass


class VastuEngine:
    """
    Vastu Engine for analyzing room direction compliance.
    
    Implements Vastu Shastra rules for determining the compatibility
    between room types and cardinal directions.
    """
    
    # Vastu rules for each direction
    VASTU_RULES = {
        "north": {
            "element": "Water",
            "ruling_planet": "Mercury",
            "suitable_rooms": ["living", "study", "office", "entrance"],
            "colors": ["green", "blue", "white"],
            "dos": [
                "Keep the north direction open and clutter-free",
                "Use light colors like green, blue, or white",
                "Place water elements like fountain or aquarium",
                "Keep windows open for natural light"
            ],
            "donts": [
                "Avoid heavy furniture in the north",
                "No red or pink colors in this direction",
                "Avoid kitchen or toilet in the north",
                "Don't block the north with tall structures"
            ]
        },
        "south": {
            "element": "Fire",
            "ruling_planet": "Mars",
            "suitable_rooms": ["kitchen", "bedroom", "storeroom"],
            "colors": ["red", "pink", "orange", "brown"],
            "dos": [
                "Keep heavy furniture in the south",
                "Use warm colors like red, pink, orange",
                "Place kitchen in southeast (Agni corner)",
                "Master bedroom can be in southwest"
            ],
            "donts": [
                "Avoid water elements in the south",
                "No underground water tank in south",
                "Don't keep the south direction completely open",
                "Avoid large windows in the south"
            ]
        },
        "east": {
            "element": "Air",
            "ruling_planet": "Sun",
            "suitable_rooms": ["living", "dining", "study", "entrance"],
            "colors": ["white", "light yellow", "green"],
            "dos": [
                "Keep the east direction open for morning sunlight",
                "Place entrance or large windows in the east",
                "Use light and bright colors",
                "Ideal for meditation and prayer room"
            ],
            "donts": [
                "Avoid heavy structures blocking the east",
                "No toilets or garbage in the east",
                "Don't use dark colors in this direction",
                "Avoid clutter in the east"
            ]
        },
        "west": {
            "element": "Space",
            "ruling_planet": "Saturn",
            "suitable_rooms": ["dining", "study", "children_bedroom", "office"],
            "colors": ["blue", "white", "grey"],
            "dos": [
                "Keep the west moderately heavy",
                "Use cool colors like blue and grey",
                "Suitable for children's bedroom",
                "Can place overhead water tank"
            ],
            "donts": [
                "Avoid completely blocking the west",
                "No master bedroom in the northwest",
                "Don't place kitchen in the west",
                "Avoid red colors in this direction"
            ]
        },
        "northeast": {
            "element": "Water",
            "ruling_planet": "Jupiter",
            "suitable_rooms": ["prayer", "study", "living"],
            "colors": ["white", "cream", "light yellow"],
            "dos": [
                "Keep this direction most open and light",
                "Ideal for prayer or meditation room",
                "Place underground water tank here",
                "Use very light and pure colors"
            ],
            "donts": [
                "Never place toilet in northeast",
                "Avoid heavy furniture completely",
                "No staircase in the northeast",
                "Don't place kitchen here"
            ]
        },
        "northwest": {
            "element": "Air",
            "ruling_planet": "Moon",
            "suitable_rooms": ["guest_room", "toilet", "pantry"],
            "colors": ["white", "light grey", "cream"],
            "dos": [
                "Keep this direction light to moderate",
                "Can place guest room here",
                "Suitable for storage of light items",
                "Keep windows for air circulation"
            ],
            "donts": [
                "Avoid master bedroom here",
                "No heavy storage in northwest",
                "Don't block air flow completely",
                "Avoid dark colors"
            ]
        },
        "southeast": {
            "element": "Fire",
            "ruling_planet": "Venus",
            "suitable_rooms": ["kitchen", "electrical_room"],
            "colors": ["red", "orange", "pink", "brown"],
            "dos": [
                "Ideal location for kitchen (Agni corner)",
                "Place electrical equipment here",
                "Use warm and energetic colors",
                "Keep this area well-lit"
            ],
            "donts": [
                "No bedroom in southeast",
                "Avoid water elements here",
                "Don't place mirrors in southeast",
                "No study room here"
            ]
        },
        "southwest": {
            "element": "Earth",
            "ruling_planet": "Rahu",
            "suitable_rooms": ["master_bedroom", "wardrobe", "heavy_storage"],
            "colors": ["brown", "earth tones", "cream", "light yellow"],
            "dos": [
                "Keep this direction heaviest in the house",
                "Ideal for master bedroom",
                "Place heavy furniture and wardrobes here",
                "Use earthy and grounding colors"
            ],
            "donts": [
                "Never place underground water tank here",
                "Avoid kitchen in southwest",
                "No open space or balcony preferred",
                "Don't use water colors like blue"
            ]
        }
    }
    
    # Room type to direction compatibility scores
    ROOM_VASTU_SCORES = {
        "bedroom": {
            "southwest": 100, "south": 85, "west": 70, "northwest": 60,
            "east": 50, "north": 40, "southeast": 30, "northeast": 20
        },
        "living": {
            "northeast": 100, "north": 95, "east": 90, "west": 75,
            "southeast": 60, "south": 50, "northwest": 70, "southwest": 30
        },
        "kitchen": {
            "southeast": 100, "south": 80, "east": 70, "west": 60,
            "northwest": 50, "north": 30, "northeast": 20, "southwest": 10
        },
        "dining": {
            "west": 100, "east": 90, "north": 80, "south": 70,
            "northwest": 75, "southeast": 60, "northeast": 50, "southwest": 40
        },
        "study": {
            "east": 100, "north": 95, "northeast": 90, "west": 80,
            "northwest": 75, "south": 60, "southeast": 50, "southwest": 40
        },
        "bathroom": {
            "northwest": 100, "west": 90, "south": 70, "southwest": 60,
            "southeast": 50, "east": 40, "north": 30, "northeast": 10
        }
    }
    
    def analyze(self, direction: str, room_type: str) -> Dict:
        """
        Analyze Vastu compliance for a direction and room type combination.
        
        Args:
            direction: Vastu direction (north, south, east, west, etc.)
            room_type: Type of room (bedroom, living, kitchen, etc.)
            
        Returns:
            Dict: Analysis results including score, suggestions, warnings
            
        Raises:
            InvalidDirectionError: If direction is not valid
        """
        direction = direction.lower().strip()
        room_type = room_type.lower().strip().replace(" ", "_")
        
        if direction not in self.VASTU_RULES:
            raise InvalidDirectionError(f"Invalid direction: {direction}")
        
        # Get base score
        room_scores = self.ROOM_VASTU_SCORES.get(room_type, self.ROOM_VASTU_SCORES["living"])
        vastu_score = room_scores.get(direction, 50)
        
        direction_rules = self.VASTU_RULES[direction]
        
        # Generate suggestions and warnings
        suggestions = []
        warnings = []
        
        # Check if room type is suitable for this direction
        suitable_rooms = direction_rules["suitable_rooms"]
        if room_type in suitable_rooms:
            suggestions.append(f"✓ {room_type.replace('_', ' ').title()} is well-suited for the {direction} direction")
        else:
            warnings.append(f"⚠ {room_type.replace('_', ' ').title()} is not ideal in the {direction} direction")
            suggestions.append(f"Consider {', '.join(suitable_rooms[:3])} for the {direction} direction instead")
        
        # Add direction-specific suggestions
        suggestions.extend(direction_rules["dos"][:2])
        
        # Add warnings based on score
        if vastu_score < 50:
            warnings.extend(direction_rules["donts"][:2])
            warnings.append("Consider consulting a Vastu expert for remedies")
        elif vastu_score < 70:
            warnings.append(direction_rules["donts"][0])
        
        # Add color recommendations
        suggestions.append(f"Recommended colors: {', '.join(direction_rules['colors'][:3])}")
        
        # Determine rating
        if vastu_score >= 80:
            direction_rating = "excellent"
        elif vastu_score >= 60:
            direction_rating = "good"
        elif vastu_score >= 40:
            direction_rating = "neutral"
        else:
            direction_rating = "poor"
        
        return {
            "vastu_score": vastu_score,
            "suggestions": suggestions,
            "warnings": warnings,
            "direction_rating": direction_rating,
            "element_balance": {
                "dominant_element": direction_rules["element"],
                "ruling_planet": direction_rules["ruling_planet"],
                "balance_status": "balanced" if vastu_score >= 60 else "needs_attention"
            }
        }
    
    def get_remedies(self, direction: str, room_type: str) -> List[str]:
        """Get Vastu remedies for non-compliant placements."""
        remedies = []
        
        direction = direction.lower()
        room_type = room_type.lower()
        
        # Direction-specific remedies
        if direction == "northeast" and room_type in ["kitchen", "toilet"]:
            remedies.extend([
                "Place a Vastu pyramid in the northeast corner",
                "Keep the area extremely clean and clutter-free",
                "Use light yellow or cream colors",
                "Place a bowl of sea salt to absorb negative energy"
            ])
        
        if direction == "southwest" and room_type in ["kitchen", "entrance"]:
            remedies.extend([
                "Place heavy furniture or wardrobe in the southwest",
                "Use earthy colors like brown or beige",
                "Keep a Vastu yantra in the room",
                "Avoid water features in this area"
            ])
        
        if direction == "southeast" and room_type in ["bedroom", "study"]:
            remedies.extend([
                "Place green plants to balance fire energy",
                "Use cool colors like blue or white",
                "Keep the room well-ventilated",
                "Place a copper pyramid in the southeast"
            ])
        
        # General remedies
        if not remedies:
            remedies = [
                "Place a Vastu pyramid in the center of the room",
                "Keep the room clean and well-lit",
                "Use colors as per the direction element",
                "Ensure proper ventilation and natural light"
            ]
        
        return remedies


# Global instance
_vastu_engine: Optional[VastuEngine] = None


def get_vastu_engine() -> VastuEngine:
    """Get or create global Vastu engine instance."""
    global _vastu_engine
    if _vastu_engine is None:
        _vastu_engine = VastuEngine()
    return _vastu_engine


__all__ = ["VastuEngine", "VastuEngineError", "InvalidDirectionError", "get_vastu_engine"]
