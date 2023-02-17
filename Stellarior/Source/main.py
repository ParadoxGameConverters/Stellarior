from Save import Save
from SaveLoader import SaveLoader
from Mod import Mod
import logging

if(__name__ == "__main__"):
    logging.basicConfig(filename="log.txt",filemode="w",format="%(asctime)s [%(levelname)s] %(message)s",level=logging.DEBUG)
    
    def logProgress(self, message, *args, **kwargs):
        if self.isEnabledFor(11):
            self._log(11, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(11, message, *args, **kwargs)

    logging.addLevelName(11,"PROGRESS")
    setattr(logging,"PROGRESS",11)
    setattr(logging.getLoggerClass(),"progress",logProgress)
    setattr(logging,"progress",logToRoot)

    logging.info("Starting conversion!")
    logging.progress("1%")
    try:
        save_loader = SaveLoader()
        save_gamestate_text = save_loader.get_gamestate_text()
        documents_path = save_loader.get_configuration_documents_path()
        save = Save(save_gamestate_text)
        save_name = save.get_save_name()
        logging.info("Found save location")
        logging.progress("5%")
        logging.info("Preparing save information")
        mod = Mod(documents_path,save_name,save.get_systems())
        mod.create_mod()
    except Exception as e:
        logging.exception("Exception occurred")