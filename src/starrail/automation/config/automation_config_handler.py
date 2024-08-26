from starrail.utils.utils import *
from starrail.utils.json_handler import JSONConfigHandler

class StarRailAutomationConfig:
    def __init__(self):
        self.automation_data_dir =  os.path.join(os.path.abspath(os.path.dirname(__file__)), f"automation-data")
        if not os.path.isdir(self.automation_data_dir):
            os.mkdir(self.automation_data_dir)  
    
    def load_all_automations(self):
        sequence_name_list = os.listdir(self.automation_data_dir)
        
        raw_json_configs = []
        for seq_filename in sequence_name_list:
            AUTOMATION_FILE = os.path.join(self.automation_data_dir, seq_filename)
            config_handler = JSONConfigHandler(AUTOMATION_FILE)
            if config_handler.CONFIG_EXISTS():
                raw_json_config = config_handler.LOAD_CONFIG() # Loads the sequence config file
                raw_json_configs.append(raw_json_config)
        return raw_json_configs

    def load_automation(self, automation_name):
        config_handler = JSONConfigHandler(os.path.join(self.automation_data_dir, f"automation-{automation_name}.json"))
        return config_handler.LOAD_CONFIG()
    
    def save_automation(self, automation_name, payload):
        config_handler = JSONConfigHandler(os.path.join(self.automation_data_dir, f"automation-{automation_name}.json"))
        return config_handler.SAVE_CONFIG(payload)
    
    def delete_automation(self, automation_name):
        config_handler = JSONConfigHandler(os.path.join(self.automation_data_dir, f"automation-{automation_name}.json"))
        if config_handler.CONFIG_EXISTS():
            return config_handler.DELETE_CONFIG()
        return False