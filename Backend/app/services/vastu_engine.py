"""
Module 6: Vastu Engine

This module handles Vastu Shastra analysis for room direction combinations.

Dependencies: Module 1 (Configuration)
"""
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class VastuEngineError(Exception):
    """Raised when Vastu analysis fails."""
    pass


class InvalidDirectionError(VastuEngineError):
    """Raised when direction is invalid."""
    pass


# Vastu Shastra rules and data
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
        "suitable_rooms": ["guest_room", "toilet", " pantry"],
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

ROOM_VASTU_SCORES = {
    "bedroom": {
        "southwest": 100,
        "south": 85,
        "west": 70,
        "northwest": 60,
        "east": 50,
        "north": 40,
        "southeast": 30,
        "northeast": 20
    },
    "living": {
        "northeast": 100,
        "north": 95,
        "east": 90,
        "west": 75,
        "southeast": 60,
        "south": 50,
        "northwest": 70,
        "southwest": 30
    },
    "kitchen": {
        "southeast": 100,
        "south": 80,
        "east": 70,
        "west": 60,
        "northwest": 50,
        "north": 30,
        "northeast": 20,
        "southwest": 10
    },
    "dining": {
        "west": 100,
        "east": 90,
        "north": 80,
        "south": 70,
        "northwest": 75,
        "southeast": 60,
        "northeast": 50,
        "southwest": 40
    },
    "study": {
        "east": 100,
        "north": 95,
        "northeast": 90,
        "west": 80,
        "northwest": 75,
        "south": 60,
        "southeast": 50,
        "southwest": 40
    },
    "bathroom": {
        "northwest": 100,
        "west": 90,
        "south": 70,
        "southwest": 60,
        "southeast": 50,
        "east": 40,
        "north": 30,
        "northeast": 10
    }
}


class VastuEngine:
    """
    Vastu Engine for analyzing room direction compliance.
    
    Implements Vastu Shastra rules for determining the compatibility
    between room types and cardinal directions.
    """
    
    # Expose module-level constants as class attributes for tests
    VASTU_RULES = VASTU_RULES
    ROOM_VASTU_SCORES = ROOM_VASTU_SCORES
    
    def __init__(self):
        self.rules = VASTU_RULES
        self.room_scores = ROOM_VASTU_SCORES
    
    def analyze(
        self, 
        direction: str, 
        room_type: str,
        call_external_api: bool = False
    ) -> Dict:
        """Analyze Vastu compliance for a room direction combination"""
        
        direction = direction.lower().strip()
        room_type = room_type.lower().strip().replace(" ", "_")
        
        # Get base score
        room_scores = self.room_scores.get(room_type, self.room_scores["living"])
        vastu_score = room_scores.get(direction, 50)
        
        # Get direction rules
        direction_rules = self.rules.get(direction, self.rules["north"])
        
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
        
        # Element balance
        element_balance = {
            "dominant_element": direction_rules["element"],
            "ruling_planet": direction_rules["ruling_planet"],
            "balance_status": "balanced" if vastu_score >= 60 else "needs_attention"
        }
        
        return {
            "direction": direction if direction in self.rules else "unknown",
            "vastu_score": vastu_score,
            "suggestions": suggestions,
            "warnings": warnings,
            "direction_rating": direction_rating,
            "element_balance": element_balance
        }
    
    def get_remedies(self, direction: str, room_type: str) -> List[str]:
        """Get Vastu remedies for non-compliant placements"""
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
