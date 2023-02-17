from Save import Save
from SaveLoader import SaveLoader
from Mod import Mod

if(__name__ == "__main__"):
    save_loader = SaveLoader()
    save_gamestate_text = save_loader.get_gamestate_text()
    documents_path = save_loader.get_configuration_documents_path()
    save = Save(save_gamestate_text)
    save_name = save.get_save_name()
    mod = Mod(documents_path,save_name,save.get_systems())
    mod.create_mod()