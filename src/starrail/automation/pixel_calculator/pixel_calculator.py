from starrail.utils.utils import aprint, LogType
from starrail.automation.pixel_calculator.resolution_detector import ResolutionDetector

class PixelCalculator:
    def __init__(self, monitor_info: dict):
        self.prev_monitor_width = monitor_info["width"]
        self.prev_monitor_height = monitor_info["height"]
    
        current_monitor_info = ResolutionDetector.get_primary_monitor_size()
        self.current_monitor_width = current_monitor_info["width"]
        self.current_monitor_height = current_monitor_info["height"]
    
    
    @staticmethod
    def transform_coordinate(prev_coor: tuple, prev_window_info: dict):
        try:
            x, y = prev_coor
            
            curr_window_info = ResolutionDetector.get_foreground_window_size()
            curr_x = curr_window_info["left"]
            curr_y = curr_window_info["top"]
            curr_w = curr_window_info["width"]
            curr_h = curr_window_info["height"]
            
            # print(curr_x, curr_y, curr_w, curr_h)
            
            prev_x = prev_window_info["left"]
            prev_y = prev_window_info["top"]
            prev_w = prev_window_info["width"]
            prev_h = prev_window_info["height"]
            
            # Normalize the coordinate relative to the original window
            normalized_x = (x - prev_x) / prev_w
            normalized_y = (y - prev_y) / prev_h

            new_x = curr_x + normalized_x * curr_w
            new_y = curr_y + normalized_y * curr_h

            return (int(new_x), int(new_y))
    
        except KeyError:
            # Unavailable for pixel calculator (ver 0.0.2)
            return prev_coor
