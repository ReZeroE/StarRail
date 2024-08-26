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
import re
import sys
import string
import shutil
from datetime import datetime
from enum import Enum
import pyautogui
import platform
from concurrent import futures
from multiprocessing import Manager
import hashlib
import readline

from termcolor import colored
from starrail import constants
from starrail.constants import BASENAME, SHORTNAME, COMMAND, GAME_FILENAME, DATETIME_FORMAT, TIME_FORMAT
from starrail.exceptions.exceptions import *


# =================================================
# ==============| CUSTOM PRINTER | ================
# =================================================

class Printer:
    @staticmethod
    def hex_text(text, hex_color):
        
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        rgb = hex_to_rgb(hex_color)
        escape_seq = f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m" # ANSI escape code for 24-bit (true color): \x1b[38;2;<r>;<g>;<b>m
        return f"{escape_seq}{text}\x1b[0m"

    @staticmethod
    def to_purple(text):
        return Printer.hex_text(text, "#a471bf")
    
    @staticmethod
    def to_lightpurple(text):
        return Printer.hex_text(text, "#c38ef5")
        
    @staticmethod
    def to_skyblue(text):
        return Printer.hex_text(text, "#6dcfd1")
        
    @staticmethod
    def to_lightgrey(text):
        return Printer.hex_text(text, "#8a8a8a")

    @staticmethod
    def to_blue(text):
        return Printer.hex_text(text, "#3c80f0")

    @staticmethod
    def to_lightblue(text):
        return Printer.hex_text(text, "#8ab1f2")
    
    @staticmethod
    def to_darkblue(text):
        return Printer.hex_text(text, "#2a9bc3")
    
    @staticmethod
    def to_lightgreen(text):
        return Printer.hex_text(text, "#74d47b")
    
    @staticmethod
    def to_lightred(text):
        return Printer.hex_text(text, "#f27e82")
    
    def to_githubblack(text):
        return Printer.hex_text(text, "#121212") # C9A2FF, 7A7A7A
    
    # Firefly Colors
    
    @staticmethod
    def to_pale_yellow(text):
        return Printer.hex_text(text, "#f3f2c9")

    @staticmethod
    def to_light_blue(text):
        return Printer.hex_text(text, "#b9d8d6")

    @staticmethod
    def to_teal(text):
        return Printer.hex_text(text, "#7ba7a8")

    @staticmethod
    def to_turquoise(text):
        return Printer.hex_text(text, "#4a8593")

    @staticmethod
    def to_dark_teal(text):
        return Printer.hex_text(text, "#2f6b72")




class LogType(Enum):
    NORMAL  = "white"
    SUCCESS = "green"
    WARNING = "yellow"
    ERROR   = "red"

def __get_colored_prefix():
    # return f"[{colored(BASENAME, "cyan")}] "
    return f"[{Printer.to_purple(SHORTNAME)}] "

def __get_colored_submodule(submodule_name):
    colored_submodule_name = Printer.to_purple(submodule_name)
    return f"[{colored_submodule_name}] "

def atext(text: str, log_type: LogType = LogType.NORMAL) -> str:
    rtext = colored(text, log_type.value)
    return f"{__get_colored_prefix()}{rtext}"

def aprint(
    text: str, 
    log_type: LogType   = LogType.NORMAL, 
    end: str            = "\n", 
    submodule_name: str = "", 
    new_line_no_prefix  = True, 
    file                = sys.stdout, 
    flush               = True
):
    # The new_line_no_prefix param coupled with \n in the text param will put the
    # text after the new line character on the next line, but without a prefix.
    if "\n" in text and new_line_no_prefix == True:
        text = text.replace("\n", f"\n           ")
    
    # Set colored submodule name if available
    colored_submodule_name = ""
    if submodule_name:
        colored_submodule_name = __get_colored_submodule(submodule_name)
    
    # Get colored prefix and text
    colored_text = colored(text, log_type.value)
    colored_prefix = __get_colored_prefix()
    
    # Put all together and print
    final_text = f"{colored_prefix}{colored_submodule_name}{colored_text}"
    print(final_text, end=end, file=file, flush=flush)


def get_prefix_space():
    return " " * (len(SHORTNAME)+2)

def color_cmd(text: str, with_quotes: bool = False):
    text = text.lower()
    
    if constants.CLI_MODE == True:
        text = text.replace(COMMAND, "").strip()
    else:
        if not text.startswith(COMMAND):
            text = f"{COMMAND} {text}"
            
    colored_cmd = colored(text, "light_cyan")
    
    if with_quotes:
        return f"'{colored_cmd}'"
    return colored_cmd

def bool_to_str(boolean: bool, true_text="Running", false_text="Not Running"):
    CHECKMARK = "\u2713"
    CROSSMARK = "\u2717"
    if boolean:
        return Printer.to_lightgreen(f"{CHECKMARK} {true_text}")
    return Printer.to_lightred(f"{CROSSMARK} {false_text}")



class StarRailGameDetector:
    """
    Honkai Star Rail Game Detector - Finds the game on local drives
    """
    def get_local_drives(self):
        available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        return available_drives

    def find_game_in_path(self, path, name, stop_flag):
        for root, _, files in os.walk(path):
            if stop_flag.value: # Check the shared flag value.
                return None
            if name in files:
                return os.path.join(root, name)
        return None

    def find_game(self, paths=[], name=GAME_FILENAME):
        for p in paths:
            if not os.path.exists(p):
                raise StarRailBaseException(f"Path does not exist. [{p}]")

        if len(paths) == 0:
            paths = self.get_local_drives()

        paths = [f"{path}\\" if path.endswith(":") and len(path) == 2 else path for path in paths]

        worker_threads = 1
        if os.cpu_count() > 1:
            worker_threads = os.cpu_count() - 1

        with futures.ProcessPoolExecutor(max_workers=worker_threads) as executor, Manager() as manager:
            stop_flag = manager.Value('b', False)   # Create a boolean shared flag.
            future_to_path = {executor.submit(self.find_game_in_path, path, name, stop_flag): path for path in paths}
            for future in futures.as_completed(future_to_path):
                result = future.result()
                if result is not None:
                    stop_flag.value = True # Set the flag to true when a result is found.
                    return result
        return None


class StarRailScreenshotController:
    """
    Honkai Star Rail Screenshot Controller - Takes and stores in-game screenshots for processing
    """
    def __init__(self):
        self.__screenshot_abspath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_data", "images", "screenshots", "screenshot.png")
    
    def get_screenshot_path(self):
        return self.__screenshot_abspath
    
    def take_screenshot(self):
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(self.__screenshot_abspath)
        assert(os.path.isfile(self.__screenshot_abspath))


def verify_platform():
    """
    Verifies whether the OS is supported by the package.
    Package starrail only support Windows installations of Honkai Star Rail.
    
    :return: true if running on Windows, false otherwise
    :rtype: bool
    """
    return os.name == "nt"


def is_admin() -> bool:
    try:
        # For Windows
        if platform.system().lower() == "windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

        # For Linux and MacOS
        else:
            return os.getuid() == 0  # os.getuid() returns '0' if running as root

    except Exception as e:
        aprint(f"Error checking administrative privileges: {e}", log_type=LogType.ERROR)
        return False


def print_disclaimer():
    DISCLAIMER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "textfiles", "disclaimer.txt")
    with open(DISCLAIMER_PATH, "r") as rf:
        lines = rf.readlines()
    print("".join(lines) + "\n")

def print_webcache_explanation():
    print(Printer.to_lightred("\n   What is Web Cache?"))
    print(f"{Printer.to_lightred(' > ') + 'Web cache for Honkai: Star Rail stores recent web data.'}")
    print(f"{Printer.to_lightred(' > ') + 'You can open URLs to view announcements, events, or pull status, allowing quick access without loading into the game.'}\n")
    


# =================================================
# ============| CENTER TEXT HELPER | ==============
# =================================================

# DON"T CHANGE THE FOLLOWING TWO CENTER TEXT FUNCTIONS. I GOT THESE TO WORK AFTER HOURS. BOTH ARE NEEDED!

def center_text(text: str):
    terminal_width, terminal_height = shutil.get_terminal_size((80, 20))  # Default size
    
    lines = text.split('\n')
    max_width = max(len(line) for line in lines)
    left_padding = (terminal_width - max_width) // 2
    
    new_text = []
    for line in lines:
        new_text.append(' ' * left_padding + line)
    return "\n".join(new_text) 
        
def print_centered(text: str):
    def strip_ansi_codes(s):
        return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', s)
    
    terminal_width = os.get_terminal_size().columns
    lines = text.split('\n')
    for line in lines:
        line_without_ansi = strip_ansi_codes(line)
        leading_spaces = (terminal_width - len(line_without_ansi)) // 2
        print(' ' * leading_spaces + line.strip())
        
        
class DatetimeHandler:
    @staticmethod
    def get_datetime():
        return datetime.now().replace(microsecond=0)

    def get_datetime_str():
        return datetime.now().strftime(DATETIME_FORMAT)

    def get_time_str():
        return datetime.now().strftime(TIME_FORMAT)

    @staticmethod
    def datetime_to_str(datetime: datetime):
        return datetime.strftime(DATETIME_FORMAT)
    
    @staticmethod
    def str_to_datetime(datetime_str: str):
        return datetime.strptime(datetime_str, DATETIME_FORMAT)
    
    @staticmethod
    def epoch_to_time_str(epoch_time: float):
        return datetime.fromtimestamp(epoch_time).strftime(DATETIME_FORMAT)

    @staticmethod
    def epoch_to_datetime(epoch_time: float):
        return datetime.fromtimestamp(epoch_time)
    
    @staticmethod
    def seconds_to_time_str(seconds: int):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        str_ret = ""
        if hours > 0:
            str_ret += f"{hours} {'Hours' if hours > 1 else 'Hour'} "
        if minutes > 0:
            str_ret += f"{minutes} {'Minutes' if minutes > 1 else 'Minute'} "
        str_ret += f"{seconds} {'Seconds' if seconds > 1 else 'Second'}"
    
        return str_ret
    
class HashCalculator:
    @staticmethod
    def SHA256(file_path: str):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    
    
def merge_dicts(*dicts):
    result = {}
    for d in dicts:
        if d == None:
            continue
        
        for key, value in d.items():
            if key in result:
                if isinstance(result[key], (list, tuple)):
                    if isinstance(value, (list, tuple)):
                        result[key].extend(value)
                    else:
                        result[key].append(value)
                else:
                    if isinstance(value, (list, tuple)):
                        result[key] = [result[key]] + list(value)
                    else:
                        result[key] = [result[key], value]
            else:
                result[key] = value if not isinstance(value, (list, tuple)) else list(value)
    return result

