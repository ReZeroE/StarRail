# SPDX-License-Identifier: MIT
# MIT License
#
# Copyright (c) 2023 Kevin L.
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
from ..constants import *
from .._exceptions._exceptions import *

class ConfigHandler:
    def __init__(self):
        self.__starrail_config = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.json")

    def __read_game_config(self):
        """
        Read config file and return's an JSON object.
        """
        with open(self.__starrail_config, "r") as f:
            config = json.load(f)
        return config
    
    # ======================================================
    # ============== | Game Instance Config | ==============
    # ======================================================
    
    def get_game_instance_pid(self):
        """
        Get the PID for the currently running instance.
        :return: The PID of the running instance. None if no instance is running.
        :rtype: int / NoneType
        """
        try:
            return self.__read_game_config()["game-config"]["pid"]
        except:
            return None
    
    def set_game_instance_pid(self, pid):
        """
        Set the PID for the currently running instance.
        :param pid: The running instance's PID to set.
        """
        config = self.__read_game_config()
        if config != None:
            config["game-config"]['pid'] = int(pid) if pid != None else None
            with open(self.__starrail_config, 'w') as wf:
                json.dump(config, wf, indent=4)
    
    # ========================================================
    # ============== | StarRail Module Config | ==============
    # ========================================================
    def get_disclaimer_status(self):
        """
        Get the disclaimer status for the module.
        :rtype: bool / NoneType
        """
        try:
            return self.__read_game_config()["module-config"]["disclaimer-read"]
        except KeyError:
            return None
        
    def set_disclaimer_status(self, status=True):
        """
        Get the disclaimer status for the module.
        :param status: Whether the disclaimer has been read.
        """
        config = self.__read_game_config()
        if config != None:
            config["module-config"]['disclaimer-read'] = status
            with open(self.__starrail_config, 'w') as wf:
                json.dump(config, wf, indent=4)
    
    def get_game_path(self):
        """
        Get absolute path for the game Honkai Star Rail.
        :return: abspath for the game. None if not found.
        :rtype: str / NoneType
        """
        try:
            game_path = self.__read_game_config()["module-config"]["game-abspath"]
            return game_path
        except KeyError:
            return None
    
    def set_game_path(self, new_path, auto=False):
        """
        Set absolute path for the game Honkai Star Rail.
        
        :param new_path: new absolute path to be set
        :param auto: whether path is found through automated game search
        :raises StarRailGameNotFoundException: if invalid absolute path is provided
        """
        if auto and new_path == None:
            raise StarRailGameNotFoundException("A0")
        elif not os.path.exists(new_path):
            raise StarRailGameNotFoundException("M0")
        elif os.path.basename(new_path) != GAME_DEFAULT:
            raise StarRailGameNotFoundException("M1")
        
        config = self.__read_game_config()
        if config != None:
            config["module-config"]['game-abspath'] = new_path
            with open(self.__starrail_config, 'w') as wf:
                json.dump(config, wf, indent=4)