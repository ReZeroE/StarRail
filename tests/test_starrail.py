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

import subprocess
import psutil
import pytest
import time
import os
import pyautogui

# ===============================================
# ==== | THE FOLLOWING IS FOR TESTING ONLY | ====
# ===============================================
if __name__ == "__main__":
    
    import time
    import starrail
    import traceback
    
    login_controller    = starrail.StarRailLoginController()
    grind_controller    = starrail.StarRailGrindController()
    rewards_controller  = starrail.StarRailRewardsController()
    
    try:
        login_controller.base_login()                                           # Start and login to game
        grind_controller.access_golden_calyx(calyx_name="bud_of_threasures")    # Access Golden Calyx - Bud of Threasures
        grind_controller.run_calyx()                                            # Run Calyx (max waves with auto stamina detection)
        rewards_controller.get_all_rewards()                                    # Get supported rewards
        login_controller.base_logout()                                          # Logout and exit game

    except Exception as ex:
        traceback.print_exc()
        time.sleep(20)