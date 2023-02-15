import save_in
from Mod import Mod

if(__name__ == "__main__"):
    with open("gamestate","r",encoding="utf-8") as file:
        save = save_in.Save(file.read())
        mod = Mod(save.get_systems())
        mod.create_mod()