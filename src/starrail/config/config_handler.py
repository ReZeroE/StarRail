# SPDX-License-Identifier: MIT
# MIT License
#
# Copyright (c) 2024 Kevin L.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json
from starrail.constants import *
from starrail.exceptions.exceptions import *
from starrail.utils.json_handler import JSONConfigHandler
from pathlib import Path

# TODO: Config is only loaded the first time when the StarRailConfig is initialized. This is an issue
# when the module is configured in the CLI since the loaded configuration persists in the CLI.

class StarRailConfig(JSONConfigHandler):
    def __init__(self):
        __starrail_config =  os.path.join(os.path.abspath(os.path.dirname(__file__)), "starrail_config.json")
        super().__init__(__starrail_config, dict)
        
        __raw_config: dict
        try:
            __raw_config = self.LOAD_CONFIG()
        except json.JSONDecodeError:
            self.__reset_config()
            __raw_config = self.LOAD_CONFIG()
        
        # Config variables
        self.instance_pid: int  = None
        self.root_path: Path    = None
        self.game_path: Path    = None
        self.disclaimer: bool   = False
        
        # Load config into attributes
        if __raw_config != None:
            try:
                self.instance_pid   = __raw_config["instance"]["pid"]
                self.root_path      = __raw_config["static"]["root_path"]
                self.game_path      = __raw_config["static"]["game_path"]
                self.disclaimer     = __raw_config["static"]["disclaimer"]
                
                if self.root_path != None:
                    self.root_path = Path(self.root_path)
                if self.game_path != None:
                    self.game_path = Path(self.game_path)
                    
            except KeyError:
                self.__reset_config()
        else:
            self.__reset_config()
    
    
    # ==================================================
    # ============== | UTILITY FUNCTIONS | =============
    # ==================================================
    
    def save_current_config(self):
        self.SAVE_CONFIG(
            {
                "instance": {
                    "pid": self.instance_pid
                },
                "static": {
                    "root_path": str(self.root_path),
                    "game_path": str(self.game_path),
                    "disclaimer": self.disclaimer
                }
            }
        )

    def full_configured(self) -> bool:
        return self.path_configured() and self.disclaimer_configured()
    
    def path_configured(self) -> bool:
        if isinstance(self.game_path, str):
            self.game_path = Path(self.game_path)
            
        if isinstance(self.root_path, Path) and isinstance(self.game_path, Path):
            return self.game_path.exists()
        return False
    
    def disclaimer_configured(self) -> bool:
        return self.disclaimer
    
    
    # ==================================================
    # ============== | HELPER FUNCTIONS | ==============
    # ==================================================
    
    def set_path(self, game_path: str):
        self.game_path = Path(game_path)
        self.root_path = Path(os.path.dirname(os.path.dirname(game_path)))
    
    
    def __reset_config(self):
        self.SAVE_CONFIG(
            {
                "instance": {
                    "pid": None
                },
                "static": {
                    "root_path": None,
                    "game_path": None,
                    "disclaimer": False
                }
            }
        )
        self.game_path = None
        self.disclaimer = False


