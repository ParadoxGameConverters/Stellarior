

class Planet:

    def __init__(self, id : int, name : str, planet_class : str, dictionary : dict):
        self.id = id
        self.name = name
        self.planet_class = planet_class
        self.token = self.name.lower().replace(" ","_")

        self.dictionary = dictionary

        self.connections = []
        self.moons = []
        self.is_moon = False