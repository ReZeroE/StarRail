
import os
import sys
import time
import tabulate

from starrail.utils.utils import *

from starrail.automation.units.sequence import AutomationSequence
from starrail.automation.recorder import AutomationRecorder
from starrail.automation.config.automation_config_handler import StarRailAutomationConfig
from starrail.controllers.star_rail_app import HonkaiStarRail

class StarRailAutomationController:
    def __init__(self, starrail_instance: HonkaiStarRail):
        self.automation_config = StarRailAutomationConfig()
        self.automation_sequences: dict[int, AutomationSequence] = self.__load_all_sequences()
    
        self.starrail = starrail_instance # Only used by recorder to identify if the game is focused.
    
    def __load_all_sequences(self):
        sequence_list: list[AutomationSequence] = []
        
        sequence_config_list = self.automation_config.load_all_automations()
        for config in sequence_config_list:
            sequence = AutomationSequence.parse_config(config)
            sequence_list.append(sequence)
            
        sequence_list.sort(key=lambda seq: seq.date_created)
        return {idx+1: sequence for idx, sequence in enumerate(sequence_list)}
    
    def verbose_general_usage(self):
        headers = [Printer.to_lightpurple(title) for title in ["Example Command", "Description"]]
        data = [
            [color_cmd("automation record"),    "Create and record a new automation sequence (macros)"],
            [color_cmd("automation show"),      "List all recorded automation sequences"],
            [color_cmd("automation run"),       "Run a recorded automation sequence"],
            [color_cmd("automation remove"),    "Delete a recorded automated sequence"],
        ]
        
        tab = tabulate.tabulate(data, headers)
        print("\n" + tab + "\n")
    
    
    # =============================================
    # ============| FETCH AUTOMATION | ============
    # =============================================
    
    def get_all_sequences(self, list_format=False):
        if list_format:
            return list(self.automation_sequences.values())
        return self.automation_sequences
    
    def get_sequence(self, sequence_name: str):
        target_sequence_name = self.__reformat_sequence_name(sequence_name)
        for sequence in self.automation_sequences.values():
            if sequence.sequence_name == target_sequence_name:
                return sequence
        return None
    
    def get_sequence_with_id(self, sequence_id: int):
        try:
            return self.automation_sequences[sequence_id]
        except KeyError:
            return None
    
    
    # =============================================
    # ============| DRIVER FUNCTIONS | ============
    # =============================================
    
    def run_requence(self, sequence_name=None):
        if len(self.automation_sequences) == 0:
            aprint(f"{Printer.to_lightred('No automation sequence has been recorded.')}")
            self.verbose_general_usage()
            return
        
        sequence = None
        
        if sequence_name:
            r_sequence_name = self.__reformat_sequence_name(sequence_name)
            sequence = self.get_sequence(r_sequence_name)
            if sequence == None:
                aprint(f"Invalid input. No sequence with name {sequence_name}.")
                raise SRExit()
            
        else:
            self.show_sequences()
            aprint(f"Which sequence would you like to run? ({self.get_range_string()}) ", end="")
            user_input_id = input("")
            
            sequence = self.get_sequence_with_id(self.tryget_int(user_input_id))
            if sequence == None:
                aprint(f"Invalid input. No sequence with ID {user_input_id}.")
                raise SRExit()
    
        aprint(f"Run automation '{sequence.sequence_name}' ({Printer.to_lightgrey(f'approximately {sequence.get_runtime()} seconds')})? [y/n] ", end="")
        user_input = input("").strip().lower()
        if user_input != "y": return
        
        aprint(f"Automation run ready start.\n{Printer.to_lightblue(' - To start')}: Focus on the game and the automation will automatically start.")
        while True:
            if self.starrail.is_focused():
                time.sleep(1)
                break
            else:
                time.sleep(0.5)
        
        sequence.execute()
        aprint("Automation sequence run complete!                                                            ")
    
    def show_sequences(self):
        headers = [Printer.to_lightpurple(title) for title in ["ID", "Sequence Name", "Date Created",  "Runtime", "Actions Count"]]
        data = []
        for seq_id, sequence in self.automation_sequences.items():
            row = [Printer.to_lightblue(seq_id), sequence.sequence_name, sequence.date_created, f"{sequence.get_runtime()} seconds", len(sequence.actions)]
            data.append(row)
        
        tab = tabulate.tabulate(data, headers)
        print("\n" + tab + "\n", flush=True)
    
    def record_sequences(self, sequence_name=None):
        if sequence_name == None:
            aprint("New sequence name: ", end="") 
            sequence_name = input("").strip()
        
        # Initialize empty automation sequence for storing recording
        NEW_SEQUENCE_NAME = self.__reformat_sequence_name(sequence_name)
        if self.__sequence_already_exist(NEW_SEQUENCE_NAME):
            aprint(f"Sequence with name '{NEW_SEQUENCE_NAME}' {Printer.to_lightred('already exist')}.")
            raise SRExit()
        
        recording_sequence = AutomationSequence(NEW_SEQUENCE_NAME)                  
        recording_sequence.set_date_created_to_current()
        
        # Start recording
        try:
            action_recorder = AutomationRecorder(recording_sequence, self.starrail)
            action_recorder.record(start_on_callback=True)
        except Exception as ex:
            aprint(f"Uncaught Error (during recording): {ex}")
            raise SRExit()
        
        # TODO: Auto refactor the recorded sequence such that consecutive holds are merged.
        
        # Convert recorded sequence into JSON and save it as config
        json_sequence = recording_sequence.to_json()
        success = self.automation_config.save_automation(recording_sequence.sequence_name, json_sequence)
        assert(success == True)
        
        # Cache recorded sequence in memory
        sequence_id = self.get_next_sequence_id()
        self.automation_sequences[sequence_id] = recording_sequence

        aprint(f"Recording complete. Saved as '{Printer.to_light_blue(recording_sequence.sequence_name)}' (ID {sequence_id}).\n{Printer.to_lightblue(' - To view')}: {color_cmd('automation show')}\n{Printer.to_lightblue(' - To run')}:  {color_cmd(f'automation run')}")
        return recording_sequence
    
    def delete_sequence(self):
        if len(self.automation_sequences) == 0:
            aprint("No automation sequence has been recorded.")
            raise SRExit()

        self.show_sequences()
        aprint(f"Which sequence would you like to delete? ({self.get_range_string()}) ", end="")
        user_input_id = input("")
        
        seq_id = self.tryget_int(user_input_id)
        sequence = self.get_sequence_with_id(seq_id)
        if sequence == None:
            aprint(f"Invalid input. No sequence with ID {user_input_id}.")
            raise SRExit()
    
        self.automation_config.delete_automation(sequence.sequence_name)
        del self.automation_sequences[seq_id]
        aprint(f"Automation sequence `{sequence.sequence_name}` has been deleted.")
        
    def clear_sequences(self):
        if len(self.automation_sequences) == 0:
            aprint("No automation sequence has been recorded.")
            raise SRExit()

        self.show_sequences()
        aprint(f"Are you sure you would like to clear all {len(self.automation_sequences)} automation sequences? [y/n] ", end="")
        user_input = input("").strip().lower()
        if user_input == "y":
            for sequence in self.automation_sequences.values():
                aprint(f"Deleting automation sequence '{sequence.sequence_name}' ...")
                self.automation_config.delete_automation(sequence.sequence_name)
            self.automation_sequences.clear()
            
        aprint("All automation sequences have been deleted.")
    

    # =============================================
    # ============| HELPER FUNCTIONS | ============
    # =============================================

    def tryget_int(self, user_input_id):
        if isinstance(user_input_id, str):
            try:
                seq_id = int(user_input_id)
            except TypeError:
                aprint(f"Invalid input: {user_input_id}", log_type=LogType.ERROR)
                raise SRExit()
        elif isinstance(user_input_id, int):
            seq_id = user_input_id
        return seq_id

    def __sequence_already_exist(self, r_sequence_name):
        for seq in self.automation_sequences.values():
            if seq.sequence_name == r_sequence_name:
                return True
        return False

    def get_range_string(self):
        if len(self.automation_sequences) <= 1:
            return "ID 1"
        return f"ID {min(self.automation_sequences.keys())}-{max(self.automation_sequences.keys())}"
    
    def get_next_sequence_id(self):
        if len(self.automation_sequences) == 0:
            return 1
        return max(self.automation_sequences.keys()) + 1
    
    def __reformat_sequence_name(self, sequence_name: str):
        return sequence_name.strip().replace(" ", "-").lower()