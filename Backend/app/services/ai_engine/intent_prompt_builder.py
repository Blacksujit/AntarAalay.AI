"""
Intent-Based Prompt Builder for Personalized Interior Design Generation

Generates detailed, room-specific prompts that adapt based on:
- Room type (kitchen, bedroom, living, etc.)
- Design style (modern, traditional, etc.)
- Materials and colors
- Functional intent of the space
- VASTU-SPECIFIC PRINCIPLES for aligned designs
"""

from typing import Dict, List, Optional
from app.services.ai_engine.base_engine import GenerationRequest


class IntentBasedPromptBuilder:
    """
    Advanced prompt builder that creates highly specific, room-appropriate prompts
    based on the user's intent and selections with VASTU-SPECIFIC principles.
    """
    
    # VASTU-SPECIFIC PRINCIPLES FOR EACH DIRECTION AND ROOM TYPE
    VASTU_PRINCIPLES = {
        # Room-specific Vastu guidelines
        'room_directions': {
            'kitchen': {
                'ideal': 'southeast',
                'alternative': 'northwest',
                'elements': ['fire', 'air'],
                'colors': ['red', 'orange', 'yellow', 'pink'],
                'avoid': ['northeast', 'southwest'],
                'principles': [
                    'Cooking platform facing east',
                    'Water sink in northeast corner',
                    'Storage in south or west walls',
                    'Gas stove in southeast corner',
                    'Windows and ventilation in east and north',
                    'Electrical appliances in southeast',
                    'Grains and food storage in southwest'
                ]
            },
            'bedroom': {
                'ideal': 'southwest',
                'alternative': 'west',
                'elements': ['earth', 'air'],
                'colors': ['blue', 'green', 'light yellow', 'white'],
                'avoid': ['northeast', 'southeast'],
                'principles': [
                    'Bed placed in southwest corner',
                    'Head facing south or east',
                    'Wardrobe in southwest or west',
                    'Dressing table in west or north',
                    'Windows in east and north',
                    'Mirror on north or east wall',
                    'Avoid bed under beam',
                    'Keep northeast corner clean and empty'
                ]
            },
            'living': {
                'ideal': 'north',
                'alternative': 'east',
                'elements': ['air', 'water'],
                'colors': ['green', 'blue', 'white', 'cream'],
                'avoid': ['southwest'],
                'principles': [
                    'Sitting arrangement facing north or east',
                    'Heavy furniture in south or west',
                    'Light furniture in north or east',
                    'Windows in north and east',
                    'Main door in north or east',
                    'Decorative items in northeast',
                    'Avoid clutter in northeast corner',
                    'Keep center space open'
                ]
            },
            'dining': {
                'ideal': 'west',
                'alternative': 'east',
                'elements': ['earth', 'fire'],
                'colors': ['orange', 'yellow', 'cream', 'light brown'],
                'avoid': ['southwest'],
                'principles': [
                    'Dining table in west or northwest',
                    'Facing east or north while eating',
                    'Kitchen access in southeast',
                    'Windows in east or north',
                    'Water arrangement in northeast',
                    'Avoid dining table under beam',
                    'Keep space well-lit and ventilated',
                    'Display positive artwork'
                ]
            },
            'bathroom': {
                'ideal': 'northwest',
                'alternative': 'southeast',
                'elements': ['water', 'fire'],
                'colors': ['white', 'light blue', 'cream', 'light gray'],
                'avoid': ['northeast', 'southwest'],
                'principles': [
                    'Toilet in northwest or southeast',
                    'Bathroom fixtures in west or south',
                    'Mirror on north or east wall',
                    'Drainage in northeast',
                    'Windows in north or east',
                    'Keep bathroom clean and dry',
                    'Avoid bathroom in center',
                    'Proper ventilation essential'
                ]
            },
            'office': {
                'ideal': 'north',
                'alternative': 'east',
                'elements': ['air', 'water'],
                'colors': ['green', 'blue', 'white', 'light yellow'],
                'avoid': ['southwest'],
                'principles': [
                    'Desk facing north or east',
                    'Sitting with back to south or west',
                    'Storage in south or west',
                    'Computer in southeast',
                    'Windows in north or east',
                    'Books in southwest',
                    'Keep northeast corner clean',
                    'Avoid clutter under desk'
                ]
            }
        },
        # Direction-specific elements and energies
        'directions': {
            'north': {
                'element': 'water',
                'energy': 'positive financial flow',
                'colors': ['green', 'blue'],
                'materials': ['wood', 'glass'],
                'features': ['water features', 'plants', 'mirrors']
            },
            'south': {
                'element': 'fire',
                'energy': 'passion and recognition',
                'colors': ['red', 'orange', 'yellow'],
                'materials': ['wood', 'metal'],
                'features': ['lighting', 'artwork', 'achievements']
            },
            'east': {
                'element': 'air',
                'energy': 'new beginnings and health',
                'colors': ['green', 'white', 'cream'],
                'materials': ['wood', 'natural materials'],
                'features': ['windows', 'plants', 'natural light']
            },
            'west': {
                'element': 'space',
                'energy': 'creativity and children',
                'colors': ['white', 'silver', 'light gray'],
                'materials': ['metal', 'glass'],
                'features': ['creative items', 'family photos', 'artwork']
            },
            'northeast': {
                'element': 'water',
                'energy': 'spiritual and meditation',
                'colors': ['white', 'cream', 'light blue'],
                'materials': ['crystal', 'stone'],
                'features': ['meditation space', 'water features', 'spiritual items']
            },
            'northwest': {
                'element': 'air',
                'energy': 'social connections and travel',
                'colors': ['white', 'light gray', 'silver'],
                'materials': ['metal', 'glass'],
                'features': ['guest seating', 'communication devices', 'travel items']
            },
            'southeast': {
                'element': 'fire',
                'energy': 'wealth and abundance',
                'colors': ['green', 'red', 'orange'],
                'materials': ['wood', 'natural materials'],
                'features': ['money plants', 'wealth symbols', 'kitchen elements']
            },
            'southwest': {
                'element': 'earth',
                'energy': 'stability and relationships',
                'colors': ['yellow', 'beige', 'brown'],
                'materials': ['earth materials', 'heavy furniture'],
                'features': ['heavy furniture', 'relationship symbols', 'stability items']
            }
        },
        # Vastu elements and their representations
        'elements': {
            'water': {
                'colors': ['blue', 'black', 'white'],
                'materials': ['glass', 'mirrors', 'fountains'],
                'shapes': ['flowing', 'irregular'],
                'features': ['water features', 'aquariums', 'fountains']
            },
            'fire': {
                'colors': ['red', 'orange', 'yellow', 'pink'],
                'materials': ['wood', 'metal', 'lighting'],
                'shapes': ['triangular', 'pointed'],
                'features': ['lighting', 'candles', 'fireplace', 'sunlight']
            },
            'earth': {
                'colors': ['yellow', 'brown', 'beige', 'terracotta'],
                'materials': ['stone', 'ceramic', 'earth materials'],
                'shapes': ['square', 'stable'],
                'features': ['ceramic items', 'stone decor', 'plants']
            },
            'air': {
                'colors': ['green', 'white', 'light blue'],
                'materials': ['wood', 'natural materials', 'fabrics'],
                'shapes': ['rectangular', 'vertical'],
                'features': ['plants', 'wind chimes', 'good ventilation', 'fabrics']
            },
            'space': {
                'colors': ['white', 'cream', 'light gray', 'silver'],
                'materials': ['metal', 'glass', 'minimal materials'],
                'shapes': ['circular', 'open'],
                'features': ['open space', 'minimal decor', 'sky views', 'light']
            }
        }
    }
    
    # Room-specific elements and functional descriptions
    ROOM_INTENTS = {
        'kitchen': {
            'function': 'culinary workspace',
            'key_elements': ['countertops', 'cabinets', 'backsplash', 'island', 'appliances', 'sink', 'lighting'],
            'atmosphere': 'functional yet beautiful cooking environment',
            'activities': 'food preparation, cooking, and casual dining'
        },
        'bedroom': {
            'function': 'restful sanctuary',
            'key_elements': ['bed', 'nightstands', 'wardrobe', 'dresser', 'headboard', 'lighting', 'window treatments'],
            'atmosphere': 'peaceful sleeping retreat',
            'activities': 'rest, sleep, and relaxation'
        },
        'living': {
            'function': 'social gathering space',
            'key_elements': ['sofa', 'coffee table', 'entertainment center', 'accent chairs', 'bookshelves', 'lighting'],
            'atmosphere': 'comfortable conversational area',
            'activities': 'entertaining guests, relaxation, family time'
        },
        'dining': {
            'function': 'formal eating area',
            'key_elements': ['dining table', 'chairs', 'sideboard', 'buffet', 'chandelier', 'display cabinet'],
            'atmosphere': 'elegant dining atmosphere',
            'activities': 'meals, dinner parties, special occasions'
        },
        'bathroom': {
            'function': 'personal hygiene space',
            'key_elements': ['vanity', 'mirror', 'shower', 'bathtub', 'toilet', 'storage', 'lighting'],
            'atmosphere': 'spa-like rejuvenation zone',
            'activities': 'daily grooming, relaxation'
        },
        'office': {
            'function': 'productive workspace',
            'key_elements': ['desk', 'chair', 'shelving', 'filing cabinets', 'task lighting', 'computer setup'],
            'atmosphere': 'focused professional environment',
            'activities': 'work, study, creative tasks'
        }
    }
    
    # Style-specific characteristics with detailed descriptors
    STYLE_PROFILES = {
        'modern': {
            'philosophy': 'clean lines, minimal ornamentation, functional simplicity',
            'materials': ['polished metals', 'glass', 'concrete', 'smooth woods', 'chrome accents'],
            'colors': ['neutral palette', 'monochromatic schemes', 'bold accent colors'],
            'furniture': ['streamlined silhouettes', 'geometric shapes', 'low-profile pieces'],
            'lighting': ['recessed lighting', 'statement fixtures', 'natural light emphasis'],
            'texture': ['smooth surfaces', 'minimal texture', 'clean finishes']
        },
        'traditional': {
            'philosophy': 'timeless elegance, classic details, ornate craftsmanship',
            'materials': ['rich hardwoods', 'brass', 'crystal', 'upholstered fabrics', 'marble'],
            'colors': ['warm deep tones', 'rich jewel colors', 'classic neutrals'],
            'furniture': ['carved details', 'curved lines', 'wingback chairs', 'pedestal tables'],
            'lighting': ['chandeliers', 'sconces', 'table lamps with fabric shades'],
            'texture': ['plush upholstery', 'drapery', 'patterned rugs', 'textured walls']
        },
        'scandinavian': {
            'philosophy': 'hygge comfort, functional simplicity, natural elements',
            'materials': ['light woods', 'wool', 'linen', 'natural fibers', 'ceramics'],
            'colors': ['whites', 'light grays', 'soft pastels', 'natural wood tones'],
            'furniture': ['clean lines', 'tapered legs', 'functional designs', 'organic shapes'],
            'lighting': ['soft ambient lighting', 'candlelight', 'large windows'],
            'texture': ['cozy textiles', 'knitted throws', 'natural textures', 'warm woods']
        },
        'bohemian': {
            'philosophy': 'eclectic freedom, global influences, artistic expression',
            'materials': ['rattan', 'macramé', 'vintage textiles', 'natural materials', 'mixed metals'],
            'colors': ['rich jewel tones', 'earthy colors', 'vibrant patterns', 'warm palette'],
            'furniture': ['mix of vintage and modern', 'low seating', 'floor cushions', 'unique pieces'],
            'lighting': ['string lights', 'lanterns', 'natural light', 'colorful lamps'],
            'texture': ['layered textiles', 'patterns', 'tassels', 'fringe', 'natural fibers']
        },
        'industrial': {
            'philosophy': 'raw authenticity, urban loft aesthetic, exposed elements',
            'materials': ['raw concrete', 'exposed brick', 'steel beams', 'reclaimed wood', 'metal pipes'],
            'colors': ['grays', 'browns', 'rust tones', 'black accents', 'neutral palette'],
            'furniture': ['utilitarian pieces', 'metal frames', 'wood and metal combinations', 'raw finishes'],
            'lighting': [' Edison bulbs', 'metal fixtures', 'track lighting', 'warehouse-style windows'],
            'texture': ['rough surfaces', 'distressed finishes', 'raw materials', 'weathered textures']
        },
        'coastal': {
            'philosophy': 'beachside serenity, light and airy, natural seaside elements',
            'materials': ['light woods', 'wicker', 'linen', 'cotton', 'natural fibers'],
            'colors': ['whites', 'soft blues', 'sandy beiges', 'seafoam greens', 'coral accents'],
            'furniture': ['slipcovered pieces', 'cane details', 'light-colored woods', 'casual comfort'],
            'lighting': ['natural light', 'driftwood fixtures', 'glass table lamps', 'nautical elements'],
            'texture': ['light fabrics', 'natural textures', 'weathered wood', 'sea-grass rugs']
        }
    }
    
    # Material-specific enhancements
    MATERIAL_ENHANCEMENTS = {
        'hardwood': {
            'description': 'rich hardwood flooring with visible grain patterns',
            'variants': ['oak', 'maple', 'walnut', 'cherry', 'bamboo'],
            'finish': 'satin or matte finish highlighting natural wood beauty'
        },
        'laminate': {
            'description': 'durable laminate flooring with realistic wood texture',
            'variants': ['wood-look', 'stone-look', 'modern patterns'],
            'finish': 'seamless planks with realistic texture'
        },
        'tile': {
            'description': 'elegant tile flooring with sophisticated patterns',
            'variants': ['ceramic', 'porcelain', 'marble-look', 'geometric patterns'],
            'finish': 'grouted tiles with clean lines and modern layout'
        },
        'carpet': {
            'description': 'plush carpeting for comfort and warmth',
            'variants': ['cut-pile', 'berber', 'patterned', 'solid colors'],
            'finish': 'soft, dense pile with comfortable underfoot feel'
        },
        'vinyl': {
            'description': 'modern luxury vinyl flooring with realistic textures',
            'variants': ['wood-look planks', 'stone-look tiles', 'modern patterns'],
            'finish': 'water-resistant surface with authentic texture replication'
        }
    }
    
    def build_intent_prompt(self, request: GenerationRequest, variation: int = 1) -> str:
        """
        Build a highly specific, Vastu-aligned prompt for interior design generation.
        
        Args:
            request: Generation request with room type, style, and materials
            variation: Variation number (1, 2, or 3) for different interpretations
            
        Returns:
            Detailed, Vastu-specific prompt tailored to the user's selections
        """
        room_type = request.room_type or 'living'
        style = request.furniture_style or 'modern'
        wall_color = request.wall_color or 'white'
        flooring = request.flooring_material or 'hardwood'
        
        # Get Vastu-specific guidelines for this room type
        vastu_room = self.VASTU_PRINCIPLES['room_directions'].get(room_type, {})
        ideal_direction = vastu_room.get('ideal', 'north')
        vastu_elements = vastu_room.get('elements', ['earth'])
        vastu_colors = vastu_room.get('colors', ['white'])
        vastu_principles = vastu_room.get('principles', [])
        
        # Get direction-specific energy
        direction_info = self.VASTU_PRINCIPLES['directions'].get(ideal_direction, {})
        direction_element = direction_info.get('element', 'earth')
        direction_energy = direction_info.get('energy', 'positive energy')
        direction_materials = direction_info.get('materials', ['wood'])
        direction_features = direction_info.get('features', ['plants'])
        
        # Get element-specific representations
        element_info = self.VASTU_PRINCIPLES['elements'].get(direction_element, {})
        element_colors = element_info.get('colors', ['white'])
        element_materials = element_info.get('materials', ['wood'])
        element_features = element_info.get('features', ['plants'])
        
        # Get room-specific intent and elements
        room_intent = self.ROOM_INTENTS.get(room_type, self.ROOM_INTENTS['living'])
        style_profile = self.STYLE_PROFILES.get(style, self.STYLE_PROFILES['modern'])
        material_info = self.MATERIAL_ENHANCEMENTS.get(flooring, self.MATERIAL_ENHANCEMENTS['hardwood'])
        
        # VASTU-SPECIFIC PROMPT BUILDING
        
        # Core Vastu-aligned description
        prompt_parts = [
            f"Vastu-compliant professional interior design photograph of a stunning {style} {room_type}",
            f"strictly following Vastu Shastra principles for {ideal_direction} facing {room_type}",
            f"designed as a {room_intent['function']} for {room_intent['activities']}",
            f"creating a {room_intent['atmosphere']} enhanced with {direction_energy}"
        ]
        
        # Vastu elements and energy flow
        prompt_parts.append(
            f"Incorporating Vastu {direction_element} element with {', '.join(element_colors[:2])} colors, "
            f"using {', '.join(element_materials[:2])} and featuring {', '.join(element_features[:2])}"
        )
        
        # Style philosophy with Vastu alignment
        vastu_style_desc = self._get_vastu_style_description(style, direction_element)
        prompt_parts.append(
            f"Embodying {vastu_style_desc} with "
            f"{', '.join(style_profile['materials'][:3])} and "
            f"Vastu-approved {', '.join(vastu_colors[:2])}"
        )
        
        # Vastu-specific room elements based on variation
        vastu_elements_desc = self._get_vastu_room_elements(room_type, style, variation)
        prompt_parts.append(f"featuring {vastu_elements_desc}")
        
        # Vastu-compliant layout and arrangement
        layout_desc = self._get_vastu_layout_description(room_type, ideal_direction, variation)
        prompt_parts.append(f"with {layout_desc}")
        
        # Wall and flooring with Vastu considerations
        wall_desc = self._get_vastu_wall_description(wall_color, style, ideal_direction)
        prompt_parts.append(f"{wall_desc} walls")
        
        flooring_desc = self._get_vastu_flooring_description(flooring, style, direction_element)
        prompt_parts.append(f"with {flooring_desc}")
        
        # Vastu-specific lighting and energy
        lighting_desc = self._get_vastu_lighting_description(room_type, style, ideal_direction, variation)
        prompt_parts.append(lighting_desc)
        
        # Vastu decorative elements and symbols
        decor_desc = self._get_vastu_decor_description(room_type, style, direction_element, variation)
        prompt_parts.append(f"decorated with {decor_desc}")
        
        # Vastu principles implementation
        if vastu_principles:
            key_principles = vastu_principles[:3]  # Top 3 principles
            principles_desc = f"following Vastu principles: {', '.join(key_principles)}"
            prompt_parts.append(principles_desc)
        
        # Energy flow and atmosphere
        energy_desc = self._get_vastu_energy_description(direction_energy, room_type, variation)
        prompt_parts.append(f"creating {energy_desc}")
        
        # Photographic quality with Vastu emphasis
        prompt_parts.extend([
            "professional architectural photography emphasizing Vastu compliance",
            "natural lighting enhanced to promote positive energy flow",
            "4K ultra high resolution showing Vastu alignment",
            "photorealistic details of Vastu-compliant elements",
            "perfect composition following Vastu spatial rules",
            "Vastu-optimized interior design magazine quality"
        ])
        
        # Room-specific Vastu activity context
        vastu_activity = self._get_vastu_activity_context(room_type, ideal_direction, variation)
        prompt_parts.append(vastu_activity)
        
        # Combine all parts into a comprehensive Vastu prompt
        final_prompt = ", ".join(prompt_parts)
        
        # Ensure prompt is not too long for most AI models
        if len(final_prompt) > 900:
            # Truncate while keeping the most important Vastu elements
            final_prompt = final_prompt[:897] + "..."
        
        return final_prompt
    
    def _get_vastu_style_description(self, style: str, element: str) -> str:
        """Get Vastu-aligned style description."""
        vastu_styles = {
            'modern': f'clean lines with {element} element harmony',
            'traditional': f'classic elegance enhanced with {element} energy',
            'scandinavian': f'minimalist simplicity balanced with {element} principles',
            'bohemian': f'eclectic freedom guided by {element} flow',
            'industrial': f'raw authenticity grounded in {element} stability',
            'coastal': f'beachside serenity aligned with {element} energy'
        }
        return vastu_styles.get(style, f'{style} design with {element} element balance')
    
    def _get_vastu_room_elements(self, room_type: str, style: str, variation: int) -> str:
        """Get Vastu-compliant room elements based on variation."""
        elements_variations = {
            'kitchen': {
                1: 'southeast cooking platform with east-facing stove, northeast water sink, south wall storage',
                2: 'Vastu-compliant L-shaped kitchen with fire element in southeast, water in northeast',
                3: 'modular kitchen following Vastu with appliances in southeast, storage in southwest'
            },
            'bedroom': {
                1: 'southwest bed placement with head facing south, west wall wardrobe, northeast empty space',
                2: 'Vastu bed in southwest corner, north wall dressing table, east window for morning light',
                3: 'master bedroom with heavy furniture in south, mirror on west wall, clean northeast corner'
            },
            'living': {
                1: 'north-facing seating with heavy furniture in south, decorative items in northeast',
                2: 'Vastu living with light furniture in north, entertainment center in southeast',
                3: 'social arrangement facing east, open center space, positive energy flow'
            },
            'dining': {
                1: 'west-facing dining table with east-facing seating, northwest display cabinet',
                2: 'Vastu dining in northwest, kitchen access in southeast, northeast water arrangement',
                3: 'formal dining with west placement, proper lighting, positive artwork display'
            },
            'bathroom': {
                1: 'northwest toilet fixtures, west wall bathroom elements, northeast drainage',
                2: 'Vastu bathroom with proper ventilation, south wall fixtures, clean layout',
                3: 'southeast bathroom with proper positioning, good lighting, clean dry space'
            },
            'office': {
                1: 'north-facing desk with back to south, west wall storage, southeast computer',
                2: 'Vastu office with east-facing desk, southwest bookshelves, clean northeast',
                3: 'productivity workspace with proper positioning, good lighting, organized layout'
            }
        }
        return elements_variations.get(room_type, elements_variations['living']).get(variation, elements_variations[room_type][1])
    
    def _get_vastu_layout_description(self, room_type: str, direction: str, variation: int) -> str:
        """Get Vastu-compliant layout description."""
        layouts = {
            1: f'Vastu-optimized layout following {direction} direction principles',
            2: f'spatial arrangement aligned with {direction} energy flow',
            3: f'geometric harmony based on {direction} Vastu guidelines'
        }
        return layouts.get(variation, layouts[1])
    
    def _get_vastu_wall_description(self, color: str, style: str, direction: str) -> str:
        """Get Vastu-compliant wall description."""
        direction_colors = {
            'north': ['green', 'blue'],
            'south': ['red', 'orange'],
            'east': ['green', 'white'],
            'west': ['white', 'silver'],
            'northeast': ['white', 'cream'],
            'northwest': ['white', 'light gray'],
            'southeast': ['green', 'red'],
            'southwest': ['yellow', 'beige']
        }
        
        vastu_colors = direction_colors.get(direction, ['white'])
        base_color = color.lower()
        
        if base_color in vastu_colors:
            return f'Vastu-approved {color}'
        else:
            return f'{color} (balanced with Vastu principles)'
    
    def _get_vastu_flooring_description(self, flooring: str, style: str, element: str) -> str:
        """Get Vastu-compliant flooring description."""
        element_flooring = {
            'water': 'marble or light tiles to enhance water energy',
            'fire': 'wood or ceramic to balance fire element',
            'earth': 'stone or earth materials to ground earth energy',
            'air': 'light wood or natural materials for air flow',
            'space': 'minimal flooring with open feel for space element'
        }
        
        base_desc = self.MATERIAL_ENHANCEMENTS.get(flooring, self.MATERIAL_ENHANCEMENTS['hardwood'])['description']
        element_desc = element_flooring.get(element, 'compatible with Vastu principles')
        
        return f'{base_desc} enhanced with {element_desc}'
    
    def _get_vastu_lighting_description(self, room_type: str, style: str, direction: str, variation: int) -> str:
        """Get Vastu-compliant lighting description."""
        direction_lighting = {
            'north': 'bright natural lighting from north windows',
            'south': 'warm lighting balanced with south sunlight',
            'east': 'morning light from east-facing windows',
            'west': 'evening light from west windows',
            'northeast': 'soft spiritual lighting from northeast',
            'northwest': 'balanced lighting for social energy',
            'southeast': 'bright lighting for wealth energy',
            'southwest': 'warm stable lighting'
        }
        
        base_lighting = direction_lighting.get(direction, 'balanced natural and artificial lighting')
        
        if variation == 1:
            return f'Vastu-enhanced {base_lighting} with energy flow optimization'
        elif variation == 2:
            return f'natural {base_lighting} promoting positive Vastu energy'
        else:
            return f'well-lit space with {base_lighting} following Vastu principles'
    
    def _get_vastu_decor_description(self, room_type: str, style: str, element: str, variation: int) -> str:
        """Get Vastu-compliant decorative elements."""
        element_decor = {
            'water': 'water features, mirrors, and flowing decorations',
            'fire': 'lighting fixtures, candles, and warm decorative elements',
            'earth': 'stone decor, ceramic items, and earthy accessories',
            'air': 'plants, wind chimes, and light fabrics',
            'space': 'minimal decor with open space emphasis'
        }
        
        base_decor = element_decor.get(element, 'Vastu-compliant decorative elements')
        
        if variation == 1:
            return f'traditional Vastu symbols and {base_decor}'
        elif variation == 2:
            return f'modern Vastu-aligned {base_decor}'
        else:
            return f'contemporary {base_decor} with Vastu energy enhancement'
    
    def _get_vastu_energy_description(self, energy: str, room_type: str, variation: int) -> str:
        """Get Vastu energy flow description."""
        energy_descriptions = {
            1: f'harmonious {energy} circulation throughout the space',
            2: f'balanced {energy} flow following Vastu guidelines',
            3: f'optimized {energy} movement and positive vibrations'
        }
        return energy_descriptions.get(variation, energy_descriptions[1])
    
    def _get_vastu_activity_context(self, room_type: str, direction: str, variation: int) -> str:
        """Get Vastu-specific activity context."""
        contexts = {
            'kitchen': f'Vastu-optimized culinary workspace with {direction} fire element alignment',
            'bedroom': f'peaceful Vastu sleeping sanctuary with {direction} stability energy',
            'living': f'harmonious Vastu social space enhanced with {direction} positive energy',
            'dining': f'Vastu-compliant dining area with {direction} energy for nourishment',
            'bathroom': f'clean Vastu hygiene space with {direction} purification energy',
            'office': f'productive Vastu workspace with {direction} success-oriented energy'
        }
        return contexts.get(room_type, f'Vastu-aligned {room_type} with {direction} energy enhancement')
    
    def _get_wall_description(self, color: str, style: str) -> str:
        """Get style-appropriate wall description."""
        color_mapping = {
            'white': 'crisp white' if style == 'modern' else 'warm white',
            'gray': 'sophisticated gray',
            'beige': 'soft beige',
            'blue': 'calming blue',
            'green': 'serene green',
            'red': 'bold red',
            'yellow': 'sunny yellow',
            'black': 'dramatic black',
            'brown': 'rich brown'
        }
        
        base_color = color_mapping.get(color.lower(), color)
        
        style_modifiers = {
            'modern': f'smooth {base_color}',
            'traditional': f'elegant {base_color}',
            'scandinavian': f'light {base_color}',
            'bohemian': f'warm {base_color}',
            'industrial': f'matte {base_color}',
            'coastal': f'airy {base_color}'
        }
        
        return style_modifiers.get(style, base_color)
    
    def _get_lighting_description(self, room_type: str, style: str) -> str:
        """Get room and style-specific lighting description."""
        lighting_scenarios = {
            'kitchen': {
                'modern': 'under-cabinet LED lighting and pendant lights over island',
                'traditional': 'classic chandelier and task lighting',
                'scandinavian': 'natural light with minimalist fixtures',
                'bohemian': 'eclectic mix of pendant lights and warm lamps',
                'industrial': 'metal pendant lights and track lighting',
                'coastal': 'natural light with rope-wrapped fixtures'
            },
            'bedroom': {
                'modern': 'recessed lighting with sleek bedside lamps',
                'traditional': 'elegant chandelier and table lamps',
                'scandinavian': 'soft diffused lighting with simple fixtures',
                'bohemian': 'string lights and colorful lanterns',
                'industrial': 'Edison bulb fixtures and wall sconces',
                'coastal': 'natural light with driftwood table lamps'
            },
            'living': {
                'modern': 'layered lighting with statement fixtures',
                'traditional': 'central chandelier with accent lamps',
                'scandinavian': 'large windows with simple ceiling fixtures',
                'bohemian': 'mix of floor lamps and eclectic lighting',
                'industrial': 'warehouse-style windows and metal fixtures',
                'coastal': 'abundant natural light with casual fixtures'
            }
        }
        
        default_lighting = 'natural and artificial lighting balance'
        
        return lighting_scenarios.get(room_type, {}).get(style, default_lighting)
    
    def build_negative_prompt(self, request: GenerationRequest) -> str:
        """Build negative prompt to avoid undesirable elements."""
        negative_elements = [
            'cluttered spaces',
            'poor lighting',
            'unnatural colors',
            'distorted proportions',
            'blurry details',
            'cartoonish elements',
            'oversized furniture',
            'empty rooms',
            'poorly arranged furniture',
            'unrealistic materials',
            'bad composition',
            'dark shadows',
            'overexposed areas'
        ]
        
        # Add style-specific negatives
        style = request.furniture_style or 'modern'
        if style == 'modern':
            negative_elements.extend(['ornate details', 'carved patterns', 'traditional elements'])
        elif style == 'traditional':
            negative_elements.extend(['minimalist', 'industrial elements', 'modern starkness'])
        elif style == 'scandinavian':
            negative_elements.extend(['dark colors', 'heavy materials', 'ornate details'])
        elif style == 'bohemian':
            negative_elements.extend(['minimalist', 'monochromatic', 'stiff arrangements'])
        elif style == 'industrial':
            negative_elements.extend(['polished surfaces', 'delicate details', 'soft colors'])
        elif style == 'coastal':
            negative_elements.extend(['dark heavy materials', 'formal elements', 'urban industrial'])
        
        return ', '.join(negative_elements)
