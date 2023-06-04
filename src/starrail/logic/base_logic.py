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

from .._exceptions._exceptions import *
from .._config.config_handler import ConfigHandler
from ..honkai_star_rail import HonkaiStarRail
from .._utils._utils import StarRailScreenshotController, starrail_log
from .._utils.controls.mouse import StarRailMouse
from .._utils.controls.keyboard import StarRailKeyboard
from .._utils.cv2_SIFT.image_matcher import StarRailImageMatcher

from .logic_maps import BASE_MENU_SCREEN_PATH, OUT_OF_STAMINA_PATH, EXIT_BTN_PATH, BaseSimulationProcess, MouseProcess, KeyboardProcess, ScreenVerificationProcess, ExecutableProcess, EndProcess, LogicMap


class StarRailLogicController:
    def __init__(self):
        self.config_handler = ConfigHandler()
        try:
            self.game_instance = HonkaiStarRail(self.config_handler.get_game_path())
        except:
            raise StarRailBaseException("Error: game path not configured. Run `starrail configure` to configure the module.")
        
        self.image_matcher          = StarRailImageMatcher()
        self.mouse_controller       = StarRailMouse()
        self.keyboard_controller    = StarRailKeyboard()
        self.screenshot_controller  = StarRailScreenshotController()
        
    
    # ===========================================
    # ======| LOGIC MAP EXEU FUNCTIONS | ========
    # ===========================================
    
    def run_logic_map(self, logic_map: LogicMap):
        from elevate import elevate; elevate() # Elevate permission to move mouse in-game
        assert(isinstance(logic_map, LogicMap))

        try:            
            for sim_process in logic_map._logic_map:
                if isinstance(sim_process, BaseSimulationProcess):
                    print(sim_process.__str__())
                
                # ==========================================
                # ==========| PROCESS EXECUTION |===========
                # ==========================================
                if isinstance(sim_process, ExecutableProcess):
                    process_name = sim_process.sprocess_name
                    executed_base_process = self.execute_process(process_name)
                    if executed_base_process: # Process executed successfully
                        continue
                    else:
                        raise StarRailBaseException(f"Attempted to execute a process that is not found. {process_name}")
                
                # ============================================
                # ==========| SCREEN VERIFICATION |===========
                # ============================================
                elif isinstance(sim_process, ScreenVerificationProcess):
                    process_name            = sim_process.sprocess_name
                    template_path           = sim_process.template_path
                    sift_match_override_val = sim_process.sift_match_override_val
                    timeout                 = sim_process.timeout
                    exit_on_match           = sim_process.exit_on_match

                    DEFAULT_TIMEOUT = 120
                    if timeout == None: timeout = DEFAULT_TIMEOUT
                    verified = self.verify_screen(template_path=template_path, timeout=timeout, ml_match_override=sift_match_override_val)
                    
                    if verified == False:
                        
                        # AUTOFIX: Auto-return to home screen with menu
                        if process_name == "base_screen_with_menu":
                            self.return_to_base_menu_screen
                            continue
                        
                        starrail_log(f"Screen verification failed {process_name}", log_type="error"); time.sleep(3)
                        self.return_to_base_menu_screen()
                        return False
                    elif (verified == True) and (exit_on_match == True):
                        return True
                    
                    continue # Screen verification success
                
                
                # ===========================================
                # ==========| CLICK KEYBOARD KEY |===========
                # ===========================================
                elif isinstance(sim_process, KeyboardProcess):
                    process_name = sim_process.sprocess_name
                    self.click_keyboard_key(process_name)
                
                
                # ==========================================
                # =======| SIMULATE MOUSE MOVEMENT |========
                # ==========================================
                elif isinstance(sim_process, MouseProcess):
                    process_name            = sim_process.sprocess_name
                    template_path           = sim_process.template_path
                    sift_match_override_val = sim_process.sift_match_override_val
                    secondary_template_path = sim_process.secondary_template_path
                    mouse_correction_offset = sim_process.mouse_correction
                    
                    while True:
                        # Take Screenshot
                        self.screenshot_controller.take_screenshot()
                        
                        # Match Image
                        screenshot_abspath = self.screenshot_controller.get_screenshot_path()
                        _, M, coords = self.image_matcher.match_image(
                            template_path, 
                            screenshot_abspath, 
                            visualize_match=False, 
                            override_threshold=sift_match_override_val,
                            secondary_template=secondary_template_path
                        )
                        
                        if coords != None: # Found match
                            self.mouse_controller.move_mouse_to_button(coords, correction_x=mouse_correction_offset[0], correction_y=mouse_correction_offset[1])
                            self.mouse_controller.click_mouse()
                            self.mouse_controller.move_mouse_to_button((0, 0), duration=0.1)
                            break
                        else:
                            continue # Continues to match

                        
                # ==========================================
                # ============| END LOGIC MAP |=============
                # ==========================================
                elif isinstance(sim_process, EndProcess):
                    starrail_log("End of current process map."); time.sleep(5)
                    return True
    
        except Exception as ex:
            print(ex.args); sys.stdout.flush(); time.sleep(10)
            
        return False
    
    # def run_logic_map(self, logic_map: dict):
    #     from elevate import elevate; elevate() # Elevate permission to move mouse in-game
    #     assert(isinstance(logic_map, dict))

    #     try:            
    #         for process_header, process_meta in logic_map.items():
    #             process_count, process_type, process_name = process_header.split()
    #             print(process_count, process_type, process_name)
                
    #             if process_meta == None:
    #                 pass # Ignore process_meta that are None
    #             else:
    #                 template_path           = process_meta['path']
    #                 match_offset            = process_meta['offset'] # Mouse position correction (x, y) from the center
    #                 ml_override_value       = process_meta['match_override_val']
    #                 secondary_template_path = process_meta['secondary_path']
                
                
    #             # ==========================================
    #             # ==========| PROCESS EXECUTION |===========
    #             # ==========================================
    #             if process_type == "[execute]":
    #                 executed_base_process = self.execute_process(process_name)
    #                 if executed_base_process: # Process executed successfully
    #                     continue
    #                 else:
    #                     raise StarRailBaseException(f"Attempted to execute a process that is not found. {process_name}")
                
                
    #             # ============================================
    #             # ==========| SCREEN VERIFICATION |===========
    #             # ============================================
    #             elif process_type == "[verify]":
    #                 verified = self.verify_screen(template_path=template_path, timeout=120, ml_match_override=ml_override_value)
    #                 if verified == False:
    #                     starrail_log(f"Screen verification failed {process_type} {process_name}", log_type="error")
    #                     time.sleep(3)
                        
    #                     self.return_to_base_menu_screen()
    #                     return False
    #                     # raise StarRailBaseException(f"Screen verification failed. Process: {process_header}")
    #                 continue # Screen verification success
                
                
    #             # ===========================================
    #             # ==========| CLICK KEYBOARD KEY |===========
    #             # ===========================================
    #             elif process_type == "[keyboard]":
    #                 self.click_keyboard_key(process_name)
                
                
    #             # ==========================================
    #             # =======| SIMULATE MOUSE MOVEMENT |========
    #             # ==========================================
    #             elif process_type == "[mouse]":
                    
    #                 while True:
    #                     # Take Screenshot
    #                     self.screenshot_controller.take_screenshot()
                        
    #                     # Match Image
    #                     screenshot_abspath = self.screenshot_controller.get_screenshot_path()
    #                     visualization, M, coords = self.image_matcher.match_image(
    #                         template_path, 
    #                         screenshot_abspath, 
    #                         visualize_match=False, 
    #                         override_threshold=ml_override_value,
    #                         secondary_template=secondary_template_path
    #                     )
                        
    #                     if coords != None: # Found match
    #                         self.mouse_controller.move_mouse_to_button(coords, correction_x=match_offset[0], correction_y=match_offset[1])
    #                         self.mouse_controller.click_mouse()
    #                         self.mouse_controller.move_mouse_to_button((0, 0), duration=0.1)
    #                         break
    #                     else:
    #                         continue # Continues to match
                        
                        
    #             # ==========================================
    #             # ============| END LOGIC MAP |=============
    #             # ==========================================
    #             elif process_type == "[end]":
    #                 starrail_log("End of current process map.")
    #                 time.sleep(5)
    #                 return True
                
    #     except Exception as ex:
    #         print(ex.args); sys.stdout.flush(); time.sleep(10)
            
    #     return False


    # =========================================
    # ======| HELPER LOGIC FUNCTIONS | ========
    # =========================================

    def return_to_base_menu_screen(self):
        starrail_log("Returning to home screen...")
        while True:
            verified_screen = self.verify_screen(BASE_MENU_SCREEN_PATH, timeout=0)
            if not verified_screen:
                # Click esc key
                self.click_keyboard_key(process_name="exit_page"); time.sleep(2)
                
                # Click exit button
                self.screenshot_controller.take_screenshot()
                screenshot_abspath = self.screenshot_controller.get_screenshot_path()
                _, _, coords = self.image_matcher.match_image(EXIT_BTN_PATH, screenshot_abspath)
                if coords != None:
                    self.mouse_controller.move_mouse_to_button(coords)
                    self.mouse_controller.click_mouse()
                    self.mouse_controller.move_mouse_to_button((0, 0), duration=0.1)
            else: break

    def check_out_of_stamina(self):
        starrail_log("Checking for out-of-stamina...")
        return self.verify_screen(OUT_OF_STAMINA_PATH, timeout=0)
    
    
    # =========================================
    # ======| HELPER UTILS FUNCTIONS | ========
    # =========================================
    def execute_process(self, process_name):
        # Function for executing processes that requires no CV2 screen matching
        if process_name == "start_game":
            starrail_log("Starting game...")
            self.game_instance.run()
            time.sleep(10)
            return True
        return False
        
        
    def verify_screen(self, template_path, timeout=120, ml_match_override=None):
        # Verify screen instance (with timeout=0)
        if timeout == 0:
            self.screenshot_controller.take_screenshot()
            screenshot_abspath = self.screenshot_controller.get_screenshot_path()
            _, _, coords = self.image_matcher.match_image(template_path, screenshot_abspath, visualize_match=False, override_threshold=ml_match_override)
            return coords != None
    
        # Verify screen with timeout loop
        start_time = time.time()
        while time.time() - start_time < timeout:
            self.screenshot_controller.take_screenshot()
            screenshot_abspath = self.screenshot_controller.get_screenshot_path()
            _, _, coords = self.image_matcher.match_image(template_path, screenshot_abspath, visualize_match=False, override_threshold=ml_match_override)
            if coords is not None: # Match found, return True                
                return True
        return False
    
    
    def click_keyboard_key(self, process_name):
        # Function for executing processes that requires no CV2 screen matching
        if process_name == "open_menu" or process_name == "exit_page":
            self.keyboard_controller.click_esc()