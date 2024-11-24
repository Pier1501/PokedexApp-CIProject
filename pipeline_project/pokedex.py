import requests
import json

def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def get_pokemon_types(pokemon_data):
    return [type_info["type"]["name"].lower() for type_info in pokemon_data["types"]]

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

    immune = []
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
        with open("types.json", "r") as f:
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
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()