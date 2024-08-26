import os
import json
from abc import ABC
from starrail.exceptions.exceptions import StarRailBaseException

class JSONConfigHandler(ABC):
    def __init__(self, config_abs_path, config_type=dict):
        self.config_file = config_abs_path
        self.config_type = config_type

    def LOAD_CONFIG(self):
        try:
            with open(self.config_file, "r") as rf:
                config = json.load(rf)
                return config
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            self.SAVE_CONFIG([] if self.config_type == list else dict())
            return None

    def SAVE_CONFIG(self, json_payload) -> bool:
        try:
            with open(self.config_file, "w") as wf:
                json.dump(json_payload, wf, indent=4)
        except Exception as ex:
            StarRailBaseException(f"Config file '{self.config_file}' cannot be created due to an unknown error ({ex}).")
        return True

    def DELETE_CONFIG(self):
        if not self.CONFIG_EXISTS():
            return False
        try:
            os.remove(self.config_file)
        except:
            return False
        return True

    def CONFIG_EXISTS(self):
        return os.path.isfile(self.config_file)
    
    def VALIDATE_CONFIG(self):
        ...