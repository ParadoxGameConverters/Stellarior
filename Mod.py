import re
from Planet import Planet
from System import System

class Mod:

    map_file_start = """static_galaxy_scenario = {
	name = "megacampaign_galaxy"
	priority = 7
	default = no
	num_empires = { min = 0 max = 16 }
	num_empire_default = 5
	fallen_empire_default = 1
	fallen_empire_max = 3
	marauder_empire_default = 1
	marauder_empire_max = 2
	advanced_empire_default = 0
	colonizable_planet_odds = 1.0
	random_hyperlanes = no
	num_wormhole_pairs_default = 0
	crisis_strength = 1.0
	extra_crisis_strength = { 10 25 }
    
    """

    system_file_start = """@base_planet_dist = 30
@base_moon_dist = 15

@capital_size = 20
@moon_capital_size = 13
"""

    system_initializer = """

# {system_name}
{system_token}_system_initializer = {{
	name = "{system_name}"
	class = "{star_class}"
	flags = {{ {system_token} }}

    
    """

    def __init__(self, systems : list[System]):
        self.systems = systems
    
    def get_planet_initalizer_body(self, planet : Planet):
        planet_string = """ = {{"""
        if(not "variables" in planet.dictionary):
            planet_string += "name = \"{planet_name}\""
        planet_string += """class = "{planet_class}"
        size = {planet_size}
        
        """
        if(not planet.is_moon):
            for moon in planet.moons:
                planet_string += "moon"
                planet_string += self.get_planet_initalizer_body(moon).replace("{","{{").replace("}","}}")

        planet_string += "}}"

        return planet_string.format(planet_name=planet.name,planet_class=planet.planet_class,planet_size=planet.dictionary["planet_size"])

    def get_system_initializer(self, system):
        result = self.system_initializer.format(system_name=system.name,system_token=system.token,star_class=system.star_class) #weź to napraw

        for planet in system.planets:
            if(not planet.is_moon):
                planet_string = "planet"

                planet_string += self.get_planet_initalizer_body(planet)
                result += planet_string
        return result

    def write_initializers(self):
        with open("out\common\solar_system_initializers\init_initializers.txt","w",encoding="utf-8") as file:
            file.write(self.system_file_start)
        for system in self.systems:
            init = self.get_system_initializer(system)
            with open("out\common\solar_system_initializers\init_initializers.txt","a",encoding="utf-8") as file:
                file.write(init)
                file.write("}")
    
    def write_map(self):
        result = self.map_file_start

        for system in self.systems:
            x = system.dictionary["x"]
            y = system.dictionary["y"]
            result += f"system = {{ id = \"{system.id}\" name = \"{system.name}\" position = {{ x = {x} y = {y} }} initializer = {system.token}_system_initializer }}\n"
            for connection in system.dictionary["hyperlane"]:
                result += f"add_hyperlane = {{ from = \"{system.id}\" to = \"{connection}\" }}\n"

        result += "}"
        with open("out\map\setup_scenarios\mega.txt","w",encoding="utf-8") as file:
            file.write(result)


    def create_mod(self):
        print("Starting")
        self.write_initializers()
        print("Writing maps")
        self.write_map()