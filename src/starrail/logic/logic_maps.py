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

# ================================
# ======| BASE TEMPLATE | ========
# ================================
_BASE_TEMPLATE_PATH      = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_data", "images", "templates")

__general_template_path   = os.path.join(_BASE_TEMPLATE_PATH, "general")
__login_template_path     = os.path.join(_BASE_TEMPLATE_PATH, "login")
__rewards_template_path   = os.path.join(_BASE_TEMPLATE_PATH, "rewards")
__grind_templete_path     = os.path.join(_BASE_TEMPLATE_PATH, "grind")

# Map Structure
# {
#   [process_count  process_type  process_name] : process_metadata,
#   [process_count  process_type  process_name] : process_metadata  
# }

# Process Count
# Used to avoid duplicate dict keys and keep track of the process sequence.

# Process Types
# 1. execute:   Executes a specific process. No CV2 matching and no mouse movement involved.
# 2. mouse:     Generates CV2 match and then operates the mouse to accomplish a specific task.
# 3. verify:    Verifies that the template is on the current screen. No mouse movement involved.
# 4. keyboard:  Simulate a key click on the keyboard. Key clicked depends on the process_name.

# Process Name
# Used to keep track of the process.
# [keyboard] and [verify] type process names are used to determine the corresponding executions.

# Process Metadata (map_metadata: dict)
# 1. path:                  The abs-path to the button template
# 2. offset:                The mouse movement correction offset (x, y)
# 3. match_override_val:    The override value to the ML image detection.
# 4. dynamic_path:          The template path can and will be modified by the controller.
# 5. secondary_path:        The abs-path to the secondary button template (shifts button coord from the first image match)

# Dev Note 6/2/23 [Kevin L]:
# Some of the KV-pair in the process maps may seem redundant, but it's a design choice I've made.
# I aim to keep each process on one line with all the parameters layed out for good readibility. 
# I've tried implementing process sequences into classes (which eliminates most redundant KV-pairs)
# but it does not provide a good enough readibility for me to favor that approach in this case.

# ======================================
# ======| IMPORTANT TEMPLATES | ========
# ======================================

BASE_MENU_SCREEN_PATH = os.path.join(__general_template_path, "base-screen-with-menu.png")
OUT_OF_STAMINA_PATH = os.path.join(__grind_templete_path, "calyx", "out-of-stamina.png")
EXIT_BTN_PATH = os.path.join(__grind_templete_path, "calyx", "challenge-complete-exit.png")

# =================================
# ======| LOGIN TEMPLATE | ========
# =================================


LOGIN_PROCESS_MAP = {
    "1 [execute]  start_game"             : None,
    "2 [mouse]    login"                  : {"path": os.path.join(__login_template_path, "title_screen.png"),     "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "3 [verify]   base_screen"            : {"path": os.path.join(__general_template_path, "base-screen.png"),    "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "4 [end]      terminate_process"      : None
}


# ==================================
# ======| AWARDS TEMPLATE | ========
# ==================================

NAMELESS_HONORS_REWARDS_PROCESS_MAP = {
    "1 [verify]   base_screen_with_menu"      : {"path": os.path.join(__general_template_path, "base-screen-with-menu.png"),      "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "2 [mouse]    open_nameless_honors"       : {"path": os.path.join(__rewards_template_path, "nameless-honors-access.png"),     "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "3 [mouse]    open_missions_tab"          : {"path": os.path.join(__rewards_template_path, "missions.png"),                   "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "4 [mouse]    claim_all_rewards"          : {"path": os.path.join(__rewards_template_path, "claim-all-button.png"),           "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "5 [keyboard] exit_page"                  : None,
    "6 [verify]   base_screen_with_menu"      : {"path": os.path.join(__general_template_path, "base-screen-with-menu.png"),      "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "7 [end]      terminate_process"          : None
}


# =================================
# ======| GRIND TEMPLATE | ========
# =================================

__calyx_templete_path = os.path.join(__grind_templete_path, "calyx")
__calyx_golden_template_path = os.path.join(__grind_templete_path, "calyx", "calyx-golden")


ACCESS_CALYX_GOLDEN_PROCESS_MAP = {
    "1 [verify]   base_screen_with_menu"      : {"path": os.path.join(__general_template_path, "base-screen-with-menu.png"),  "offset": (0, 0),  "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "2 [mouse]    open_interastral_guide"     : {"path": os.path.join(__general_template_path, "interastral-guide.png"),      "offset": (0, 0),  "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "3 [mouse]    open_survival_index_tab"    : {"path": os.path.join(__grind_templete_path, "survival-index-tab.png"),       "offset": (0, 0),  "match_override_val": 30,   "dynamic_path": False, "secondary_path": None},
    "4 [mouse]    select_calyx_golden"        : {"path": os.path.join(__calyx_golden_template_path, "calyx-golden.png"),      "offset": (0, 0),  "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "5 [mouse]    select_calyx_type"          : {"path": os.path.join(__calyx_golden_template_path, "XXX"),                   "offset": (0, 0),  "match_override_val": None, "dynamic_path": True,  "secondary_path": os.path.join(__calyx_templete_path, "teleport-btn.png")},
    "6 [end]      terminate_process"          : None
}
CALYX_CRIMSON_PROCESS_MAP = {
    
}

RUN_CALYX_PROCESS_MAP = {
    "1 [verify]   calyx_menu"           : {"path": os.path.join(__calyx_templete_path, "calyx-verify.png"),  "offset": (0, 0),  "match_override_val": 40, "dynamic_path": False, "secondary_path": None},
    "2 [mouse]    start_challenge"      : {"path": os.path.join(__calyx_templete_path, "start-challenge.png"),      "offset": (0, 0),  "match_override_val": None, "dynamic_path": False, "secondary_path": None}, 
    "3 [mouse]    start_challenge-2"    : {"path": os.path.join(__calyx_templete_path, "start-challenge-2.png"),      "offset": (0, 0),  "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "4 [mouse]    turn_on_auto_battle"  : {"path": os.path.join(__calyx_templete_path, "auto-battle-off.png"),      "offset": (0, 0),  "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "5 [end]      terminate_process"   : None
}

LOOP_CALYX_PROCESS_MAP = {
    "1 [verify]   challenge_complete"    : {"path": os.path.join(__calyx_templete_path, "challenge-completed.png"),  "offset": (0, 0),  "match_override_val": 80, "dynamic_path": False, "secondary_path": None},
    "2 [mouse]    challenge_again"       : {"path": os.path.join(__calyx_templete_path, "challenge-again.png"),      "offset": (0, 0),  "match_override_val": None, "dynamic_path": False, "secondary_path": None},
    "3 [end]      terminate_process"     : None
}



# ==================================
# ======| HELPER TEMPLATE | ========
# ==================================

FAIL_SAFT_PROCESS_MAP = {
    
}


MAPS = [
    LOGIN_PROCESS_MAP,
    NAMELESS_HONORS_REWARDS_PROCESS_MAP,
    ACCESS_CALYX_GOLDEN_PROCESS_MAP,
    CALYX_CRIMSON_PROCESS_MAP,
    RUN_CALYX_PROCESS_MAP,
    LOOP_CALYX_PROCESS_MAP
]


# MAP VALIDATION (ensures all mapped templates exist)
if __name__ == "__main__":
    def validate_maps():
        validate_success = True
        for map in MAPS:
            for _, meta in map.items():
                try:
                    path = meta['path']
                except:
                    continue
                if path is not None and os.path.isfile(path) == False and meta['dynamic_path'] == False:
                    print(f"Invalid Path: {path}")
                    validate_success = False
        return validate_success
    
    if validate_maps():
        print("All maps are good.")
    