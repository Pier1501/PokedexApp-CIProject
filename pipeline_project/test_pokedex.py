from jsonschema import validate
import json
import pytest
import os
from pokedex import get_pokemon_data, get_pokemon_types
from pokedex import calculate_type_effectiveness

current_directory = os.getcwd()
typing_json_path = os.path.join(current_directory, "typing.json")


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



# Testing json schema of the pokemon
def validate_wrapper(schema, pokemon_name):
    instance = get_pokemon_data(pokemon_name)
    try:
        validate(instance = instance, schema = schema_pokemon_data)
        return True
    except Exception as e:
        print(f"Schema validation error: {e}")
        return False

# Testing pokemon types
def test_charizard_types():
    charizard_data = {
        "types": ["fire", "flying"] 
    }
    assert get_pokemon_types(charizard_data) == ["fire", "flying"]

def test_tyranitar_types():
    tyranitar_data = {
        "types": ["rock", "dark"] 
    }
    assert get_pokemon_types(tyranitar_data) == ["rock", "dark"]


def test_torchic_not_water():
    torchic_data = get_pokemon_data('torchic')
    types = torchic_data["types"]
    assert "water" not in types, f"Expected Torchic to not be Water type, but got {types}"

def test_pikachu_not_ground():
    pikachu_data = get_pokemon_data('pikachu')
    types = pikachu_data["types"]
    assert "ground" not in types, f"Expected Pikachu to not be Ground type, but got {types}"

# Testing pokemon weaknesses table
def test_charizard_effectiveness():
    with open(typing_json_path, 'r') as typing_file:
        type_chart = json.load(typing_file)
   
    effectiveness = calculate_type_effectiveness(["fire", "flying"], type_chart)
    assert effectiveness["water"] == 2.0, "Charizard should be weak to water"
    assert effectiveness["rock"] == 4.0, "Charizard should be very weak to rock"
    assert effectiveness["ground"] == 0.0, "Charizard should be immune to ground"


def test_scizor_effectiveness():
    with open(typing_json_path, 'r') as typing_file:
        type_chart = json.load(typing_file)
   
    effectiveness = calculate_type_effectiveness(["bug", "steel"], type_chart)
    assert effectiveness["fire"] == 4.0, "Scizor should be very weak to fire"
    assert effectiveness["ground"] == 1.0, "Scizor should be weak to ground"
    assert effectiveness["grass"] == 0.25, "Scizor should be weak to rock"


#  Schema for validating types weaknesses file (JSON SCHEMA VALIDATION NOT IMPLEMENTED)
typing_chart_schema = {
  "type": "object",
  "additionalProperties": False,
  "required": [
    "normal", "fire", "water", "electric", "grass", "ice",
    "fighting", "poison", "ground", "flying", "psychic",
    "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"
  ],
  "propertyNames": {
    "enum": [
      "normal", "fire", "water", "electric", "grass", "ice",
      "fighting", "poison", "ground", "flying", "psychic",
      "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"
    ]
  },
  "properties": {
    "normal": { "$ref": "#/$defs/typeEffectiveness" },
    "fire": { "$ref": "#/$defs/typeEffectiveness" },
    "water": { "$ref": "#/$defs/typeEffectiveness" },
    "electric": { "$ref": "#/$defs/typeEffectiveness" },
    "grass": { "$ref": "#/$defs/typeEffectiveness" },
    "ice": { "$ref": "#/$defs/typeEffectiveness" },
    "fighting": { "$ref": "#/$defs/typeEffectiveness" },
    "poison": { "$ref": "#/$defs/typeEffectiveness" },
    "ground": { "$ref": "#/$defs/typeEffectiveness" },
    "flying": { "$ref": "#/$defs/typeEffectiveness" },
    "psychic": { "$ref": "#/$defs/typeEffectiveness" },
    "bug": { "$ref": "#/$defs/typeEffectiveness" },
    "rock": { "$ref": "#/$defs/typeEffectiveness" },
    "ghost": { "$ref": "#/$defs/typeEffectiveness" },
    "dragon": { "$ref": "#/$defs/typeEffectiveness" },
    "dark": { "$ref": "#/$defs/typeEffectiveness" },
    "steel": { "$ref": "#/$defs/typeEffectiveness" },
    "fairy": { "$ref": "#/$defs/typeEffectiveness" }
  },
  "$defs": {
    "typeEffectiveness": {
      "type": "object",
      "additionalProperties": False,
      "required": [
        "normal", "fire", "water", "electric", "grass", "ice",
        "fighting", "poison", "ground", "flying", "psychic",
        "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"
      ],
      "properties": {
        "normal": { "$ref": "#/$defs/multiplier" },
        "fire": { "$ref": "#/$defs/multiplier" },
        "water": { "$ref": "#/$defs/multiplier" },
        "electric": { "$ref": "#/$defs/multiplier" },
        "grass": { "$ref": "#/$defs/multiplier" },
        "ice": { "$ref": "#/$defs/multiplier" },
        "fighting": { "$ref": "#/$defs/multiplier" },
        "poison": { "$ref": "#/$defs/multiplier" },
        "ground": { "$ref": "#/$defs/multiplier" },
        "flying": { "$ref": "#/$defs/multiplier" },
        "psychic": { "$ref": "#/$defs/multiplier" },
        "bug": { "$ref": "#/$defs/multiplier" },
        "rock": { "$ref": "#/$defs/multiplier" },
        "ghost": { "$ref": "#/$defs/multiplier" },
        "dragon": { "$ref": "#/$defs/multiplier" },
        "dark": { "$ref": "#/$defs/multiplier" },
        "steel": { "$ref": "#/$defs/multiplier" },
        "fairy": { "$ref": "#/$defs/multiplier" }
      }
    },
    "multiplier": {
      "type": "number",
      "enum": [0, 0.5, 1, 2],
      "description": "Damage multiplier for type effectiveness (0 = immune, 0.5 = not very effective, 1 = normal, 2 = super effective)"
    }
  }
}

def validate_typing_chart(typing_chart_schema, typing_chart_path = typing_json_path):
    with open(typing_chart_path, 'r') as typing_file:
        typing_chart_instance = json.load(typing_file)
    try:
        validate(instance = typing_chart_instance, schema = typing_chart_schema)
        return True
    except Exception as e:
        print(f"Schema validation error: {e}")
        return False


# Snapshot testing

def test_pokemon_data_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'pipeline_project/snapshots'

    snapshot.assert_match(get_pokemon_data('charizard'), "pokemon_data_snapshot.txt")

'''
def test_effectiveness_table_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'pipeline_project/snapshots'

    test_cases = [
        {
            "pokemon": "Charizard",
            "types": ["fire", "flying"]
        },
        {
            "pokemon": "Bulbasaur",
            "types": ["grass", "poison"]
        },
        {
            "pokemon": "Gengar",
            "types": ["ghost", "poison"]
        },
        {
            "pokemon": "Tyranitar",
            "types": ["rock", "dark"]
        }
    ]

    with open(typing_json_path, 'r') as typing_file:
        type_chart = json.load(typing_file)
   
    results = {}
    for case in test_cases:
        effectiveness = calculate_type_effectiveness(case["types"], type_chart)
       
        # Format results in a readable way
        categorized = {
            "pokemon": case["pokemon"],
            "types": case["types"],
            "effectiveness": {
                "immune": [],
                "quarter": [],
                "half": [],
                "neutral": [],
                "double": [],
                "quadruple": []
            }
        }
       
        for type_name, multiplier in effectiveness.items():
            if multiplier == 0:
                categorized["effectiveness"]["immune"].append(type_name)
            elif multiplier == 0.25:
                categorized["effectiveness"]["quarter"].append(type_name)
            elif multiplier == 0.5:
                categorized["effectiveness"]["half"].append(type_name)
            elif multiplier == 1:
                categorized["effectiveness"]["neutral"].append(type_name)
            elif multiplier == 2:
                categorized["effectiveness"]["double"].append(type_name)
            elif multiplier == 4:
                categorized["effectiveness"]["quadruple"].append(type_name)
       
        results[case["pokemon"]] = categorized
   
    snapshot.assert_match(results, "effectiveness_table_snapshot.txt")
'''