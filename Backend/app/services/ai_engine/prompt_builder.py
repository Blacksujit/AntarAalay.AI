"""
Prompt Builder for Interior Styling

This module creates optimized prompts for image-to-image interior transformation
that preserve room geometry while adding furniture and styling.

Key Principles:
- Preserve original layout and geometry
- Guide furniture placement and styling
- Maintain realistic scale and perspective
- Avoid geometric distortion
"""

from typing import Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class StyleParameters:
    """Interior styling parameters."""
    room_type: str
    furniture_style: str
    wall_color: str
    flooring_material: str
    lighting_style: Optional[str] = None
    additional_elements: Optional[str] = None


class PromptBuilder:
    """
    Builds optimized prompts for interior image-to-image transformation.
    
    Focuses on layout preservation while adding realistic furniture and styling.
    """
    
    # Room type mappings for better prompt specificity
    ROOM_TYPE_MAPPINGS = {
        'living': 'living room',
        'bedroom': 'bedroom',
        'kitchen': 'kitchen',
        'dining': 'dining room',
        'bathroom': 'bathroom',
        'study': 'home office',
        'office': 'office',
        'hallway': 'hallway'
    }
    
    # Furniture style mappings with descriptive terms
    FURNITURE_STYLE_MAPPINGS = {
        'modern': 'modern minimalist furniture',
        'contemporary': 'contemporary furniture',
        'scandinavian': 'Scandinavian light wood furniture',
        'industrial': 'industrial metal and wood furniture',
        'traditional': 'traditional classic furniture',
        'rustic': 'rustic farmhouse furniture',
        'luxury': 'luxury high-end furniture',
        'midcentury': 'mid-century modern furniture',
        'bohemian': 'bohemian eclectic furniture',
        'minimalist': 'minimalist clean-lined furniture'
    }
    
    # Color mappings with natural descriptions
    COLOR_MAPPINGS = {
        'white': 'crisp white',
        'gray': 'warm gray',
        'beige': 'soft beige',
        'blue': 'calming blue',
        'green': 'sage green',
        'navy': 'deep navy blue',
        'black': 'charcoal black',
        'brown': 'warm brown',
        'cream': 'creamy off-white',
        'lightgray': 'light gray'
    }
    
    # Flooring material mappings
    FLOORING_MAPPINGS = {
        'hardwood': 'natural hardwood flooring',
        'laminate': 'laminate wood flooring',
        'tile': 'ceramic tile',
        'carpet': 'plush carpet',
        'vinyl': 'luxury vinyl flooring',
        'stone': 'natural stone flooring',
        'marble': 'polished marble flooring',
        'concrete': 'polished concrete flooring'
    }
    
    def build_positive_prompt(
        self, 
        style_params: StyleParameters,
        preserve_geometry: bool = True
    ) -> str:
        """
        Build a positive prompt for interior transformation.
        
        Args:
            style_params: Styling parameters
            preserve_geometry: Whether to emphasize geometry preservation
            
        Returns:
            Optimized positive prompt string
        """
        # Map parameters to descriptive terms
        room_desc = self.ROOM_TYPE_MAPPINGS.get(style_params.room_type.lower(), style_params.room_type)
        furniture_desc = self.FURNITURE_STYLE_MAPPINGS.get(style_params.furniture_style.lower(), style_params.furniture_style)
        wall_color_desc = self.COLOR_MAPPINGS.get(style_params.wall_color.lower(), style_params.wall_color)
        flooring_desc = self.FLOORING_MAPPINGS.get(style_params.flooring_material.lower(), style_params.flooring_material)
        
        # Base prompt with geometry preservation
        if preserve_geometry:
            base_prompt = (
                f"Photorealistic architectural interior transformation of an empty {room_desc}. "
                f"Preserve original room geometry, wall positions, and perspective exactly. "
                f"Add realistic {furniture_desc} that fits the space naturally. "
                f"Walls painted {wall_color_desc}. "
                f"Flooring: {flooring_desc}. "
                f"Maintain realistic scale, proper furniture placement, natural lighting interaction."
            )
        else:
            base_prompt = (
                f"Beautiful {room_desc} with {furniture_desc}. "
                f"Walls painted {wall_color_desc}. "
                f"Flooring: {flooring_desc}. "
                f"Interior design, architectural photography."
            )
        
        # Add optional elements
        if style_params.lighting_style:
            base_prompt += f" {style_params.lighting_style} lighting."
        
        if style_params.additional_elements:
            base_prompt += f" {style_params.additional_elements}."
        
        # Quality and style modifiers
        base_prompt += (
            " Ultra realistic, high detail, professional architectural photography, "
            "volumetric lighting, depth accurate, physically grounded furniture, "
            "no distortion, proper scale."
        )
        
        return base_prompt.strip()
    
    def build_negative_prompt(self, preserve_geometry: bool = True) -> str:
        """
        Build a negative prompt to avoid common artifacts.
        
        Args:
            preserve_geometry: Whether to emphasize geometry preservation
            
        Returns:
            Negative prompt string
        """
        base_negative = (
            "distorted perspective, warped walls, broken geometry, floating furniture, "
            "unrealistic proportions, deformed objects, low resolution, blurry, "
            "text, watermark, signature, duplicate objects, extra windows, "
            "doors in wrong places, furniture clipping through walls"
        )
        
        if preserve_geometry:
            base_negative += (
                ", stretched perspective, bent walls, incorrect scale, "
                "impossible furniture placement, objects defying gravity, "
                "hallucinated architectural elements"
            )
        
        base_negative += (
            ", cartoon, illustration, painting, art, anime, 3d render, "
            "oversaturated, unrealistic colors"
        )
        
        return base_negative.strip()
    
    def build_controlnet_prompt(
        self, 
        style_params: StyleParameters,
        edge_strength: float = 1.0
    ) -> Dict[str, str]:
        """
        Build prompts optimized for ControlNet conditioning.
        
        Args:
            style_params: Styling parameters
            edge_strength: ControlNet edge strength
            
        Returns:
            Dictionary with positive and negative prompts
        """
        positive = self.build_positive_prompt(style_params, preserve_geometry=True)
        
        # Add ControlNet-specific guidance
        if edge_strength > 0.8:
            positive += " Follow the structural edges precisely."
        
        negative = self.build_negative_prompt(preserve_geometry=True)
        
        return {
            'positive': positive,
            'negative': negative
        }
    
    def get_style_variations(self, base_style: str) -> Dict[str, str]:
        """
        Get style variations for regeneration options.
        
        Args:
            base_style: Base furniture style
            
        Returns:
            Dictionary of style variations
        """
        variations = {
            'warmer': f"{base_style} with warm tones and cozy atmosphere",
            'cooler': f"{base_style} with cool tones and modern feel",
            'minimal': f"minimalist {base_style} with clean lines",
            'luxury': f"luxury {base_style} with premium materials",
            'eclectic': f"eclectic mix with {base_style} elements"
        }
        
        return variations
    
    def validate_style_parameters(self, style_params: StyleParameters) -> tuple[bool, Optional[str]]:
        """
        Validate style parameters.
        
        Args:
            style_params: Parameters to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not style_params.room_type:
            return False, "Room type is required"
        
        if not style_params.furniture_style:
            return False, "Furniture style is required"
        
        if not style_params.wall_color:
            return False, "Wall color is required"
        
        if not style_params.flooring_material:
            return False, "Flooring material is required"
        
        return True, None
    
    def get_prompt_hash(self, style_params: StyleParameters) -> str:
        """
        Generate a hash for prompt caching and deduplication.
        
        Args:
            style_params: Style parameters
            
        Returns:
            Hash string
        """
        import hashlib
        
        prompt_data = (
            f"{style_params.room_type}_{style_params.furniture_style}_"
            f"{style_params.wall_color}_{style_params.flooring_material}_"
            f"{style_params.lighting_style}_{style_params.additional_elements}"
        )
        
        return hashlib.md5(prompt_data.encode()).hexdigest()[:8]


class PromptTemplate:
    """
    Pre-defined prompt templates for common interior scenarios.
    """
    
    TEMPLATES = {
        'modern_living': {
            'positive': "Modern living room with clean lines, minimalist furniture, neutral colors, natural light, open space",
            'negative': "cluttered, dark, traditional, ornate, crowded"
        },
        'cozy_bedroom': {
            'positive': "Cozy bedroom with soft lighting, comfortable furniture, warm colors, peaceful atmosphere",
            'negative': "sterile, cold, bright, office-like, minimal"
        },
        'gourmet_kitchen': {
            'positive': "Gourmet kitchen with modern appliances, ample counter space, stylish backsplash, functional layout",
            'negative': "cramped, outdated, dark, poorly organized"
        }
    }
    
    @classmethod
    def get_template(cls, template_name: str) -> Optional[Dict[str, str]]:
        """Get a pre-defined prompt template."""
        return cls.TEMPLATES.get(template_name)
    
    @classmethod
    def list_templates(cls) -> list[str]:
        """List available template names."""
        return list(cls.TEMPLATES.keys())
    
    def build_prompt(self, furniture_style: str, wall_color: str, flooring_material: str) -> tuple[str, str]:
        """
        Build prompts for interior design transformation.
        
        Args:
            furniture_style: Style of furniture (e.g., "modern", "traditional")
            wall_color: Wall color (e.g., "white", "beige")
            flooring_material: Flooring material (e.g., "hardwood", "carpet")
            
        Returns:
            Tuple of (positive_prompt, negative_prompt)
        """
        # Positive prompt according to specifications
        positive_prompt = (
            f"Photorealistic interior redesign of the given empty room. "
            f"Preserve original geometry, walls, and perspective. "
            f"Add {furniture_style} furniture. "
            f"Walls painted {wall_color}. "
            f"Flooring made of {flooring_material}. "
            f"Natural lighting, realistic shadows, correct scale, "
            f"physically grounded objects."
        )
        
        # Negative prompt according to specifications
        negative_prompt = (
            "warped walls, broken perspective, floating furniture, "
            "distorted geometry, unrealistic proportions, "
            "low resolution, text, watermark"
        )
        
        return positive_prompt, negative_prompt
