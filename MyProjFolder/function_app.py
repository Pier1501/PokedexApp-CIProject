import azure.functions as func
import json
import logging
import os 
import requests as rq


app = func.FunctionApp()

def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    try:
        response = rq.get(url)
        response.raise_for_status() 
        pokemon_data = response.json()
        pokemon_info = {
            "name": pokemon_data["name"].capitalize(),
            "id": pokemon_data["id"],
            "height": pokemon_data["height"] / 10,
            "weight": pokemon_data["weight"] / 10,
            "types": [t["type"]["name"] for t in pokemon_data["types"]],
            "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]]
        }
        return pokemon_info
    except rq.exceptions.RequestException as e:
        return None

def calculate_type_effectiveness(pokemon_types, type_chart):
    effectiveness = {
        attack_type: 1.0 for attack_type in type_chart.keys()
    }
    
    for attack_type in type_chart:
        for defender_type in pokemon_types:
            effectiveness[attack_type] *= type_chart[attack_type][defender_type]
    
    return effectiveness

@app.route(route="Pokedex", auth_level=func.AuthLevel.ANONYMOUS)
def Pokedex(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get the pokemon name from query parameter
        pokemon_name = req.params.get('pokemon')
        
        # Load type chart from the included json file
        with open('typing.json', 'r') as f:
            type_chart = json.load(f)

        if not pokemon_name:
            return func.HttpResponse(
                json.dumps({"error": "Please provide a Pokemon name using the 'pokemon' query parameter"}),
                mimetype="application/json",
                status_code=400
            )

        # Get Pokemon data from PokeAPI
        pokemon_data = get_pokemon_data(pokemon_name)
        
        if not pokemon_data:
            return func.HttpResponse(
                json.dumps({"error": f"Could not find Pokemon: {pokemon_name}"}),
                mimetype="application/json",
                status_code=404
            )

        # Calculate type effectiveness
        effectiveness = calculate_type_effectiveness(pokemon_data["types"], type_chart)
        
        # Organize effectiveness data
        effectiveness_categories = {
            "immune": [],
            "quarter": [],
            "half": [],
            "neutral": [],
            "double": [],
            "quadruple": []
        }
        
        for type_name, multiplier in effectiveness.items():
            if multiplier == 0:
                effectiveness_categories["immune"].append(type_name)
            elif multiplier == 0.25:
                effectiveness_categories["quarter"].append(type_name)
            elif multiplier == 0.5:
                effectiveness_categories["half"].append(type_name)
            elif multiplier == 1:
                effectiveness_categories["neutral"].append(type_name)
            elif multiplier == 2:
                effectiveness_categories["double"].append(type_name)
            elif multiplier == 4:
                effectiveness_categories["quadruple"].append(type_name)

        # Prepare response
        response_data = {
            "pokemon_info": pokemon_data,
            "type_effectiveness": effectiveness_categories
        }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )