import subprocess
from starrail.utils.utils import *
import signal
import time
import psutil

class StarRailPermissionsHandler:
    @staticmethod
    def elevate(arguments: list = []):
        ARGUMENTS = " ".join([str(arg) for arg in arguments])
        try:
            # \k keeps the terminal open after the user exits the starrail cli env
            cmd_command = f'cmd /k "{COMMAND} {ARGUMENTS}"'
            result = subprocess.run(["powershell", "-Command", f'Start-Process cmd -ArgumentList \'/k {cmd_command}\' -Verb RunAs'])
            
            if result.returncode == 0:
                print("")
                aprint(Printer.to_lightgreen(f"Admin permission granted.") + f"\nPlease use the new terminal with the {SHORTNAME}-CLI that opened.")
            else:
                aprint(f"Command 'starrail elevate' permission denied.", log_type=LogType.ERROR)
            
        except Exception as e:
            aprint(f"Failed to elevate privileges: {e}")
        
        time.sleep(3)
        cmd_proc_id = psutil.Process(os.getppid()).ppid()
        kill_command = f'taskkill /F /PID {cmd_proc_id}'
        os.system(kill_command)
        
    
    @staticmethod
    def elevate_post_cli(follow_up_cmd: str):
        try:
            # \k keeps the terminal open after the user exits the starrail cli env
            cmd_command_1 = f'cmd /k "{COMMAND}"'
            combined_commands = f"{cmd_command_1} && {follow_up_cmd}"
            result = subprocess.run([
                "powershell", 
                "-Command", 
                f'Start-Process cmd -ArgumentList \'/k "{combined_commands}"\' -Verb RunAs'
            ])
            
            if result.returncode == 0:
                aprint(f"Permissions granted. Please use the new terminal with the {SHORTNAME}-CLI that opened.")
            else:
                aprint(f"Command 'starrail elevate' permission denied.", log_type=LogType.ERROR)
            
        except Exception as e:
            aprint(f"Failed to elevate privileges: {e}")