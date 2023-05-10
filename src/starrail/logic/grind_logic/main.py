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
import cv2

from .constants import LOGIN_PROCESS_MAP, LOGIN_TEMPLATE_PATH

from ..._exceptions._exceptions import *
from ..._config.config_handler import ConfigHandler
from ...honkai_star_rail import HonkaiStarRail
from ..._utils._utils import StarRailScreenshotController
from ..._utils.controls.mouse import StarRailMouse
from ..._utils.cv2_SIFT.image_matcher import StarRailImageMatcher

class StarRailGrindController:
    def __init__(self):
        self.config_handler = ConfigHandler()
        try:
            self.game_instance = HonkaiStarRail(self.config_handler.get_game_path())
        except:
            raise StarRailBaseException("Error: game path not configured. Run `starrail configure` to configure the module.")
        self.image_matcher =  StarRailImageMatcher()
        self.mouse_controller = StarRailMouse()
        self.screenshot_controller = StarRailScreenshotController()
        
    def run(self):
        from elevate import elevate; elevate() # Elevate permission to move mouse in-game
        for process_name, template_name in LOGIN_PROCESS_MAP.items():
            if process_name == "start_game":
                self.game_instance.run()
                time.sleep(10)
                continue
            
            print(f"running {process_name}...")
            template_path = os.path.join(LOGIN_TEMPLATE_PATH, template_name)
            
            while True:
                self.screenshot_controller.take_screenshot()
                screenshot_abspath = self.screenshot_controller.get_screenshot_path()
                visualization, M, coords = self.image_matcher.match_image(template_path, screenshot_abspath, show_match=True)
                print(f"Coord: {coords}")
                
                if M is not None:
                    cv2.imshow("Image2 with Box", visualization)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                
                if coords == None: # No match
                    pass
                else:
                    self.mouse_controller.move_mouse_to_button(coords)
                    self.mouse_controller.click_mouse()
                    break
        