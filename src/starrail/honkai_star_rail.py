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
import sys
import time
import psutil
import subprocess

from .constants import *
from ._exceptions._exceptions import *

class HonkaiStarRail:
    """
    Honkai Star Rail game instance.
    """
    def __init__(self, game_path, process=None):
        self.process        = process
        self.is_focused     = False
        self.game_path      = self.__verify_path(game_path)
    
    def run(self) -> bool:
        subprocess.Popen(self.game_path, shell=True)
        
        TIMEOUT = 30
        starting_time = time.time()
        while time.time() - starting_time < TIMEOUT:
            for p in psutil.process_iter():
                if p.name() == GAME_DEFAULT:
                    try:
                        self.process = psutil.Process(p.pid)
                        return True
                    except Exception as ex:
                        print(ex.__traceback__)
            time.sleep(1)
        return False
    
    
    def terminate(self, force_terminate=False) -> bool:
        if force_terminate:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == GAME_DEFAULT:
                    proc.terminate()
                    return True
            return False
        
        if self.process.is_running:
            self.process.terminate()
            self.process.wait()
            return True
        return False

    
    def restart(self) -> bool:
        return self.terminate() and self.run()

    
    def is_running(self) -> bool:
        return self.process.is_running
    
    
    # ==================================================
    # ============== | Helper Functions | ==============
    # ==================================================
    
    def __verify_path(self, game_path):
        """
        Verify the absolute path to the game Honkai Star Rail.
        :param game_path: new absolute path to be set
        :return: the verified game path
        :rtype: str
        """
        if game_path == None or not os.path.exists(game_path):
            raise StarRailGameNotFoundException("M0")
        elif os.path.basename(game_path) != GAME_DEFAULT:
            raise StarRailGameNotFoundException("M1")
        return game_path
    
    
    def __get_pid_by_name(self, name):
        
        for process in psutil.process_iter(['pid', 'name']):
            try:
                process_info = process.as_dict(attrs=['pid', 'name'])
            except psutil.NoSuchProcess:
                pass
            else:
                if process_info['name'] == name:
                    return process_info['pid']
        return None

    