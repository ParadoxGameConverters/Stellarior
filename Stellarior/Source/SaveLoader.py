from zipfile import ZipFile
import os
import re

class SaveLoader():
    
    def get_configuration_savegame_path(self):
        result = ""
        with open("configuration.txt","r",encoding="utf-8") as configuration:
            result = configuration.read()
            result = re.search("SaveGame = (.+)",result).groups()[0].replace("\"","")
        return result
    
    def get_savegame_archive_name(self):
        savegame_path = self.get_configuration_savegame_path()
        return savegame_path.split("\\")[-1] #might not work for linux? - to be fixed later

    def get_out_mod_name(self):
        result = ""
        with open("configuration.txt","r",encoding="utf-8") as configuration:
            result = configuration.read()
            result = re.search("output_name = (.+)",result).groups()[0].replace("\"","")
            if(result == ""):
                result = self.get_savegame_archive_name()
                result = ".".join(result.split(".")[:-1])
        return result

    def get_configuration_documents_path(self):
        result = ""
        with open("configuration.txt","r",encoding="utf-8") as configuration:
            result = configuration.read()
            result = re.search("StellarisDocDirectory = (.+)",result).groups()[0].replace("\"","")
        return result

    def get_gamestate_text(self):
        result = ""
        with ZipFile(self.get_configuration_savegame_path(),"r") as zipFile:
            zipFile.extract("gamestate",path=os.path.join(os.getcwd()))
        with open("gamestate","r",encoding="utf-8") as file:
            result = file.read()
        return result