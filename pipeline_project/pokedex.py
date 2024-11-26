import requests as rq
import json

url_pokeapi = "https://pokeapi.co/api/v2/pokemon/"

def get_pokemon_data(pokemon_name):
    url = url_pokeapi + pokemon_name.lower()
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
        return f"Error: {str(e)}"

def get_pokemon_types(pokemon_data):
    if isinstance(pokemon_data, dict) and "types" in pokemon_data:
        if isinstance(pokemon_data["types"], list):
            return pokemon_data["types"] 
        return [type_info["type"]["name"].lower() for type_info in pokemon_data["types"]]
    return []

def calculate_type_effectiveness(pokemon_types, type_chart):
    effectiveness = {
        attack_type: 1.0 for attack_type in type_chart.keys()
    }
    
    for attack_type in type_chart:
        for defender_type in pokemon_types:
            effectiveness[attack_type] *= type_chart[attack_type][defender_type]
    
    return effectiveness

def print_effectiveness_table(pokemon_name, effectiveness):
    print(f"\nDefensive Type Chart for {pokemon_name}:")
    print("-" * 40)

    immune = []<
    quarter = []
    half = []
    neutral = []
    double = []
    quadruple = []
    
    for type_name, multiplier in effectiveness.items():
        if multiplier == 0:
            immune.append(type_name)
        elif multiplier == 0.25:
            quarter.append(type_name)
        elif multiplier == 0.5:
            half.append(type_name)
        elif multiplier == 1:
            neutral.append(type_name)
        elif multiplier == 2:
            double.append(type_name)
        elif multiplier == 4:
            quadruple.append(type_name)
    
    if immune:
        print("Immune to (0x):", ", ".join(t.capitalize() for t in immune))
    if quarter:
        print("Very Resistant (0.25x):", ", ".join(t.capitalize() for t in quarter))
    if half:
        print("Resistant (0.5x):", ", ".join(t.capitalize() for t in half))
    if double:
        print("Weak (2x):", ", ".join(t.capitalize() for t in double))
    if quadruple:
        print("Very Weak (4x):", ", ".join(t.capitalize() for t in quadruple))

def main():
    try:
        with open("/workspaces/2023-25.BD.UFS14/pipeline_project/types.json", "r") as f:
            type_chart = json.load(f)
    except FileNotFoundError:
        print("Error: types.json not found in current directory")
        return
    
    pokemon_name = input("Enter the name of a Pokemon: ").lower()
    
    try:
        pokemon_data = get_pokemon_data(pokemon_name)
        if not pokemon_data:
            print(f"Could not find Pokemon: {pokemon_name}")
            return
        
        pokemon_types = get_pokemon_types(pokemon_data)
        print(f"\n{pokemon_name.capitalize()} is a {'/'.join(t.capitalize() for t in pokemon_types)} type Pokemon")
        
        effectiveness = calculate_type_effectiveness(pokemon_types, type_chart)
        print_effectiveness_table(pokemon_name.capitalize(), effectiveness)
        
    except Exception as e:
        print(f"An error occurred in the main: {str(e)}")

if __name__ == "__main__":
    main()