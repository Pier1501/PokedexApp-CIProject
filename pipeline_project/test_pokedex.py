from jsonschema import validate
import json
import pytest

from pokedex import get_pokemon_data, get_pokemon_types
from pokedex import calculate_type_effectiveness

# Schema for validating Pokemon data
schema_pokemon_data = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "id": {"type": "integer"},
        "height": {"type": "number"},
        "weight": {"type": "number"},
        "types": {
            "type": "array",
            "items": {"type": "string"}
        },
        "abilities": {
            "type": "array",
            "items": {"type": "string"}
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
        "types": ["fire", "flying"] 
    }
    assert get_pokemon_types(charizard_data) == ["fire", "flying"]

def test_tyranitar_types():
    tyranitar_data = {
        "types": ["rock", "dark"] 
    }
    assert get_pokemon_types(gyarados_data) == ["rock", "dark"]
    
def test_torchic_not_water():
    torchic_data = get_pokemon_data('torchic')
    types = torchic_data["types"]
    assert "water" not in types, f"Expected Torchic to not be Water type, but got {types}"

def test_pikachu_not_ground():
    pikachu_data = get_pokemon_data('pikachu')
    types = pikachu_data["types"]
    assert "ground" not in types, f"Expected Pikachu to not be Ground type, but got {types}"


