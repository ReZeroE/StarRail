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
import string
from termcolor import colored
from ..constants import GAME_DEFAULT
from .._exceptions._exceptions import *

class StarRailGameDetector:
    def get_local_drives(self):
        available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        return available_drives
    
    def find_game(self, paths=[], name=GAME_DEFAULT):
        for p in paths:
            if not os.path.exists(p):
                raise StarRailBaseException(f"Path does not exist. [{p}]")
        
        if len(paths) == 0:
            paths = self.get_local_drives()
        
        paths = [f"{path}\\" if path.endswith(":") and len(path) == 2 else path for path in paths]
        
        for drive_path in paths:
            for root, _, files in os.walk(drive_path):
                if name in files:
                    return os.path.join(root, name)
        return None


def check_platform():
    """
    Verifies whether the OS is supported by the package.
    Package starrail only support Windows installations of Honkai Star Rail.
    
    :return: true if running on Windows, false otherwise
    :rtype: bool
    """
    return os.name == "nt"

def print_disclaimer():
    DISCLAIMER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_data", "disclaimer.txt")
    with open(DISCLAIMER_PATH, "r") as rf:
        lines = rf.readlines()
    print("".join(lines) + "\n")
    
def print_path_config_ex():
    DISCLAIMER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_data", "path_config_ex.txt")
    with open(DISCLAIMER_PATH, "r") as rf:
        lines = rf.readlines()
    print("".join(lines) + "\n")
    

r_colors = {
    'warning'   : 'yellow',
    'normal'    : 'green',
    'info'      : 'cyan'
}
def rprint(text, type=None, end="\n"):
    if type == None:
        raise StarRailBaseException("Type not provided for rprint.")
    print(colored(text, r_colors[type]), end=end)

def rtext(text, type=None):
    if type == None:
        raise StarRailBaseException("Type not provided for rtext.")
    return colored(text, r_colors[type])


log_colors = {
    'normal'    : 'white',
    'success'   : 'green',
    'warning'   : 'yellow',
    'error'     : 'red'
}
def starrail_log_text(text, log_type="normal"):
    prefix = colored("StarRail-Log", "cyan")
    rtext = colored(text, log_colors[log_type])
    return f"[{prefix}] {rtext}"
    
def starrail_log(text, log_type="normal", end="\n"):
    rtext = starrail_log_text(text, log_type)
    print(rtext, end=end, file=sys.stdout)
    sys.stdout.flush()
    
def verify_game_path(abspath):
    return abspath != None and len(abspath) > 0 and os.path.exists(abspath) and os.path.basename(abspath) == GAME_DEFAULT
