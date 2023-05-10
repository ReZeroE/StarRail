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

import sys
import time
import psutil
import argparse
from tabulate import tabulate
from termcolor import colored
from colorama import init; init() 

from .._utils._utils import *
from .._bin.loader.loader import Loader 
from .._exceptions._exceptions import *
from .._config.config_handler import ConfigHandler
from ..honkai_star_rail import HonkaiStarRail


class StarRailCommandLineEndPoints:
    def __init__(self):
        self.instance = self.__create_instance()
        self.config_handler = ConfigHandler()
        self.supported_commands = {
            "start":            "Start game from command-line",
            "stop":             "Stop game from command-line (the game instance must be started with 'starrail start')",
            "restart":          "Restart the game from command-line",
            "configure":        "Configure the 'starrail' module (once after installation)",
            "set-path":         "Set game's path in 'starrail' (overwrites previously set path)",
            "show-config":      "Display configuration status"
        }
        
        
    # =========================================
    # ======== | Endpoints Functions | ========
    # =========================================
    
    def configure(self, on_error=False):
        def user_agreement():
            disclaimer_read = config_handler.get_disclaimer_status()
            if not disclaimer_read:
                # os.system("cls")
                rprint("\n\n - STEP 1 OF 2. DISCLAIMER AGREEMENT - ", "info")
                print_disclaimer()
                
                rprint("[IMPORTANT] Please read the disclaimer above before continuing!", "warning")
                if input("AGREE? [y/n] ").lower() == "y":
                    config_handler.set_disclaimer_status()
                else: exit()
                
                return True # Configuration complete
            return False # Already configured
        
        def configure_path():
            game_path_configured = verify_game_path(config_handler.get_game_path())
            if not game_path_configured:
                # os.system("cls")
                rprint("\n\n - STEP 2 OF 2. SET UP GAME PATH (StarRail.exe) -\n", "info")
                
                # Set path in configuration
                self.auto_detect_game_path()
                
                return True # Configuration complete
            return False # Already configured
        
        
        config_handler = ConfigHandler()
        
        # Config chart already displayed on error
        if not on_error:
            self.display_config()
        
        ua_configured = user_agreement()
        p_configured = configure_path()

        if ua_configured and p_configured:
            starrail_log("Configuration Completed.", log_type="success")
        else:
            starrail_log("Configuration Already Complete.", log_type="success")
            
        exit()
        # self.instance = self.__create_instance()

    def start_game(self) -> bool:
        self.instance.run()
    
    def terminate_game(self) -> bool:
        config_handler = ConfigHandler()
        
        instance_pid = config_handler.get_game_instance_pid()
        if instance_pid != None:
            running_process = psutil.Process(config_handler.get_game_instance_pid())
            self.instance = HonkaiStarRail(config_handler.get_game_path(), running_process)
            return self.instance.terminate(), instance_pid
        return False, instance_pid
    
    def restart_game(self) -> bool:
        return self.start_game() and self.terminate_game()
    
    def configure_game(self):
        self.configure()

    def display_config(self):
        config_handler = ConfigHandler()
        
        # =================================
        # ========| Config Table | ========
        # =================================
        # Config table data initialization
        completed_text =    colored("Completed", color="green")
        incompleted_text =  colored("Incompleted", color="red")
        
        disclaimer_status = completed_text
        disclaimer_completed = config_handler.get_disclaimer_status()
        if not disclaimer_completed:
            disclaimer_status = incompleted_text
        
        game_path_set = completed_text
        game_path_configured = verify_game_path(config_handler.get_game_path())
        if not game_path_configured:
            game_path_set = incompleted_text
        
        headers = ["Configuration", "Status"]
        config_table = [
            ["User Agreement",      disclaimer_status],
            ["StarRail Path Setup", game_path_set]
        ]
        
        # Print config table
        rprint("\n ----- STARRAIL MODULE CONFIG ----- ", "info")
        try:
            print(tabulate(config_table, headers, tablefmt="fancy_outline") + "\n")
        except UnicodeEncodeError:
            print(tabulate(config_table, headers, tablefmt="outline") + "\n")


    # =========================================
    # ========= | Endpoints Helpers | =========
    # =========================================

    def configure(self, on_error=False):
        def user_agreement():
            disclaimer_read = config_handler.get_disclaimer_status()
            if not disclaimer_read:
                # os.system("cls")
                rprint("\n\n - STEP 1 OF 2. DISCLAIMER AGREEMENT - ", "info")
                print_disclaimer()
                
                rprint("[IMPORTANT] Please read the disclaimer above before continuing!", "warning")
                if input("AGREE? [y/n] ").lower() == "y":
                    config_handler.set_disclaimer_status()
                else: exit()
                
                return True # Configuration complete
            return False # Already configured
        
        def configure_path():
            game_path_configured = verify_game_path(config_handler.get_game_path())
            if not game_path_configured:
                # os.system("cls")
                rprint("\n\n - STEP 2 OF 2. SET UP GAME PATH (StarRail.exe) -\n", "info")
                
                # Set path in configuration
                self.auto_detect_game_path()
                
                return True # Configuration complete
            return False # Already configured
        
        
        config_handler = ConfigHandler()
        
        # Config chart already displayed on error
        if not on_error:
            self.display_config()
        
        ua_configured = user_agreement()
        p_configured = configure_path()

        if ua_configured and p_configured:
            starrail_log("Configuration Completed.", log_type="success")
        else:
            starrail_log("Configuration Already Complete.", log_type="success")
            
        exit()
        # self.instance = self.__create_instance()

    def auto_detect_game_path(self):
        config_handler = ConfigHandler()
        
        logt = starrail_log_text("Locating Honkai: Star Rail (this may take a while)...")
        with Loader(logt, end=None):
            game_path = self.__safe_find_game()
            print("\n" + starrail_log_text(f"Game found at: {game_path}"))
            config_handler.set_game_path(game_path)

    def set_path(self, is_called_on_endpoint=False):
        config_handler = ConfigHandler()
        
        # Display Header
        if is_called_on_endpoint:
            os.system("cls")
            rprint(" ----- STARRAIL SET PATH -----\n", "info")
        
        # Print set-path examples + explanations
        print_path_config_ex()
        
        AUTO_SELECT_KEY = "auto-detect"
        ct = rtext("Auto-Detect", "warning")
        ct_key = rtext(AUTO_SELECT_KEY, "warning")
        print(f"\nTo {ct} the location of the game, enter {ct_key}. Else, enter the path to the game.")

        game_path = input("Enter the path to Honkai Star Rail:\n>>> ")
        # AUTO DETECTING
        if game_path.strip().lower() == AUTO_SELECT_KEY:
            self.auto_detect_game_path()
        
        # MANUAL ENTERING
        else:
            reformatted_path = self.__reformat_path(game_path)
            logt = starrail_log_text(f"Searching for Honkai: Star Rail at {reformatted_path}...")
            with Loader(logt, end=None):
                game_path = self.__safe_find_game([reformatted_path])
                starrail_log("\n" + f"Game found at: {game_path}")
                config_handler.set_game_path(game_path)
        
        # If called on endpoint, display PATH SET confirmation
        if is_called_on_endpoint:
            starrail_log("Game path set successfully.", "success")
    
    def verify_config(self):    
        config_handler = ConfigHandler()
        # Game path not provided -> game instance == None
        has_valid_path = verify_game_path(config_handler.get_game_path())
        has_read_disclaimer = config_handler.get_disclaimer_status()
        
        if has_valid_path == False or has_read_disclaimer == False:
            self.display_config()
            user_input = input("Start configuring `starrail`? [y/n] ")
            if user_input.lower() == "y":
                self.configure(on_error=True)
            else:
                print("Canceled."); exit()
    
    
    # ======================================
    # ======== | Helper Functions | ========
    # ======================================
    
    def __safe_find_game(self, input_paths=[]):
        """
        Find game in the given paths.
        Safe: raises exception if game not found. 
        """
        if isinstance(input_paths, str):
            raise StarRailBaseException("__saft_find_game needs to be provided with a list of paths, not str.")
        
        detector = StarRailGameDetector()
        if len(input_paths) == 0:
            paths_to_search = detector.get_local_drives()
        else:
            paths_to_search = input_paths
        
        game_path = detector.find_game(
            paths=paths_to_search, 
            name=GAME_DEFAULT
        )
        
        if game_path != None: 
            return game_path
        else:
            print("")
            starrail_log(f"Game ({GAME_DEFAULT}) not found in {paths_to_search} , Existing.", "error")
            exit()
    
    def __create_instance(self):
        try:
            config_handler = ConfigHandler()
            game_path = config_handler.get_game_path()
            return HonkaiStarRail(game_path)
        except StarRailGameNotFoundException:
            return None

    def __reformat_path(self, input_path):
        input_path = input_path.strip()
        return input_path


def execute_command():
    config_handler = ConfigHandler()
    endpoint_handler = StarRailCommandLineEndPoints()

    # ======================================
    # ======== | Setup Arg Parser | ========
    # ======================================
    
    parser = argparse.ArgumentParser(prog='starrail', description="Commandline Honkai Star Rail Automation Tool")

    subparsers = parser.add_subparsers(dest='command')
    for command, desc in endpoint_handler.supported_commands.items():
        subparsers.add_parser(command, description=desc)

    # =====================================
    # ======== | Parse Arguments | ========
    # =====================================
    args = parser.parse_args()
    
    #  ================================================================= -> START GAME
    if args.command == 'start':
        endpoint_handler.verify_config()
        
        starrail_log("Starting game...")
        time.sleep(1)
        endpoint_handler.start_game()
        config_handler.set_game_instance_pid(endpoint_handler.instance.process.pid)
        starrail_log(f"[PID {config_handler.get_game_instance_pid()}] Game Started!")

    #  ================================================================= -> STOP GAME
    elif args.command == 'stop':
        endpoint_handler.verify_config()
        
        starrail_log("Terminating game...")
        try:
            success, pid = endpoint_handler.terminate_game()
        except psutil.AccessDenied or PermissionError:
            pass
        config_handler.set_game_instance_pid(None)
        
    #  ================================================================= -> RESTART GAME
    elif args.command == 'restart':
        endpoint_handler.verify_config()
        
        starrail_log("Restarting game...")
        endpoint_handler.restart_game()
       
    #  ================================================================= -> CONFIGURE GAME 
    elif args.command == "configure":
        endpoint_handler.configure_game()
        
    #  ================================================================= -> SET NEW PATH FOR GAME 
    elif args.command == "set-path":
        endpoint_handler.set_path(is_called_on_endpoint=True)
        
    #  ================================================================= -> SHOW STARRAIL CONFIG 
    elif args.command == "show-config":
        endpoint_handler.display_config()

