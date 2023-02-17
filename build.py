import shutil
import os

if(__name__ == "__main__"):
    if(not os.path.exists("Release/blankMod")):
        shutil.copytree("Stellarior/Data_Files/blankMod/output","Release/blankMod")
    if(not os.path.exists("Release/Configuration")):
        shutil.copytree("Stellarior/Data_Files/Configuration","Release/Configuration")