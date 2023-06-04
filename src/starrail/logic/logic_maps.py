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



class BaseSimulationProcess:
    def __init__(self, sproc_name):
        self.sprocess_name = sproc_name
        
    def __str__(self):
        return f"{self.__class__} {self.sprocess_name}"


class MouseProcess(BaseSimulationProcess):
    def __init__(self, sproc_name, template_path=None, dynamic_path=False, secondary_template_path=None, mouse_correction=(0, 0), sift_match_override_val=None):
        super(MouseProcess, self).__init__(sproc_name)
        
        self.template_path           = template_path
        self.dynamic_path            = dynamic_path
        self.secondary_template_path = secondary_template_path
                
        self.mouse_correction        = mouse_correction
        self.sift_match_override_val = sift_match_override_val
        
    def update_dynamic_template_path(self, filename):
        if self.dynamic_path == True:
            self.template_path = self.template_path.replace("XXX", filename)


class ScreenVerificationProcess(BaseSimulationProcess):
    def __init__(self, sproc_name, template_path=None, dynamic_path=False, mouse_correction=(0, 0), sift_match_override_val=None, timeout=None, exit_on_match=False):
        super(ScreenVerificationProcess, self).__init__(sproc_name)
        
        self.template_path           = template_path
        self.dynamic_path            = dynamic_path
                
        self.mouse_correction        = mouse_correction
        self.sift_match_override_val = sift_match_override_val
        self.timeout                 = timeout
        self.exit_on_match           = exit_on_match
        
    def update_dynamic_template_path(self, filename):
        if self.dynamic_path == True:
            self.template_path = self.template_path.replace("XXX", filename)
        
class KeyboardProcess(BaseSimulationProcess):
    def __init__(self, sproc_name):
        super(KeyboardProcess, self).__init__(sproc_name)


class ExecutableProcess(BaseSimulationProcess):
    def __init__(self, sproc_name):
        super(ExecutableProcess, self).__init__(sproc_name)


class EndProcess(BaseSimulationProcess):
    def __init__(self, sproc_name="end_process_map"):
        super(EndProcess, self).__init__(sproc_name)


class LogicMap:
    def __init__(self):
        self._logic_map = []
        
    def add_process(self, sim_process):
        self._logic_map.append(sim_process)
        
    def add_processes(self, sim_processes: list):
        assert(isinstance(sim_processes, list))
        self._logic_map += sim_processes
        
    def get_logic_map(self):
        return self._logic_map
        


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


# ======================================
# ======| IMPORTANT TEMPLATES | ========
# ======================================

BASE_MENU_SCREEN_PATH   = os.path.join(__general_template_path, "base-screen-with-menu.png")
OUT_OF_STAMINA_PATH     = os.path.join(__grind_templete_path, "calyx", "out-of-stamina.png")
EXIT_BTN_PATH           = os.path.join(__grind_templete_path, "calyx", "challenge-complete-exit.png")

# =================================
# ======| LOGIN TEMPLATE | ========
# =================================


# LOGIN_PROCESS_MAP = {
#     "1 [execute]  start_game"             : None,
#     "2 [mouse]    login"                  : {"path": os.path.join(__login_template_path, "title_screen.png"),     "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None, "break_on_fail": False},
#     "3 [verify]   base_screen"            : {"path": os.path.join(__general_template_path, "base-screen.png"),    "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None, "break_on_fail": False},
#     "4 [end]      terminate_process"      : None
# }

LOGIN_PROCESS_MAP = LogicMap()
LOGIN_PROCESS_MAP.add_processes(
    [
        ExecutableProcess           (sproc_name="start_game"    ),
        MouseProcess                (sproc_name="login",        template_path=os.path.join(__login_template_path, "title_screen.png")),
        ScreenVerificationProcess   (sproc_name="base_screen",  template_path=os.path.join(__general_template_path, "base-screen.png")),
        EndProcess()
    ]
)


# ==================================
# ======| AWARDS TEMPLATE | ========
# ==================================

# NAMELESS_HONORS_REWARDS_PROCESS_MAP = {
#     "1 [verify]   base_screen_with_menu"      : {"path": os.path.join(__general_template_path, "base-screen-with-menu.png"),      "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None, "break_on_fail": False},
#     "2 [mouse]    open_nameless_honors"       : {"path": os.path.join(__rewards_template_path, "nameless-honors-access.png"),     "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None, "break_on_fail": False},
#     "3 [mouse]    open_missions_tab"          : {"path": os.path.join(__rewards_template_path, "missions.png"),                   "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None, "break_on_fail": False},
#     "4 [mouse]    claim_all_rewards"          : {"path": os.path.join(__rewards_template_path, "claim-all-button.png"),           "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None, "break_on_fail": False},
#     "5 [keyboard] exit_page"                  : None,
#     "6 [verify]   base_screen_with_menu"      : {"path": os.path.join(__general_template_path, "base-screen-with-menu.png"),      "offset": (0, 0),   "match_override_val": None, "dynamic_path": False, "secondary_path": None, "break_on_fail": False},
#     "7 [end]      terminate_process"          : None
# }

NAMELESS_HONORS_REWARDS_PROCESS_MAP = LogicMap()
NAMELESS_HONORS_REWARDS_PROCESS_MAP.add_processes(
    [
        ScreenVerificationProcess   (sproc_name="base_screen_with_menu",    template_path=os.path.join(__general_template_path, "base-screen-with-menu.png")        ),
        MouseProcess                (sproc_name="open_nameless_honors",     template_path=os.path.join(__rewards_template_path, "nameless-honors-access.png")       ),
        MouseProcess                (sproc_name="open_missions_tab",        template_path=os.path.join(__rewards_template_path, "missions.png")                     ),
        ScreenVerificationProcess   (sproc_name="verify_claim_all_rewards", template_path=os.path.join(__rewards_template_path, "claim-all-button.png"),            timeout=10),
        MouseProcess                (sproc_name="claim_all_rewards",        template_path=os.path.join(__rewards_template_path, "claim-all-button.png")             ),
        KeyboardProcess             (sproc_name="exit_page"                 ),
        ScreenVerificationProcess   (sproc_name="base_screen_with_menu",    template_path=os.path.join(__general_template_path, "base-screen-with-menu.png")        ),
        EndProcess()
    ]
)

ASSIGNMENT_REWARDS_PROCESS_MAP = LogicMap()
ASSIGNMENT_REWARDS_PROCESS_MAP.add_processes(
    [
        ScreenVerificationProcess   (sproc_name="base_screen_with_menu",            template_path=os.path.join(__general_template_path, "base-screen-with-menu.png")    ),
        MouseProcess                (sproc_name="open_assignments",                 template_path=os.path.join(__rewards_template_path, "assignments-access.png")       ),
        ScreenVerificationProcess   (sproc_name="verify_claim_assignment_reward",   template_path=os.path.join(__rewards_template_path, "claim-button.png"),            timeout=10),
        MouseProcess                (sproc_name="claim_assignment_reward",          template_path=os.path.join(__rewards_template_path, "claim-button.png")             ),
        MouseProcess                (sproc_name="dispatch_again",                   template_path=os.path.join(__rewards_template_path, "dispatch-again.png")           ),
        KeyboardProcess             (sproc_name="exit_page"                         ),
        ScreenVerificationProcess   (sproc_name="base_screen_with_menu",            template_path=os.path.join(__general_template_path, "base-screen-with-menu.png")    ),
        EndProcess()
    ]
)

ACCESS_DAILY_TRAINING_REWARDS_PROCESS_MAP = LogicMap()
ACCESS_DAILY_TRAINING_REWARDS_PROCESS_MAP.add_processes(
    [
        ScreenVerificationProcess   (sproc_name="base_screen_with_menu",            template_path=os.path.join(__general_template_path, "base-screen-with-menu.png")    ),
        MouseProcess                (sproc_name="open_interastral_guide",           template_path=os.path.join(__general_template_path, "interastral-guide.png")        ),
        ScreenVerificationProcess   (sproc_name="daily_training_tab",               template_path=os.path.join(__rewards_template_path, "daily-training-tab.png")       ),
        EndProcess()
    ]
)
LOOP_DAILY_TRAINING_REWARDS_PROCESS_MAP = LogicMap()
LOOP_DAILY_TRAINING_REWARDS_PROCESS_MAP.add_processes(
    [
        ScreenVerificationProcess   (sproc_name="verify_claim_daily_training_reward",        template_path=os.path.join(__rewards_template_path, "claim-daily-training-button.png"),   timeout=10, sift_match_override_val=40),
        MouseProcess                (sproc_name="claim_daily_training_reward",               template_path=os.path.join(__rewards_template_path, "claim-daily-training-button.png")    ),
    ]
)

# =================================
# ======| GRIND TEMPLATE | ========
# =================================

__calyx_templete_path = os.path.join(__grind_templete_path, "calyx")
__calyx_golden_template_path = os.path.join(__grind_templete_path, "calyx", "calyx-golden")


ACCESS_CALYX_CRIMSON_PROCESS_MAP = {
    
}

ACCESS_CALYX_GOLDEN_PROCESS_MAP = LogicMap()
ACCESS_CALYX_GOLDEN_PROCESS_MAP.add_processes(
    [
        ScreenVerificationProcess   (sproc_name="base_screen_with_menu",    template_path=os.path.join(__general_template_path, "base-screen-with-menu.png")    ),
        MouseProcess                (sproc_name="open_interastral_guide",   template_path=os.path.join(__general_template_path, "interastral-guide.png")        ),
        MouseProcess                (sproc_name="open_survival_index_tab",  template_path=os.path.join(__grind_templete_path, "survival-index-tab.png"),        sift_match_override_val=25),
        MouseProcess                (sproc_name="select_calyx_golden",      template_path=os.path.join(__calyx_golden_template_path, "calyx-golden.png")        ),
        MouseProcess                (sproc_name="select_calyx_type",        template_path=os.path.join(__calyx_golden_template_path, "XXX"),                    dynamic_path=True, secondary_template_path=os.path.join(__calyx_templete_path, "teleport-btn.png")),
        EndProcess()
    ]
)


RUN_CALYX_PROCESS_MAP = LogicMap()
RUN_CALYX_PROCESS_MAP.add_processes(
    [
        ScreenVerificationProcess   (sproc_name="calyx_menu",           template_path=os.path.join(__calyx_templete_path, "calyx-verify.png"),      sift_match_override_val=40),
        MouseProcess                (sproc_name="start_challenge",      template_path=os.path.join(__calyx_templete_path, "start-challenge.png")    ),
        MouseProcess                (sproc_name="start_challenge-2",    template_path=os.path.join(__calyx_templete_path, "start-challenge-2.png")  ),
        MouseProcess                (sproc_name="turn_on_auto_battle",  template_path=os.path.join(__calyx_templete_path, "auto-battle-off.png")    ),
        EndProcess()
    ]
)

LOOP_CALYX_PROCESS_MAP = LogicMap()
LOOP_CALYX_PROCESS_MAP.add_processes(
    [
        ScreenVerificationProcess   (sproc_name="challenge_complete",   template_path=os.path.join(__calyx_templete_path, "challenge-completed.png"),   sift_match_override_val=80),
        MouseProcess                (sproc_name="challenge_again",      template_path=os.path.join(__calyx_templete_path, "challenge-again.png")        ),
        EndProcess()
    ]
)




# ==================================
# ======| HELPER TEMPLATE | ========
# ==================================

FAIL_SAFT_PROCESS_MAP = {
    
}


MAPS = [
    LOGIN_PROCESS_MAP,
    
    NAMELESS_HONORS_REWARDS_PROCESS_MAP,
    ASSIGNMENT_REWARDS_PROCESS_MAP,
    ACCESS_DAILY_TRAINING_REWARDS_PROCESS_MAP,
    LOOP_DAILY_TRAINING_REWARDS_PROCESS_MAP,
    
    ACCESS_CALYX_GOLDEN_PROCESS_MAP,
    ACCESS_CALYX_CRIMSON_PROCESS_MAP,
    RUN_CALYX_PROCESS_MAP,
    LOOP_CALYX_PROCESS_MAP
]




# MAP VALIDATION (ensures all mapped templates exist)
if __name__ == "__main__":
    def validate_maps():
        validate_success = True
        for m in MAPS:
            if isinstance(m, LogicMap):
                for proc in m.get_logic_map():
                    if isinstance(proc, MouseProcess) or isinstance(proc, ScreenVerificationProcess):
                        template_path = proc.template_path
                        dynamic_path = proc.dynamic_path
                        if not os.path.isfile(template_path) and dynamic_path == False:
                            print(f"Invalid Path: {template_path}")
                            validate_success = False
        return validate_success
    
    if validate_maps():
        print("All maps are good.")
    
    
#     def validate_maps():
#         validate_success = True
#         for map in MAPS:
#             for _, meta in map.items():
#                 if meta is not None and not os.path.isfile(meta['path']) and meta['dynamic_path'] == False:
#                     print(f"Invalid Path: {meta['path']}")
#                     validate_success = False
#         return validate_success
    
#     if validate_maps():
#         print("All maps are good.")
    