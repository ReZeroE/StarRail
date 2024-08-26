import psutil
import time
import ctypes
import subprocess

from starrail.utils.utils import *

class ProcessHandler:
    
    @staticmethod
    def get_focused_pid():
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        hwnd = user32.GetForegroundWindow()
        pid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        return pid.value
    
    
    @staticmethod
    def get_related_processes(process_pid: int):
        process = psutil.Process(process_pid)
        if not process.is_running():
            return None, None
        
        parent_procs: list[psutil.Process] = []
        children_procs: list[psutil.Process] = []
               
        try:
            parent_procs = process.parents()
            children_procs = process.children(recursive=True)
        except:
            pass

        return parent_procs, children_procs
    
    
    @staticmethod
    def kill_pid(pid, verbose_failure=True, is_child=False):
        
        process_info = f"process {pid}" if not is_child else f"child process {pid}"
        try:
            proc = psutil.Process(pid)
            if proc.is_running():
                proc.kill(); time.sleep(0.1)
                
                aprint(f"Process {proc.name()} (PID {proc.pid}) terminated successfully.", submodule_name="ProcHandler")
                return True
        
        except psutil.NoSuchProcess:
            if verbose_failure:
                aprint(f"Unabled to terminate {process_info} because it's already closed.", log_type=LogType.ERROR, submodule_name="ProcHandler")
        except Exception as ex:
            if verbose_failure:
                aprint(f"Unabled to terminate {process_info} ({ex}).", log_type=LogType.ERROR, submodule_name="ProcHandler")
        return False

    
    @staticmethod
    def kill_pid_and_residual(pid):
        try:
            proc = psutil.Process(pid)
            child_procs = []
            try:
               child_procs = proc.children(recursive=True)
            except:
                pass
        except psutil.NoSuchProcess:
            aprint(f"Unabled to terminate root process {pid} because it's already closed.", log_type=LogType.WARNING, submodule_name="ProcHandler")
            return
        
        ProcessHandler.kill_pid(pid, verbose_failure=True)
        
        for cproc in child_procs:
            if cproc.is_running():
                ProcessHandler.kill_pid(cproc.pid, verbose_failure=False, is_child=True)
                time.sleep(0.5)