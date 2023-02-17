from zipfile import ZipFile
import os
import re

class SaveLoader():
    
    def get_configuration_savegame_path(self):
        result = ""
        with open("configuration.txt","r",encoding="utf-8") as configuration:
            result = configuration.read()
            result = re.findall("SaveGame = (.+)",result)[0].replace("\"","")
        return result

    def get_configuration_documents_path(self):
        result = ""
        with open("configuration.txt","r",encoding="utf-8") as configuration:
            result = configuration.read()
            result = re.findall("StellarisDocDirectory = (.+)",result)[0].replace("\"","")
        return result

    def get_gamestate_text(self):
        result = ""
        with ZipFile(self.get_configuration_savegame_path(),"r") as zipFile:
            zipFile.extract("gamestate",path=os.path.join(os.getcwd()))
        with open("gamestate","r",encoding="utf-8") as file:
            result = file.read()
        return result