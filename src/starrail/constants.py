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

# ==================================
# ==========| CONSTANTS | ==========
# ==================================

BASENAME            = "StarRail CLI"
SHORTNAME           = "StarRail"
COMMAND             = "starrail"
VERSION             = "1.0.2"
VERSION_DESC        = "Beta"
DEVELOPMENT         = VERSION_DESC.lower() != "stable"

TIME_FORMAT         = "%H:%M:%S"
DATETIME_FORMAT     = "%Y-%m-%d %H:%M:%S"

GAME_NAME           = "Honkai: Star Rail"
GAME_FILENAME       = "StarRail.exe"
GAME_FILE_PATH      = f"Star Rail/Game/{GAME_FILENAME}"
GAME_FILE_PATH_NEW  = f"Star Rail Games/{GAME_FILENAME}"

AUTHOR              = "Kevin L."
AUTHOR_DETAIL       = f"{AUTHOR} - kevinliu@vt.edu - Github: ReZeroE"
REPOSITORY          = "https://github.com/ReZeroE/StarRail"
ISSUES              = f"{REPOSITORY}/issues"

HOMEPAGE_URL        = "https://hsr.hoyoverse.com/en-us/"
HOYOLAB_URL         = "https://www.hoyolab.com/home"
YOUTUBE_URL         = "https://www.youtube.com/channel/UC2PeMPA8PAOp-bynLoCeMLA"


# ==================================
# ============| PATHS | ============
# ==================================

HOME_DIRECTORY      = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

__PYTHON_MODULE_PATH = os.path.join(HOME_DIRECTORY, "Lib", "site-packages", "starrail")
if os.path.exists(__PYTHON_MODULE_PATH):
    # If the module is built using `pip install .`, then the path would be something like C:/PythonXXX/Lib/site-packages/<package_name>
    HOME_DIRECTORY = __PYTHON_MODULE_PATH
    STARRAIL_DIRECTORY = __PYTHON_MODULE_PATH
else:
    # Else if the module is built locally using `pip install -e .`, then the path will be the local directory structure
    STARRAIL_DIRECTORY   = os.path.join(HOME_DIRECTORY, "src", "starrail")


# ==================================
# ===========| GLOBALS | ===========
# ==================================

# Global variables to identify whether the program is in CLI mode
# MUST BE USED AS constants.CLI_MODE (only this accesses the re-bind value)
CLI_MODE        = False

CURSOR_UP_ANSI  = "\033[A"

MIN_WEAK_MATCH_EXE_SIZE = 0.5 # megabytes


# ==================================
# ==========| RECORDER | ===========
# ==================================

RECORDER_WINDOW_INFO = {
    "width": 600,
    "height": 100,
    "border-radius": 10
}

CALIBRATION_MONITOR_INFO = {
    "width": 3840,
    "height": 2160
}


# ==================================
# ============| OTHER | ============
# ==================================

WEBCACHE_IGNORE_FILETYPES = [
    ".js",
    ".css",
    ".png",
    ".jpg",
    ".jpeg"
]

from pynput.keyboard import Key
PYNPUT_KEY_MAPPING = {
    'Key.esc'       : Key.esc,
    'Key.space'     : Key.space,
    'Key.backspace' : Key.backspace,
    'Key.enter'     : Key.enter,
    
    'Key.tab'       : Key.tab,
    'Key.caps_lock' : Key.caps_lock,
    'Key.shift'     : Key.shift,
    'Key.ctrl'      : Key.ctrl,
    'Key.alt'       : Key.alt,
    
    'Key.delete'    : Key.delete,
    'Key.end'       : Key.end,
    'Key.home'      : Key.home,
    
    'Key.f1'        : Key.f1,
    'Key.f2'        : Key.f2,
    'Key.f3'        : Key.f3,
    'Key.f4'        : Key.f4,
    'Key.f5'        : Key.f5,
    'Key.f6'        : Key.f6,
    'Key.f7'        : Key.f7,
    'Key.f8'        : Key.f8,
    'Key.f9'        : Key.f9,
    'Key.f10'       : Key.f10,
    'Key.f11'       : Key.f11,
    'Key.f12'       : Key.f12,
    
    'Key.page_down' : Key.page_down,
    'Key.page_up'   : Key.page_up,
    
    'Key.up'        : Key.up,
    'Key.down'      : Key.down,
    'Key.left'      : Key.left,
    'Key.right'     : Key.right,
    
    'Key.media_play_pause'  : Key.media_play_pause,
    'Key.media_volume_mute' : Key.media_volume_mute,
    'Key.media_volume_up'   : Key.media_volume_up,
    'Key.media_volume_down' : Key.media_volume_down,
    'Key.media_previous'    : Key.media_previous,
    'Key.media_next'        : Key.media_next,
    'Key.insert'            : Key.insert,
    'Key.menu'              : Key.menu,
    'Key.num_lock'          : Key.num_lock,
    'Key.pause'             : Key.pause,
    'Key.print_screen'      : Key.print_screen,
    'Key.scroll_lock'       : Key.scroll_lock
}