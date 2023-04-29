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
from termcolor import colored

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
    

rprint_colors = {
    'warning'   : 'red',
    'normal'    : 'green',
    'cyan'      : 'cyan'
}
def rprint(text, type=None, end="\n"):
    if type == None:
        raise Exception("Type not provided for rprint.")
    print(colored(text, rprint_colors[type]), end=end)

def rtext(text, type=None):
    if type == None:
        raise Exception("Type not provided for rtext.")
    return colored(text, rprint_colors[type])


def starrail_log(text, log_type=None, end="\n"):
    log_colors = {
        'normal'    : 'green',
        'info'      : 'cyan',
        'warning'   : 'red'
    }
    if log_type == None:
        raise Exception("Type not provided for starrail_log.")
    
    prefix = colored("StarRail Log", log_colors["info"])
    message = colored(text, log_colors[log_type])
    print(f"[{prefix}] {message}", end=end, file=sys.stdout)