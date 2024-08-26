import time
import win32process
import pygetwindow
from ctypes import windll
from screeninfo import get_monitors
from win32gui import GetWindowRect, GetForegroundWindow

from starrail.exceptions.exceptions import *
from starrail.utils.process_handler import ProcessHandler


class ResolutionDetector:
    windll.user32.SetProcessDPIAware()
    
    @staticmethod
    def get_primary_monitor_size() -> dict:
        monitors = get_monitors()
        for m in monitors:
            if m.is_primary:
                monitor_info = {
                    "width": m.width,
                    "height": m.height
                }
                return monitor_info
        return None

    @staticmethod
    def get_foreground_window_size():
        window_size = GetWindowRect(GetForegroundWindow())
        monitor_size = ResolutionDetector.get_primary_monitor_size()
        return {
            'left'          : window_size[0],
            'top'           : window_size[1],
            'width'         : window_size[2],
            'height'        : window_size[3],
            'is_fullscreen' : window_size[2] == monitor_size["width"] and window_size[2] == monitor_size["height"]
        }

    @staticmethod
    def get_window_size():
        pid = ProcessHandler.get_focused_pid()
        # print(f"Currently focused PID: {pid}")
        if pid == None: return None
        
        win_info: dict = ResolutionDetector.get_window_info(pid)
        if win_info == None:
            raise Exception(f"Failed to fetch window size. No results returned (PID {pid}).")
        
        monitor_info = ResolutionDetector.get_primary_monitor_size()
        
        if  monitor_info["width"] == win_info["width"] and \
            monitor_info["height"] == win_info["height"] and \
            win_info["top"] == 0 and win_info["left"] == 0:
            
            win_info["is_fullscreen"] = True
        else:
            win_info["is_fullscreen"] = False
            
        return win_info


    @staticmethod
    def get_window_info(pid, retry: int = 5):
        for _ in range(retry):
            windows = pygetwindow.getWindowsWithTitle('')  # Get all windows
            for window in windows:
                _, window_pid = win32process.GetWindowThreadProcessId(window._hWnd)
                if window_pid == pid:
                    if (window.left >= 0 and window.top >= 0) and (window.width > 0 and window.height > 0):
                        return {
                            'left'          : window.left,
                            'top'           : window.top,
                            'width'         : window.width,
                            'height'        : window.height,
                            'is_fullscreen' : None
                        }
            time.sleep(1)
        return None
        
    
    
