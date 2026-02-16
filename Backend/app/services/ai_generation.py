"""
AI Generation Engine for AntarAalay.ai

Generates interior designs using Stable Diffusion with ControlNet
for layout preservation from 4-directional room images.
"""
import uuid
from datetime import datetime
from typing import List, Dict, Optional
import aiohttp
import asyncio

from app.config import get_settings

# Stable Diffusion / ControlNet configuration
SD_API_URL = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
CONTROLNET_ENABLED = True

# Style templates
STYLE_TEMPLATES = {
    "modern": "modern minimalist interior design, clean lines, contemporary furniture",
    "traditional": "traditional Indian interior design, ethnic decor, warm lighting",
    "contemporary": "contemporary interior design, sleek furniture, neutral colors",
    "minimalist": "minimalist interior design, clutter-free, simple elegance",
    "luxury": "luxury interior design, premium materials, elegant decor",
}

# Vastu-compliant direction-based suggestions
VASTU_ENHANCEMENTS = {
    "north": "ample natural lighting, water elements, blue/green accents",
    "south": "heavy furniture placement, red/earth tones, stability",
    "east": "open spaces, morning light, wooden elements",
    "west": "metal accents, white/grey tones, evening ambiance",
}


class AIGenerationEngine:
    """AI engine for generating interior designs with ControlNet."""

    def __init__(self):
        self.settings = get_settings()

    def build_prompt(
        self,
        room_type: str,
        style: str,
        wall_color: Optional[str] = None,
        flooring: Optional[str] = None,
        furniture_style: Optional[str] = None,
        direction_hints: Optional[List[str]] = None
    ) -> str:
        """Build the generation prompt with customization options."""
        
        # Base style template
        base_style = STYLE_TEMPLATES.get(style, style)
        
        # Build customization string
        customizations = []
        if wall_color:
            customizations.append(f"walls painted {wall_color}")
        if flooring:
            customizations.append(f"flooring made of {flooring}")
        if furniture_style:
            customizations.append(f"{furniture_style} furniture")
        
        # Add Vastu enhancements based on directions
        vastu_hint = ""
        if direction_hints:
            for direction in direction_hints:
                if direction in VASTU_ENHANCEMENTS:
                    vastu_hint += f", {VASTU_ENHANCEMENTS[direction]}"
        
        # Combine into final prompt
        customization_str = ", ".join(customizations) if customizations else ""
        
        prompt = (
            f"Interior design for a {room_type}, {base_style}, "
            f"{customization_str}, high quality photorealistic render, "
            f"professional interior photography, detailed textures{vastu_hint}. "
            f"Preserve original room layout and proportions. "
            f"Vastu Shastra compliant design principles."
        )
        
        return prompt

    async def generate_design(
        self,
        room_images: Dict[str, str],
        room_type: str,
        style: str,
        customization: Optional[Dict] = None,
        num_variations: int = 3
    ) -> Dict:
        """
        Generate AI interior designs from room images.
        
        Args:
            room_images: Dict with north, south, east, west image URLs
            room_type: Type of room (living room, bedroom, etc.)
            style: Design style (modern, traditional, etc.)
            customization: Dict with wall_color, flooring, furniture_style
            num_variations: Number of design variations to generate
            
        Returns:
            Dict with design_id, generated image URLs, and metadata
        """
        customization = customization or {}
        
        # Build the prompt
        prompt = self.build_prompt(
            room_type=room_type,
            style=style,
            wall_color=customization.get('wall_color'),
            flooring=customization.get('flooring'),
            furniture_style=customization.get('furniture_style'),
            direction_hints=list(room_images.keys())
        )
        
        # Generate images (simulated for MVP - replace with actual SD API)
        generated_images = await self._call_stable_diffusion(
            prompt=prompt,
            control_images=room_images,
            num_variations=num_variations
        )
        
        # Create design record
        design_id = str(uuid.uuid4())
        design_data = {
            'design_id': design_id,
            'prompt_used': prompt,
            'generated_images': generated_images,
            'style': style,
            'customization': customization,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'completed'
        }
        
        return design_data

    async def _call_stable_diffusion(
        self,
        prompt: str,
        control_images: Dict[str, str],
        num_variations: int
    ) -> List[str]:
        """
        Call Stable Diffusion API with ControlNet.
        
        For MVP: Returns placeholder URLs. Replace with actual API integration.
        """
        # TODO: Replace with actual SD API call
        # Example using Stability AI API:
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(SD_API_URL, ...) as response:
        #         ...
        
        # For now, return placeholder URLs
        placeholder_urls = [
            f"https://placehold.co/1024x768/amber/white?text=AI+Design+Variation+{i+1}"
            for i in range(num_variations)
        ]
        
        return placeholder_urls

    async def regenerate_with_customization(
        self,
        room_images: Dict[str, str],
        previous_design: Dict,
        new_customization: Dict
    ) -> Dict:
        """
        Regenerate design with new customization options.
        
        Args:
            room_images: Dict with 4 directional image URLs
            previous_design: Previous design data
            new_customization: New customization options
            
        Returns:
            Dict with new design data
        """
        # Merge previous customization with new changes
        merged_customization = {
            **previous_design.get('customization', {}),
            **new_customization
        }
        
        # Generate new designs
        return await self.generate_design(
            room_images=room_images,
            room_type=previous_design.get('room_type', 'room'),
            style=previous_design.get('style', 'modern'),
            customization=merged_customization,
            num_variations=3
        )


# Singleton instance
ai_engine = AIGenerationEngine()
