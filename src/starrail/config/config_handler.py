import os
import json
from ..exceptions.sr_exceptions import *

class ConfigHandler:
    def __init__(self):
        self.starrail_config = os.path.join(os.path.abspath(os.path.dirname(__file__)), "game_config.json")

    def read_game_config(self):
        with open(self.starrail_config, "r") as f:
            config = json.load(f)
        return config if config else None
    
    def get_game_path(self):
        try:
            return self.read_game_config()["game-abspath"]
        except:
            return None
    
    def set_game_path(self, new_path):
        config = self.read_game_config()
        if config != None:
            config['game-abspath'] = new_path
            with open(self.starrail_config, 'w') as wf:
                json.dump(config, wf, indent=4)
            

if __name__ == "__main__":
    c = ConfigHandler()
    print(c.get_game_path())