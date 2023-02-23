import re
from Planet import Planet
from System import System
from Species import Species
from Country import Country
import logging

class Save:
    re_planet = R"[0-9]+={\n\t\t\tname={"
    re_system = R"[0-9]+={\n\t\tcoordinate={"
    re_country = R"[0-9]+={\n\t\tflag={"
    re_species = R"[0-9]+={\n\t\t(?:.*\n\t\t){0,1}name_list="

    def __init__(self, text):
        self.text = text
        self.generated_species = None

    def get_save_attribute(self, attribute):
        result = re.search(f"{attribute}=(.+)\n",self.text).groups()[0]
        result = result.replace("\"","")
        return result

    def get_save_name(self):
        return self.get_save_attribute("name")
    
    def get_save_date(self):
        return self.get_save_attribute("date")

    def get_starts(self, re_template, start=0, end=-1):
        if(end<=0):
            end = len(self.text)
        result = re.findall(re_template, self.text[start:end])
        return result

    def get_dictionary_from_entries(self, entries):
        dictionary = {}
        for dictionary_entry in entries:
            dictionary_entry = (dictionary_entry[0].replace("\t",""),dictionary_entry[1])
            dictionary[dictionary_entry[0]] = dictionary_entry[1].replace("\"","")
        return dictionary

    def get_planet_dictionaries(self):
        planet_finish_text = "auto_slots_taken"
        result = []
        start_planets = self.text.find("\nplanets={\n")
        end_planets = self.text.find("\ncountry={\n")
        shorter_text = self.text[:end_planets]
        for planet_start in self.get_starts(self.re_planet,start_planets,end_planets):
            start = shorter_text.find(planet_start)
            shorter_text = shorter_text[start:]
            end = shorter_text.find(planet_finish_text)
            planet_text = shorter_text[:end]

            dictionary_entries = re.findall("\n\t\t\t(.+)=(.+)",planet_text)

            id = planet_text[:planet_text.find("=")]
            name = re.findall("key=\"(.+)\"",planet_text)[0]
            dictionary = self.get_dictionary_from_entries(dictionary_entries)
            dictionary["id"] = id
            dictionary["name"] = name
            result.append(dictionary)
        return result
            

    def get_planets(self):
        logging.info("Getting planets")
        result = []
        for planet_dictionary in self.get_planet_dictionaries():
            planet = Planet(planet_dictionary["id"],planet_dictionary["name"],planet_dictionary["planet_class"],planet_dictionary)
            result.append(planet)
        logging.progress("25%")
        logging.info("Got planets")
        return result            

    def set_planet_moons(self, planet_dictionary : list[Planet]):
        for planet_id in planet_dictionary:
            planet = planet_dictionary[planet_id]
            if("moon_of" in planet.dictionary):
                planet.is_moon = True
                parent_id = planet.dictionary["moon_of"]
                parent = planet_dictionary[parent_id]
                parent.moons.append(planet)


    def get_system_dictionaries(self):
        system_finish_text = "sector"
        system_starting_point = self.text.find("galactic_object={")
        system_ending_point = self.text.find("\nambient_object={")
        result = []
        shorter_text = self.text[:system_ending_point]
        for system_start in self.get_starts(self.re_system,system_starting_point,system_ending_point):
            start = shorter_text.find(system_start)
            shorter_text = shorter_text[start:]
            end = shorter_text.find(system_finish_text)
            system_text = shorter_text[:end]

            dictionary_entries = re.findall("\n\t\t(.+)=(.+)",system_text)
            id = system_text[:system_text.find("=")]
            name = re.findall("key=\"(.+)\"",system_text)[0]
            dictionary = self.get_dictionary_from_entries(dictionary_entries)
            dictionary["id"] = id
            dictionary["name"] = name

            planets = re.findall("\tplanet=([0-9]+)",system_text)
            dictionary["planet"] = []
            for planet_id in planets:
                dictionary["planet"].append(planet_id)

            hyperlanes = re.findall("\tto=([0-9]+)",system_text)
            dictionary["hyperlane"] = []
            for hyperlane_id in hyperlanes:
                dictionary["hyperlane"].append(hyperlane_id)

            result.append(dictionary)
        return result

    def get_systems(self):
        logging.info("Getting systems")
        result = []

        planets = self.get_planets()
        planet_dictionary = {}
        for planet in planets:
            planet_dictionary[planet.id] = planet

        self.set_planet_moons(planet_dictionary)

        for system_dictionary in self.get_system_dictionaries():
            system = System(system_dictionary["id"],system_dictionary["name"],system_dictionary["star_class"],system_dictionary)
            for planet_id in system_dictionary["planet"]:
                system.planets.append(planet_dictionary[planet_id])
            result.append(system)

        logging.progress("50%")
        logging.info("Got systems")
        return result

    def get_species_dictionaries(self):
        species_finish_text = "gender"
        species_starting_point = self.text.find("species_db={")
        species_ending_point = self.text.find("spy_networks={")
        result = []
        shorter_text = self.text[:species_ending_point]
        for species_start in self.get_starts(self.re_species,species_starting_point,species_ending_point):
            start = shorter_text.find(species_start)
            shorter_text = shorter_text[start:]
            end = shorter_text.find(species_finish_text)
            species_text = shorter_text[:end]

            dictionary_entries = re.findall("\n\t\t(.+)=(.+)",species_text)
            id = species_text[:species_text.find("=")]
            name = re.search("key=\"(.+)\"",species_text[species_text.find("name="):]).groups()[0]
            plural = re.search("key=\"(.+)\"",species_text[species_text.find("plural="):]).groups()[0]
            adjective = re.search("key=\"(.+)\"",species_text[species_text.find("adjective="):]).groups()[0]
            if(adjective == "%ADJECTIVE%"):
                adjective = re.search("key=\"(.+)\"",species_text[species_text.find("value={\n\t\t\t\t\t"):]).groups()[0]
            dictionary = self.get_dictionary_from_entries(dictionary_entries)
            dictionary["id"] = id
            dictionary["name"] = name
            dictionary["plural"] = plural
            dictionary["adjective"] = adjective

            result.append(dictionary)
        return result

    def get_species(self):
        logging.info("Getting species")
        if(self.generated_species != None):
            return self.generated_species
        else:
            result = []

            for species_dictionary in self.get_species_dictionaries():
                species = Species(species_dictionary)
                result.append(species)
            
            logging.info("Got species")
            self.generated_species = result
            return result

    def get_country_dictionaries(self):
        country_finish_text = "sector"
        country_starting_point = self.text.find("country={")
        country_ending_point = self.text.find("\first_contact={")
        result = []
        shorter_text = self.text[:country_ending_point]
        for country_start in self.get_starts(self.re_country,country_starting_point,country_ending_point):
            start = shorter_text.find(country_start)
            shorter_text = shorter_text[start:]
            end = shorter_text.find(country_finish_text)
            country_text = shorter_text[:end]

            dictionary_entries = re.findall("\n\t\t(.+)=(.+)",country_text)
            id = country_text[:country_text.find("=")]
            name = re.findall("key=\"(.+)\"",country_text)[0]
            adjective_command_list = ["%ADJ%","%ADJECTIVE%"]
            if(name in adjective_command_list):
                name_segment = country_text[country_text.find("name="):country_text.find("adjective=")]
                name_values = re.findall("value={\n\t+key=\"(.+)\"",name_segment)
                name = " ".join(name_values)
            
            #also add country adjective if the names works

            dictionary = self.get_dictionary_from_entries(dictionary_entries)
            dictionary["id"] = id
            dictionary["name"] = name

            result.append(dictionary)
        return result

    def get_countries(self):
        logging.info("Getting countries")
        result = []

        species = self.get_species()
        species_id_dictionary = {}
        for one_species in species:
            species_id_dictionary[int(one_species.dictionary["id"])] = one_species

        for country_dictionary in self.get_country_dictionaries():
            founder_species_id = int(country_dictionary["founder_species_ref"])
            country = Country(species_id_dictionary[founder_species_id],country_dictionary)

            result.append(country)
        
        logging.info("Got countries")
        return result