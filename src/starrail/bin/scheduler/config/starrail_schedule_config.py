from starrail.utils.utils import *
from starrail.utils.json_handler import JSONConfigHandler

class StarRailScheduleConfig(JSONConfigHandler):
    def __init__(self):
        __scheduler_config =  os.path.join(os.path.abspath(os.path.dirname(__file__)), "schedules.json")
        super().__init__(__scheduler_config, list)
    
    def load_schedule(self):
        return self.LOAD_CONFIG()
    
    def save_schedule(self, payload):
        ret = self.SAVE_CONFIG(payload)