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
from copy import deepcopy

from .calyx_name_map import CALYX_GOLDEN_NAME_MAP, CALYX_CRIMSON_NAME_MAP
from ..logic_maps import ACCESS_CALYX_GOLDEN_PROCESS_MAP, ACCESS_CALYX_CRIMSON_PROCESS_MAP, RUN_CALYX_PROCESS_MAP, LOOP_CALYX_PROCESS_MAP, MouseProcess, ScreenVerificationProcess
from ..base_logic import StarRailLogicController

class StarRailGrindController:
    def __init__(self):
        self.logic_controller = StarRailLogicController()    
    
    def base_grind_game(self):
        pass
    
    def access_golden_calyx(self, calyx_name=None):
        # Set Calyx Flower in Calyx Golden 
        for sim_process in ACCESS_CALYX_GOLDEN_PROCESS_MAP._logic_map:
            if isinstance(sim_process, MouseProcess) or isinstance(sim_process, ScreenVerificationProcess):
                if sim_process.dynamic_path == True:
                    sim_process.update_dynamic_template_path(filename=CALYX_GOLDEN_NAME_MAP[calyx_name])

        # # Navigate to home screen with menu
        # self.logic_controller.return_to_base_menu_screen()
        
        # Run logic map to access the Calyx page
        run_success = self.logic_controller.run_logic_map(logic_map=ACCESS_CALYX_GOLDEN_PROCESS_MAP)
        return run_success
    
    
    def run_calyx(self):
        run_success = self.logic_controller.run_logic_map(logic_map=RUN_CALYX_PROCESS_MAP)
        while True:
            self.logic_controller.run_logic_map(logic_map=LOOP_CALYX_PROCESS_MAP)
            if self.logic_controller.check_out_of_stamina() == True:
                break
        self.logic_controller.return_to_base_menu_screen()
        return run_success
            
