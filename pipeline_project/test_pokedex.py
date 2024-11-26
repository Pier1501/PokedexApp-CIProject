from jsonschema import validate
import json
import pytest

from pokedex import get_pokemon_data, get_pokemon_types
from pokedex import calculate_type_effectiveness


schema_pokemon_data = {
    "type": "object",
    "properties": {
                "name": {"type", "string"},
                "id": {"type", "integer"},
                "height": {"type", "number"},
                "weight": {"type", "number"}, 
                "types": {
                    "type": "array",
                    "items": {
                            "type": "string"
                    }
                },
                "abilities": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
    },
    "required": ["name", "id", "height", "weight", "types", "abilities"]
}

def validate_wrapper(schema, pokemon_name):
    instance = get_pokemon_data(pokemon_name)
    try:
        validate(instance = instance, schema = schema_pokemon_data)
        return True
    except Exception as e:
        print(f"Schema validation error: {e}")
        return False
    

def test_charizard_types():
    charizard_data = {
        "types": [
            {"type": {"name": "FIRE"}},
            {"type": {"name": "FLYING"}}
        ]
    }
    assert get_pokemon_types(charizard_data) == ["fire", "flying"]
    
def test_gyarados_types():
    gyarados_data = {
        "types": [
            {"type": {"name": "WATER"}},
            {"type": {"name": "FLYING"}}
        ]
    }
    assert get_pokemon_types(gyarados_data) == ["water", "flying"]

def test_torchic_not_water():
    torchic_data = get_pokemon_data('Torchic')
    test_types = get_pokemon_types(torchic_data)
    assert "water" not in test_types

def test_pikachu_not_ground():
    pikachu_data = get_pokemon_data('Pikachu')
    test_types = get_pokemon_types(pikachu_data)
    assert "ground" not in test_types




