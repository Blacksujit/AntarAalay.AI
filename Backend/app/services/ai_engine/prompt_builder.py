"""
Prompt Builder for AI Image Generation

Builds detailed prompts for interior design generation
based on style, room type, and user preferences.
"""

from typing import Dict, List


class PromptBuilder:
    """
    Builds detailed prompts for interior design generation.
    """
    
    # Style descriptors
    STYLE_PROMPTS = {
        'modern': 'modern minimalist interior design, clean lines, neutral colors, professional photography',
        'traditional': 'traditional Indian interior design, rich colors, ethnic patterns, wooden furniture',
        'minimalist': 'minimalist interior design, white and beige tones, simple furniture, uncluttered space',
        'luxury': 'luxurious interior design, premium materials, elegant furniture, sophisticated decor',
        'bohemian': 'bohemian interior design, eclectic decor, vibrant colors, mix of patterns, cozy atmosphere',
        'industrial': 'industrial interior design, exposed brick, metal accents, rustic wood, urban style',
        'scandinavian': 'scandinavian interior design, light wood, white walls, cozy textiles, functional furniture',
        'contemporary': 'contemporary interior design, sleek furniture, bold accents, geometric patterns'
    }
    
    # Room type descriptors
    ROOM_PROMPTS = {
        'living': 'living room with comfortable seating, coffee table, entertainment center',
        'bedroom': 'bedroom with comfortable bed, nightstands, wardrobe, peaceful atmosphere',
        'kitchen': 'kitchen with modern appliances, countertops, cabinets, good lighting',
        'dining': 'dining room with table, chairs, elegant lighting, formal setting',
        'bathroom': 'bathroom with modern fixtures, clean design, good ventilation',
        'office': 'home office with desk, chair, storage, professional environment',
        'study': 'study room with bookshelves, desk, comfortable reading chair'
    }
    
    # Quality and detail enhancers
    QUALITY_ENHANCERS = [
        'high quality',
        '4k resolution',
        'professional photography',
        'detailed textures',
        'realistic lighting',
        'sharp focus',
        'interior design magazine style'
    ]
    
    # Negative prompts to avoid
    NEGATIVE_PROMPTS = [
        'blurry',
        'low quality',
        'distorted',
        'deformed',
        'bad anatomy',
        'watermark',
        'text',
        'ugly',
        'duplicate',
        'cartoon',
        'drawing',
        'painting'
    ]
    
    def build_prompt(
        self,
        style: str,
        room_type: str,
        wall_color: str = None,
        flooring_material: str = None,
        additional_details: List[str] = None
    ) -> str:
        """
        Build a comprehensive prompt for interior design generation.
        
        Args:
            style: Interior design style (modern, traditional, etc.)
            room_type: Type of room (living, bedroom, etc.)
            wall_color: Wall color preference
            flooring_material: Flooring material preference
            additional_details: Additional descriptive details
            
        Returns:
            Complete prompt string
        """
        # Get base style and room descriptions
        style_desc = self.STYLE_PROMPTS.get(style.lower(), self.STYLE_PROMPTS['modern'])
        room_desc = self.ROOM_PROMPTS.get(room_type.lower(), self.ROOM_PROMPTS['living'])
        
        # Build prompt components
        components = [style_desc, room_desc]
        
        # Add color if specified
        if wall_color:
            components.append(f'{wall_color} walls')
        
        # Add flooring if specified
        if flooring_material:
            components.append(f'{flooring_material} flooring')
        
        # Add additional details
        if additional_details:
            components.extend(additional_details)
        
        # Add quality enhancers
        components.extend(self.QUALITY_ENHANCERS)
        
        # Combine all components
        positive_prompt = ', '.join(components)
        
        return positive_prompt
    
    def get_negative_prompt(self) -> str:
        """
        Get the negative prompt to avoid unwanted elements.
        
        Returns:
            Negative prompt string
        """
        return ', '.join(self.NEGATIVE_PROMPTS)
    
    def build_flux_prompt(
        self,
        style: str,
        room_type: str,
        wall_color: str = None,
        flooring_material: str = None
    ) -> str:
        """
        Build prompt optimized for FLUX.1-schnell model.
        
        Args:
            style: Interior design style
            room_type: Type of room
            wall_color: Wall color
            flooring_material: Flooring material
            
        Returns:
            FLUX-optimized prompt
        """
        # FLUX prefers more natural language prompts
        prompt_parts = []
        
        # Main description
        style_desc = self.STYLE_PROMPTS.get(style.lower(), self.STYLE_PROMPTS['modern'])
        room_desc = self.ROOM_PROMPTS.get(room_type.lower(), self.ROOM_PROMPTS['living'])
        
        prompt_parts.append(f"A beautiful {style_desc} of a {room_desc}")
        
        # Add specific details
        if wall_color:
            prompt_parts.append(f"with {wall_color} walls")
        
        if flooring_material:
            prompt_parts.append(f"featuring {flooring_material} floors")
        
        # Add quality and atmosphere
        prompt_parts.extend([
            "bright natural lighting",
            "professional interior photography",
            "high quality detailed",
            "4k resolution"
        ])
        
        return ', '.join(prompt_parts)
