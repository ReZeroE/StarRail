import time
import threading
import tkinter as tk
import asyncio
from pynput import mouse, keyboard

from starrail.constants import RECORDER_WINDOW_INFO, CALIBRATION_MONITOR_INFO
from starrail.automation.units.action import Action, MouseAction, KeyboardAction, ScrollAction
from starrail.automation.units.sequence import AutomationSequence
from starrail.automation.pixel_calculator.resolution_detector import ResolutionDetector

from starrail.utils.utils import *
from starrail.exceptions.exceptions import *
from starrail.controllers.star_rail_app import HonkaiStarRail


'''
MouseAction
    1. Action delay
ScrollAction
    1. Action delay
KeyboardAction:
    1. Action delay
    2. Hold time (0.9.0)
'''

class AutomationRecorder():
    def __init__(self, sequence: AutomationSequence, starrail_instance: HonkaiStarRail):
        self.sequence = sequence
        self.starrail = starrail_instance
        
        self.label              = None
        self.prev_action_time   = None
        self.is_recording       = False
        self.stop_event         = threading.Event()

        self.keyboard_key      = None
        self.keyboard_press_time = None
    
    
    def create_indicator_window(self):
        LENGTH, WIDTH, RADIUS = self.__scale_window(RECORDER_WINDOW_INFO['height'], RECORDER_WINDOW_INFO['width'], RECORDER_WINDOW_INFO["border-radius"])
        
        root = tk.Tk()
        root.title("Waiting for game to be focused...")
        root.geometry(f"{WIDTH}x{LENGTH}+0+0")
        root.overrideredirect(True)  # Remove window decorations

        root.attributes('-topmost', True) # STAY ON TOOOOOPPPPPP

        # Set the overall background color to black and then make it transparent
        background_color = 'black'
        root.configure(bg=background_color)
        root.attributes('-transparentcolor', background_color)

        canvas = tk.Canvas(root, bg=background_color, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Replace 'black' with the color of your choice for the rounded rectangle
        canvas_color = '#333333'
        canvas.create_polygon(
            [
                RADIUS,             0,                  WIDTH - RADIUS,     0, 
                WIDTH,              RADIUS,             WIDTH,              LENGTH - RADIUS, 
                WIDTH - RADIUS,     LENGTH,             RADIUS,             LENGTH, 
                0,                  LENGTH - RADIUS,    0,                  RADIUS
            ],
            smooth=True, fill=canvas_color)

        self.label = tk.Label(canvas, text="Waiting for game to be focused...", font=('Helvetica', 9), fg='#FFFFFF', bg=canvas_color)
        self.label.place(relx=0.4, rely=0.5, anchor='center')

        button_width = 120
        button_height = 70
        button_width, button_height, _ = self.__scale_window(button_width, button_height)
        stop_button = tk.Button(canvas, text='Stop\nRecording', font=('Helvetica', 10), command=lambda: self.stop_recording(root), bg='#14628c', fg='#FFFFFF')
        stop_button.place(relx=0.85, rely=0.5, anchor='center', width=button_width, height=button_height)
    
        # Mouse movement handling
        def on_press(event):
            root._drag_start_x = event.x
            root._drag_start_y = event.y

        def on_drag(event):
            dx = event.x - root._drag_start_x
            dy = event.y - root._drag_start_y
            x = root.winfo_x() + dx
            y = root.winfo_y() + dy
            root.geometry(f"+{x}+{y}")

        root.bind('<Button-1>', on_press)
        root.bind('<B1-Motion>', on_drag)

        self.label.config(text=f"Waiting for game to be focused...")

        root.mainloop()
    
    
    # =============================================
    # ===============| BASE DRIVER | ==============
    # =============================================
    
    def stop_recording(self, root: tk.Tk):
        self.stop_event.set()
        self.is_recording = False
        self.sequence.actions = self.sequence.actions[:-1]    # Remove the last key click (user clicks on the Stop Recording button)
        root.quit()
        
    def pause_or_resume_recording(self):
        self.is_recording = not self.is_recording
        
    def record(self, start_on_callback=False) -> AutomationSequence:
        threading.Thread(target=self.create_indicator_window, daemon=True).start()
        
        if start_on_callback:
            self.is_recording = True
            self.prev_action_time = None
            aprint(f"Ready to record.\n{Printer.to_lightblue(" - To start")}: Focus onto the game and the recording will automatically start.\n{Printer.to_lightblue(" - To stop")}:  Click 'Stop Recording' on the top-left corner of the screen.")
        else:
            raise Exception("Record must start on callback. Other case not implemented.")
        
        # mouse_listener = mouse.Listener(on_click=self.__on_mouse_action)
        # keyboard_listener = keyboard.Listener(on_press=self.__on_keyboard_action)
        
        with mouse.Listener(on_click=self.__on_mouse_action, on_scroll=self.__on_scroll_action) as mouse_listener, \
            keyboard.Listener(on_press=self.__on_keyboard_action_press, on_release=self.__on_keyboard_action_release) as keyboard_listener:
            
            mouse_listener_thread     = threading.Thread(target=mouse_listener.join)
            keyboard_listener_thread  = threading.Thread(target=keyboard_listener.join)
            
            mouse_listener_thread.start()
            keyboard_listener_thread.start()

            # Wait until stop recording event is triggered
            self.stop_event.wait()

            # Stop listeners
            mouse_listener.stop()
            keyboard_listener.stop()

            # Wait for listeners to finish
            mouse_listener_thread.join()
            keyboard_listener_thread.join()

        time.sleep(0.3)
        return self.sequence
    
    
    # =============================================
    # ============| ON-ACTION DRIVER | ============
    # =============================================
    
    def __on_mouse_action(self, x, y, button, pressed):
        '''
        On mouse action is executed twice:
            1. when the mouse is pressed
            2. when the mouse is released
            
        The application is only focused on-release, therefore we need to ignore the on-press action.
        As of version 0.9.0, hold-time has not been implemented.
        '''
        if pressed or not self.starrail.is_focused():
            return
        
        if self.is_recording:
            now = time.time()
            delay = now - self.prev_action_time if self.prev_action_time else float(0)
            clicked = button == mouse.Button.left # If left is clicked, the click is registered as "clicked", else if right is clicked, only the mouse movement will be registered.
            self.sequence.add(MouseAction((x, y), delay, clicked, ResolutionDetector.get_foreground_window_size()))
            self.prev_action_time = now
            self.on_mouse_action_update_window(x, y, delay)


    def __on_scroll_action(self, x, y, dx, dy):
        if not self.starrail.is_focused():
            return
        
        if self.is_recording:
            now = time.time()
            delay = now - self.prev_action_time if self.prev_action_time else float(0)
            self.sequence.add(ScrollAction((x, y), dx, dy, delay, ResolutionDetector.get_foreground_window_size()))
            self.prev_action_time = now
            self.on_scroll_action_update_window(x, y, dx, dy, delay)


    '''
    Key hold_time has been implemented as of 0.9.0 and there are a few key notes.
        1. Only one key will be recorded at a time. No key or key-mouse combination is supported.
        2. When a new key is pressed with the previous key not yet released, the new key will be completely ignored until the release of the previous key.
    '''
    def __on_keyboard_action_press(self, key):
        # NOTE: This function will be executed repeatedly during a key-hold by the keyboard listener (aka param key will remain the same on every iteration).
        
        # If the current key is the same as the previous key, continue.
        if key == self.keyboard_key:
            pass
        # If there is already an press-regeistered key but it's not the current key (a new key is pressed while the
        # previous key has not been released), do not register this new key.
        elif self.keyboard_key != None and key != self.keyboard_key:
            pass
        # New key pressed.
        else:
            self.keyboard_key = key
            self.keyboard_press_time = time.time()

    def __on_keyboard_action_release(self, key):
        # If key released is not the press-registered key, then ignore this key
        if key != self.keyboard_key:
            return
        
        # If the app is unfocused, reset the press-registered key and time
        if not self.starrail.is_focused():
            self.keyboard_key = None
            self.keyboard_press_time = None
            return
        
        # Pause/resume listener on Enter key press
        elif key == keyboard.Key.space:
            self.keyboard_key = None
            self.keyboard_press_time = None
            self.pause_or_resume_recording()
            return  # Return to not record this space key press

        # Record only if is_recording is set to True
        if self.is_recording:
            now         = time.time()
            hold_time   = now - self.keyboard_press_time
            delay       = now - self.prev_action_time - hold_time if self.prev_action_time else float(0)
            
            self.sequence.add(KeyboardAction(key, delay, hold_time))
            self.prev_action_time = now
            self.keyboard_key = None
            self.keyboard_press_time = None
            self.on_keyboard_action_update_window(key, delay, hold_time)




    # =============================================
    # ============| UPDATE UI WINDOW | ============
    # =============================================

    def on_mouse_action_update_window(self, x, y, delay):
        if self.label:
            self.__update_label(text=f"Mouse Click Detected - ({x}, {y})\nDelay: {round(delay, 2)}")
            
    def on_scroll_action_update_window(self, x, y, dx, dy, delay):
        if self.label:
            if dy > 0:
                self.__update_label(text=f"Scroll Detected - ({x}, {y}) - Scrolled UP\nDelay: {round(delay, 2)}")
            elif dy < 0:
                self.__update_label(text=f"Scroll Detected - ({x}, {y}) - Scrolled DOWN\nDelay: {round(delay, 2)}")
            else:
                self.__update_label(text="Scroll Detected - Horizontal scroll not supported.")

    def on_keyboard_action_update_window(self, key, delay, hold_time):
        if self.label:
            try:
                self.__update_label(text=f"Key Detected - '{key.char}'\nDelay: {round(delay, 2)}, Hold: {round(hold_time, 2)}")
            except AttributeError:
                self.__update_label(text=f"Key Detected - '{key}'\nDelay: {round(delay, 2)}, Hold: {round(hold_time, 2)}")
    
    def on_pause_action_update_window(self):
        if self.is_recording:
            self.__update_label(text=f"Recording resumed...")
        else:
            self.__update_label(text=f"Recording paused...")
            

    def __update_label(self, text: str):
        self.label.place(relx=0.4, rely=0.6, anchor='center')
        self.label.config(text=f"Total Actions Recorded: {len(self.sequence.actions)}\n{text}\n")

    def __scale_window(self, standard_width, standard_height, standard_radius=None):
        monitor_info = ResolutionDetector.get_primary_monitor_size()
        width_ratio  = monitor_info["width"]  / CALIBRATION_MONITOR_INFO["width"]
        height_ratio = monitor_info["height"] / CALIBRATION_MONITOR_INFO["height"]
        
        if standard_radius != None:
            radius = standard_radius * ((width_ratio+height_ratio)/2)
        else:
            radius = 0
        
        return int(standard_width*width_ratio), int(standard_height*height_ratio), int(radius)