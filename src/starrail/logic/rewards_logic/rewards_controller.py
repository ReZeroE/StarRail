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

from ..logic_maps import NAMELESS_HONORS_REWARDS_PROCESS_MAP, ASSIGNMENT_REWARDS_PROCESS_MAP, ACCESS_DAILY_TRAINING_REWARDS_PROCESS_MAP, LOOP_DAILY_TRAINING_REWARDS_PROCESS_MAP
from ..base_logic import StarRailLogicController

class StarRailRewardsController:
    def __init__(self):
        self.logic_controller = StarRailLogicController()
        
    def get_nameless_honor_rewards(self):
        run_success = self.logic_controller.run_logic_map(logic_map=NAMELESS_HONORS_REWARDS_PROCESS_MAP)
        self.logic_controller.return_to_base_menu_screen()
        return run_success
    
    def get_assignment_rewards(self):
        run_success = self.logic_controller.run_logic_map(logic_map=ASSIGNMENT_REWARDS_PROCESS_MAP)
        self.logic_controller.return_to_base_menu_screen()
        return run_success
    
    def get_daily_training_rewards(self):
        run_success = self.logic_controller.run_logic_map(logic_map=ACCESS_DAILY_TRAINING_REWARDS_PROCESS_MAP)
        while True:
            loop_success = self.logic_controller.run_logic_map(logic_map=LOOP_DAILY_TRAINING_REWARDS_PROCESS_MAP)
            if loop_success == False:
                break
        self.logic_controller.return_to_base_menu_screen()
        return run_success
    
    def get_all_rewards(self):
        s1 = self.get_nameless_honor_rewards()
        s2 = self.get_assignment_rewards()
        s3 = self.get_daily_training_rewards()
        return s1 and s2 and s3