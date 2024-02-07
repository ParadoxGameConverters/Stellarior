import re
from Planet import Planet
from System import System
from Country import Country
from Species import Species
import os
import shutil
import logging

class Mod:

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

    def __init__(self, save_name : str , systems : list[System], countries : list[Country], species : list[Species]):
        self.mod_name = "Converted - " + save_name
        self.systems = systems
        self.countries = countries
        self.species = species

        self.mod_folder_name = save_name.replace(" ","_").lower()
        self.mod_folder = os.path.join("output",self.mod_folder_name)

        self.map_file_start = "static_galaxy_scenario = {\n"+f"name = \"{save_name}\""+"""
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

    def get_prescripted_empire(self, empire : Country):
        result = f"{empire.token} = {{\n"
        result += f"name = \"{empire.name}\"\n"

        result += """adjective = "PRESCRIPTED_adjective_tzynn"
	spawn_enabled = yes # yes / no / always

	ship_prefix = "PRESCRIPTED_ship_prefix_tzynn"

        """
        #temporary
        result += """	species = {
		class = "REP"
		portrait = "rep9"
		name = "PRESCRIPTED_species_name_tzynn"
		plural = "PRESCRIPTED_species_plural_tzynn"
		adjective = "PRESCRIPTED_species_adjective_tzynn"
		name_list = "REP1"
		trait = "trait_strong"
		trait = "trait_resilient"
		trait = "trait_rapid_breeders"
		trait = "trait_decadent"
		trait = "trait_quarrelsome"
	}
        """

        result += """room = "personality_slaving_despots_room"

	authority = "auth_imperial"
	civics = { "civic_police_state" "civic_slaver_guilds" }
	government = gov_star_empire
	origin = "origin_default"

	ethic = "ethic_authoritarian"
	ethic = "ethic_fanatic_militarist"

	planet_name = "PRESCRIPTED_planet_name_tzynn"
	planet_class = "pc_desert"
	system_name = "PRESCRIPTED_system_name_tzynn"

	graphical_culture = "reptilian_01"
	city_graphical_culture = "reptilian_01"

	empire_flag = {
		icon= {
			category = "pointy"
			file = "flag_pointy_2.dds"
		}
		background= {
			category = "backgrounds"
			file = "v.dds"
		}
		colors={
			"red"
			"black"
			"null"
			"null"
		}
	}

	ruler = {
		name = "PRESCRIPTED_ruler_name_tzynn"
		gender = male
		portrait = "rep9"
		texture = 1
		clothes = 4
		leader_class = ruler
	}
}

        """
    
        return result

    def create_path_if_doesnt_exist(self, path):
        if(not os.path.exists(path)):
            os.makedirs(path)     

    def write_prescripted_countries(self):
        prescripted_countries_folder_path = os.path.join(self.mod_folder,"prescripted_countries")
        prescripted_countries_path = os.path.join(prescripted_countries_folder_path,"98_prescripted_countries.txt")

        self.create_path_if_doesnt_exist(prescripted_countries_folder_path)

        with open(prescripted_countries_path,"w",encoding="utf-8") as file:
            file.write("")
        with open(prescripted_countries_path, "a", encoding="utf-8") as file:
            for empire in self.countries:
                file.write(self.get_prescripted_empire(empire))
        

    def write_initializers(self):
        initializers_folder_path = os.path.join(self.mod_folder,"common\solar_system_initializers")
        initializers_path = os.path.join(initializers_folder_path,"init_initializers.txt")

        self.create_path_if_doesnt_exist(initializers_folder_path)

        with open(initializers_path,"w",encoding="utf-8") as file:
            file.write(self.system_file_start)
        for system in self.systems:
            init = self.get_system_initializer(system)
            with open(initializers_path,"a",encoding="utf-8") as file:
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
        map_folder_path = os.path.join(self.mod_folder,"map\setup_scenarios")
        map_path = os.path.join(map_folder_path,"mega.txt")
        self.create_path_if_doesnt_exist(map_folder_path)
        with open(map_path,"w",encoding="utf-8") as file:
            file.write(result)

    def copy_blank_mod(self):
        blank_mod_path = "blankMod"
        if(os.path.exists(self.mod_folder)):
            shutil.rmtree(self.mod_folder)
        shutil.copytree(blank_mod_path,self.mod_folder)

    def create_descriptor_file(self):
        template = f"""version="3"
tags={{
	"Balance"
}}
name="{self.mod_name}"
supported_version="3.3.4"
        """
        with(open(os.path.join(self.mod_folder,"descriptor.mod"),"w",encoding="utf-8")) as descriptor:
            descriptor.write(template)
    
    def create_outside_descriptor_file(self):
        template = f"""version="3"
tags={{
	"Balance"
}}
name="{self.mod_name}"
supported_version="3.3.4"
path="mod/{self.mod_folder_name}"
        """

        with(open(os.path.join("output",self.mod_folder_name+".mod"),"w",encoding="utf-8")) as descriptor:
            descriptor.write(template)

    def create_mod(self):
        logging.info("Initializing files")
        logging.progress("51%")
        self.copy_blank_mod()
        self.create_descriptor_file()
        self.create_outside_descriptor_file()
        logging.progress("55%")
        logging.info("Writing system initializers")
        self.write_initializers()
        logging.progress("75%")
        logging.info("Writing prescripted empires")
        self.write_prescripted_countries()
        logging.progress("82%")
        logging.info("Writing maps")
        self.write_map()
        logging.progress("99%")