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
    

def test_get_pokemon_types_success():
    charizard_data = {
        "types": [
            {"type": {"name": "FIRE"}},
            {"type": {"name": "FLYING"}}
        ]
    }
    assert get_pokemon_types(charizard_data) == ["fire", "flying"]
    
    gyarados_data = {
        "types": [
            {"type": {"name": "WATER"}},
            {"type": {"name": "FLYING"}}
        ]
    }
    assert get_pokemon_types(gyarados_data) == ["water", "flying"]

def test_get_pokemon_types_error(pokemon_name = 'Torchic'):
    test_data = get_pokemon_data(pokemon_name)
    test_types = get_pokemon_types(test_data)

    assert "fire" in test_types, f"Expected {pokemon_name} to be Fire type, but got {test_types}"

    torchic_wrong_data = {
        "types": [
            {"type": {"name": "GRASS"}}
        ]
    }
    with pytest.raises(KeyError):
        get_pokemon_types(torchic_wrong_data)

    with pytest.raises(TypeError):
        get_pokemon_types(None)




