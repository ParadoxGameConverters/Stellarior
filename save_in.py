import re
from Planet import Planet
from System import System

class Save:
    re_planet = R"[0-9]+={\n\t\t\tname={"
    re_system = R"[0-9]+={\n\t\tcoordinate={"
    planet_finish_text = "auto_slots_taken"
    system_finish_text = "sector"

    def __init__(self, text):
        self.text = text

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
        result = []
        start_planets = self.text.find("\nplanets={\n")
        end_planets = self.text.find("\ncountry={\n")
        shorter_text = self.text[:end_planets]
        for planet_start in self.get_starts(self.re_planet,start_planets,end_planets):
            start = shorter_text.find(planet_start)
            shorter_text = shorter_text[start:]
            end = shorter_text.find(self.planet_finish_text)
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
        print("Getting planets")
        result = []
        for planet_dictionary in self.get_planet_dictionaries():
            planet = Planet(planet_dictionary["id"],planet_dictionary["name"],planet_dictionary["planet_class"],planet_dictionary)
            result.append(planet)
        print("Got planets")
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
        system_starting_point = self.text.find("galactic_object={")
        system_ending_point = self.text.find("\nambient_object={")
        result = []
        shorter_text = self.text[:system_ending_point]
        for system_start in self.get_starts(self.re_system,system_starting_point,system_ending_point):
            start = shorter_text.find(system_start)
            shorter_text = shorter_text[start:]
            end = shorter_text.find(self.system_finish_text)
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
        print("Getting systems")
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

        return result
