from jsonschema import validate
import json

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