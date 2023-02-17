from Planet import Planet

class System:

    def __init__(self, id : int, name : str, star_class : str, dictionary : dict):
        self.id = id
        self.name = name
        self.planets = []
        self.token = self.name.lower().replace(" ","_")
        self.star_class = star_class
        self.dictionary = dictionary
