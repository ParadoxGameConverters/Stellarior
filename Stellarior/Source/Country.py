
class Country:

    def __init__(self, primary_species, dictionary):
        self.primary_species = primary_species
        self.dictionary = dictionary

        self.name = dictionary["name"]
        self.adjective = dictionary["adjective"]

        self.token = self.name.replace(" ","_").lower()