import requests

def get_stats(name):
    poke_url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    poke_response = requests.get(poke_url)
    
    if poke_response.status_code == 200:
        data = poke_response.json()
        stat_dict = {}
        for i in data['stats']:
            stat_dict[i["stat"]["name"]] = i["base_stat"]

        return stat_dict
    
def get_pokemon(name):
    poke_url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    poke_response = requests.get(poke_url)
    
    if poke_response.status_code == 200:
        data = poke_response.json()
        stat_dict = get_stats(name)
        print(f"Name: {data['name']}")
        print(f"HP: {stat_dict['hp']}")
        print(f"Attack: {stat_dict['attack']}")
        print(f"Defense: {stat_dict['defense']}")
        print(f"Height: {data['height']}")
        print("Types:", ", ".join([t["type"]["name"] for t in data["types"]]))
    else:
        print("Pokémon not found!")

def compare_poke(name1, name2):
    poke1 = get_stats(name1)
    poke2 = get_stats(name2)
    for stat in poke1:
        if poke1[stat] > poke2[stat]:
            print(f'{name1} has a higher {stat} than {name2}')
        elif poke1[stat] < poke2[stat]:
            print(f'{name2} has a higher {stat} than {name1}')
        else:
            print(f'{name1} has the same {stat} as {name2}')


def get_evo_chain(name):
    evo_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    evo_response = requests.get(evo_url)

    if evo_response.status_code == 200:
        data = evo_response.json()
        evo_url = data["evolution_chain"]["url"]
        evo_response = requests.get(evo_url)
        if evo_response.status_code == 200:
            evo_chain_data = evo_response.json()
            names = []
            def walk(chain_node):
                if "species" in chain_node and "name" in chain_node["species"]:
                    names.append(chain_node["species"]["name"])
                for next_node in chain_node.get("evolves_to", []):
                    walk(next_node)
            walk(evo_chain_data["chain"])
            print("Evolution chain:", " → ".join(names))
        else:
            print("Could not fetch evolution chain info.")
        
    else:
        print("Pokémon not found!")

def main():
    print("----- Welcome ----- \n")
    print("1: Search pokemon by name")
    print('2: Compare pokemon')
    print('3: Get pokemon evolution chain\n')
    option = int(input("Please Select an option "))
    if option == 1:
        get_pokemon(input("Input a pokemon: "))
    elif option == 2:
        compare_poke(input("Input a pokemon: "), input("Input a pokemon: "))
    elif option == 3:
        get_evo_chain(input("Input a pokemon: "))
    else:
        print("Invalid input")

main()


