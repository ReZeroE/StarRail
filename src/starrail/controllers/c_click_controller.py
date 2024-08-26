import time
import pyautogui
import random
from pynput import keyboard
from threading import Event

from starrail.exceptions.exceptions import SRExit
from starrail.utils.utils import aprint, Printer, is_admin, color_cmd
from starrail.constants import BASENAME

class ContinuousClickController:
    def __init__(self):
        self.thread_event = Event()
        self.pause = False
        self.click_count = 0


    def click_continuously(
        self,
        count: int          = -1,
        interval: float     = 1.0,
        randomize_by: float = 0.0,
        hold_time: float    = 0.1,
        start_after: float  = 5.0,
        quiet: bool         = False
    ):
        self.__verbose_start(count, interval, randomize_by, hold_time, start_after, quiet)

        listener = keyboard.Listener(on_press=self.__on_press)
        listener.start()
        
        time.sleep(start_after)
        try:
            while True:
                if self.click_count == count or self.thread_event.is_set():
                    listener.stop()
                    break
                elif self.pause:
                    time.sleep(0.1)
                    continue

                if not quiet:
                    self.__verbose_click(count)

                self.__click(hold_time, interval, randomize_by)

        except KeyboardInterrupt:
            print("")
            listener.stop()
            time.sleep(1)
            raise SRExit()


    def __click(self, hold_time, interval, randomize_interval):
        self.click_count += 1
        
        pyautogui.mouseDown()
        time.sleep(hold_time)
        pyautogui.mouseUp()
        
        time.sleep(interval)
        time.sleep(random.uniform(0, randomize_interval))


    def __verbose_start(self, count, interval, randomize_by, hold_time, start_after, quiet):
        title_text = Printer.to_lightblue(f"Uniform clicking starting in {start_after} seconds.")
        stop_text = Printer.to_lightblue(" - To stop:  ") + "Press CTRL+C or ESC"
        pause_text = Printer.to_lightblue(" - To pause: ") + "Press SPACE"
        count_text = "INFINITE" if count == -1 else str(count)
        count_text = Printer.to_purple(" - Total clicks:   ") + count_text
        interval_text = Printer.to_purple(" - Click interval: ") + f"{interval} seconds"
        if randomize_by > 0:
            interval_text += f" + random(0, {randomize_by}) seconds"
        hold_time_text = Printer.to_purple(" - Hold duration:  ") + f"{hold_time} seconds"
        
        warning_text = ""
        if not is_admin():
            warning_text = Printer.to_lightred(f"\n\nNote: Currently not running {BASENAME} as admin. Clicks will not work in game applications.")
            ccmd = color_cmd("starrail elevate", with_quotes=True)
            warning_text += Printer.to_lightred(f"\n      Run ") + ccmd + Printer.to_lightred(f" to elevate permissions to admin.")
        
        aprint(
            f"{title_text} \
            \n{stop_text} \
            \n{pause_text} \
            \n\n{count_text} \
            \n{hold_time_text} \
            \n{interval_text} \
            {warning_text}\n"
        )

    def __verbose_click(self, max_count):
        buffer          = " " * 10
        x, y            = pyautogui.position()
        max_count_text  = "INF" if max_count == -1 else max_count
        aprint(f"[Count {self.click_count + 1}/{max_count_text}] Clicking ({x}, {y})...{buffer}", end="\r")


    def __on_press(self, button):
        if button == keyboard.Key.esc:
            if self.click_count > 0:
                print("")
            aprint("Esc key pressed, stopping...")
            self.thread_event.set()
            exit() # After the event is set, the listener thread termiantes

        if button == keyboard.Key.space:
            self.pause = not self.pause

            buffer = " " * 7
            if self.pause:
                aprint(f"Clicks paused. Press space again to start.{buffer}", end="\r")
            else:
                aprint(f"Clicks unpaused. Press space again to pause.{buffer}", end="\r")

