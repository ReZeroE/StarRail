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

from .._utils._utils import *
from .._exceptions._exceptions import *
from ._config.config_handler import ConfigHandler
from ..honkai_star_rail import HonkaiStarRail

class StarRailCommandLineEndPoints:
    def __init__(self):
        self.instance = self.__create_instance()
        self.config_handler = ConfigHandler()
        self.supported_commands = [
            "start",
            "stop",
            "restart",
            "info",
            "set-path",
            "configure"
        ]
        
        self.__verify_config()
        
    
    def configure(self, on_error=False):
        config_handler = ConfigHandler()
        
        # Config chart already displayed on error
        if not on_error:
            self.__display_config()
        
        # Disclaimer ================================================================================
        rprint("\n - STEP 1. DISCLAIMER AGREEMENT - ", "cyan")
        disclaimer_read = config_handler.get_disclaimer_status()
        if not disclaimer_read:
            print_disclaimer()
            
            rprint("[IMPORTANT] Please read the disclaimer above before continuing!", "warning")
            if input("AGREE? [y/n] ").lower() == "y":
                config_handler.set_disclaimer_status()
            else: exit()
        
        # Setup game path ============================================================================
        rprint("\n - STEP 2. SET UP GAME PATH (StarRail.exe) -", "cyan")
        
        game_path_configured = config_handler.get_game_path() != None
        if not game_path_configured:
        
            example = """
    Example Path:
        D:\Honkai Star Rail\Star Rail\Game\StarRail.exe
        
    Note: Please make sure it's an absolute path to the game's executable StarRail.exe
            
            """
            
            print("\n Please provide the absolute path to the game Honkai: Star Rail (to the file StarRail.exe).")
            print(example)
            game_path = input("Honkai Star Rail Path: ")
            reformatted_path = self.__reformat_path(game_path)
            config_handler.set_game_path(reformatted_path)

        # Create StarRail game instance ================================================================
        # self.__display_config()
        self.instance = self.__create_instance()
    
    
    def start_game(self) -> bool:
        self.instance.run()
    
    def terminate_game(self) -> bool:
        config_handler = ConfigHandler()
        
        instance_pid = config_handler.get_game_instance_pid()
        if instance_pid != None:
            running_process = psutil.Process(config_handler.get_game_instance_pid())
            self.instance = HonkaiStarRail(config_handler.get_game_path(), running_process)
            return self.instance.terminate()
        return False
    
    def restart_game(self) -> bool:
        return self.start_game() and self.terminate_game()
    
    def configure_game(self):
        self.configure()
    
    
    # ======================================
    # ======== | Helper Functions | ========
    # ======================================
    
    def __create_instance(self):
        try:
            config_handler = ConfigHandler()
            game_path = config_handler.get_game_path()
            return HonkaiStarRail(game_path)
        except StarRailGameNotFoundException:
            return None
        
    def __verify_config(self):    
        self.__display_config()
        
        # ==================================
        # ========| Verify Config | ========
        # ==================================
        # Game path not provided -> game instance == None
        if self.instance == None:
            user_input = input("Start configuring `starrail`? [y/n] ")
            if user_input.lower() == "y":
                self.configure(on_error=True)
            else:
                print("Canceled."); exit()


    def __display_config(self):
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
        game_path_empty = config_handler.get_game_path() == None
        if game_path_empty:
            game_path_set = incompleted_text
        
        headers = ["Configuration", "Status"]
        config_table = [
            ["Disclaimer Agreement",  disclaimer_status],
            ["StarRail Path Setup",       game_path_set]
        ]
        
        # Print config table
        print(colored("\n ----- STARRAIL MODULE CONFIG ----- ", "cyan"))
        try:
            print(tabulate(config_table, headers, tablefmt="fancy_outline") + "\n")
        except UnicodeEncodeError:
            print(tabulate(config_table, headers, tablefmt="outline") + "\n")


    def __reformat_path(self, input_path):
        input_path = input_path.strip()
        print(os.path.basename(input_path))
        return input_path

        
def execute_command():
    config_handler = ConfigHandler()
    endpoint_handler = StarRailCommandLineEndPoints()

    # ======================================
    # ======== | Setup Arg Parser | ========
    # ======================================
    
    parser = argparse.ArgumentParser(prog='starrail', description="Commandline Honkai Star Rail Automation Tool")

    subparsers = parser.add_subparsers(dest='command')
    for command in endpoint_handler.supported_commands:
        subparsers.add_parser(command)

    # =====================================
    # ======== | Parse Arguments | ========
    # =====================================
    args = parser.parse_args()
    
    #  ==================================== -> START GAME
    if args.command == 'start':
        starrail_log("Starting game...", log_type="info"); time.sleep(1)
        endpoint_handler.start_game()
        config_handler.set_game_instance_pid(endpoint_handler.instance.process.pid)
        starrail_log(f"[PID{config_handler.get_game_instance_pid()}] Game Started!", log_type="info")

    #  ==================================== -> STOP GAME
    elif args.command == 'stop':
        starrail_log("Terminating game...", log_type="info")
        try:
            endpoint_handler.terminate_game()
        except psutil.AccessDenied:
            pass
        config_handler.set_game_instance_pid(None)
        
    #  ==================================== -> RESTART GAME
    elif args.command == 'restart':
        starrail_log("Restarting game...", log_type="info")
        endpoint_handler.restart_game()
       
    #  ==================================== -> CONFIGURE GAME 
    elif args.command == "configure":
        endpoint_handler.configure_game()


if __name__ == "__main__":
    pass
        
    