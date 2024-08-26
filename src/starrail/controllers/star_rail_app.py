
import os
import sys
import time
import psutil
import tabulate
import webbrowser
import subprocess
import configparser
from pathlib import Path

from starrail.utils.utils import *
from starrail.utils.process_handler import ProcessHandler
from starrail.config.config_handler import StarRailConfig
from starrail.controllers.webcache_controller import StarRailWebCacheController, StarRailWebCacheBinaryFile
from starrail.controllers.streaming_assets_controller import StarRailStreamingAssetsController, StarRailStreamingAssetsBinaryFile

from starrail.bin.loader.loader import Loader 

class HonkaiStarRail:
    def __init__(self):
        self.config = StarRailConfig()
        self.module_configured = self.config.full_configured()
        
        self.webcache_controller = StarRailWebCacheController(self.config)
        self.streaming_assets_controller = StarRailStreamingAssetsController(self.config)
    
    
    # =============================================
    # ============| DRIVER FUNCTIONS | ============
    # =============================================
    
    def start(self) -> bool:
        aprint("Starting Honkai: Star Rail...")
        starrail_proc = self.get_starrail_process()
        
        # If the application is already running
        if starrail_proc != None and starrail_proc.is_running():
            ctext = Printer.to_lightred("already running")
            aprint(f"[PID {starrail_proc.pid}] Application `{starrail_proc.name()}` is {ctext} in the background.")
            raise SRExit()

        # If the application is not running, then start the application
        success = subprocess.Popen([str(self.config.game_path)], shell=True)
        if self.wait_to_start():
            starrail_proc = self.get_starrail_process()
            aprint(f"[PID {starrail_proc.pid}] Honkai: Star Rail has started successfully!")
            return True

        aprint(f"Honkai: Star Rail failed to start due to an unknown reason.")
        return False

    def terminate(self):
        aprint("Terminating Honkai: Star Rail...", end="\r")
        
        # If the cached proc PID is working
        if self.config.instance_pid != None:
            try:
                starrail_proc = psutil.Process(self.config.instance_pid)
                if self.proc_is_starrail(starrail_proc):
                    starrail_proc.terminate()
                    aprint("Honkai: Star Rail terminated successfully.")
                    return True
            except psutil.NoSuchProcess:
                self.config.instance_pid = None
                self.config.save_current_config()
        
        # If no PID is cached, find proc and termiante
        starrail_proc = self.get_starrail_process()
        if starrail_proc != None:
            starrail_proc.terminate()
            aprint("Honkai: Star Rail terminated successfully.")
            return True
        
        aprint(f"Honkai: Star Rail is currently {Printer.to_lightred('not running')}.      ")
        return False

    def schedule(self):
        # Scheduler implement seperately in starrail/bin as of version 1.0.0.
        ...



    # =============================================
    # ===========| UTILITY FUNCTIONS | ============
    # =============================================

    def show_status(self):
        aprint("Loading status for the Honkai: Star Rail process...")
        
        starrail_proc = self.get_starrail_process()
        headers = [Printer.to_lightblue(title) for title in ["Title", "HSR Real-time Status"]]
        
        if starrail_proc != None: # Is running
            data = [
                ["Status",          bool_to_str(starrail_proc.is_running())],
                ["Process ID",      starrail_proc.pid],
                ["Started On",      DatetimeHandler.epoch_to_time_str(starrail_proc.create_time())],
                ["CPU Percent",     f"{starrail_proc.cpu_percent(1)}%"],
                ["CPU Affinity",    ",".join([str(e) for e in starrail_proc.cpu_affinity()])],
                ["IO Operations",   f"Writes: {starrail_proc.io_counters().write_count}, Reads: {starrail_proc.io_counters().read_count}"],
                ["RAM Usage",       f"{round(psutil.virtual_memory()[3]/1000000000, 2)} GB"]
            ]
        else:
            data = [
                ["Status",          bool_to_str(False)],
                ["Process ID",      "None"],
                ["Started On",      "None"],
                ["CPU Percent",     "None"],
                ["CPU Affinity",    "None"],
                ["IO Operations",   "None"]
            ]
            
        for row in data:
            row[0] = Printer.to_lightpurple(row[0])
            
        table = tabulate.tabulate(data, headers=headers)
        print("\n" + table + "\n")
            
    def show_config(self):
        # print(Printer.to_lightpurple("\n - Game Configuration Table -"))
        headers = [Printer.to_lightblue(title) for title in ["Title", "Details", "Relevant Command"]]
        data = [
            ["Game Version", self.fetch_game_version(), color_cmd("starrail version")],
            ["Game Executable", os.path.normpath(self.config.game_path), color_cmd("starrail start/stop")],
            ["Game Screenshots", self.__get_screenshot_path(), color_cmd("starrail screenshots")],
            ["Game Logs", self.__get_log_path(), color_cmd("starrail game-logs")],
            ["Game (.exe) SHA256", HashCalculator.SHA256(self.config.game_path) if self.config.game_path.exists() else None, ""]
        ]
        for row in data:
            row[0] = Printer.to_lightpurple(row[0])
        
        table = tabulate.tabulate(data, headers=headers)
        print("\n" + table + "\n")
        
    def screenshots(self):
        aprint("Opening the screenshots directory...", end="\r")
        screenshot_path = self.__get_screenshot_path()
        os.startfile(screenshot_path)
        aprint(f"Screenshots directory opened in the File Explorer ({Printer.to_lightgrey(screenshot_path)}).")

    def logs(self):
        aprint("Opening the logs directory...", end="\r")
        logs_path = self.__get_log_path()
        os.startfile(logs_path)
        aprint(f"Logs directory opened in the File Explorer ({Printer.to_lightgrey(logs_path)}).")

    def show_pulls(self):
        aprint("Showing the pull history page...", end="\r")
        cache_urls = self.webcache_controller.get_events_cache()
        if cache_urls == None:
            aprint("No pull history cache found locally.")
            return
        
        for url in cache_urls:
            webbrowser.open(url)
            
        aprint("All pages opened successfully.      ")
        
    def verbose_play_time(self):
        sr_proc = self.get_starrail_process()
        if sr_proc == None:
            aprint("Honkai: Star Rail is currently not running.")
            return
        
        ctime = sr_proc.create_time()
        time_delta = datetime.now() - DatetimeHandler.epoch_to_datetime(ctime)    
        aprint(f"{Printer.to_lightblue('Session Time:')} {DatetimeHandler.seconds_to_time_str(time_delta.seconds)}")


    # =============================================
    # ==========| WEBCACHE FUNCTIONS | ============
    # =============================================

    def webcache_announcements(self):
        aprint("Decoding announcement webcache...")
        cache_urls = self.webcache_controller.get_announcements_cache()
        
        if cache_urls == None:
            aprint("No announcement webcache found.")
        else:
            self.__print_cached_urls(cache_urls)

    def webcache_events(self):
        aprint("Decoding events/pulls webcache...")
        cache_urls = self.webcache_controller.get_events_cache()
        
        if cache_urls == None:
            aprint("No events webcache found.")
        else:
            self.__print_cached_urls(cache_urls)

    def webcache_all(self):
        e_cache_urls = self.webcache_controller.get_events_cache()
        a_cache_urls = self.webcache_controller.get_announcements_cache()

        if e_cache_urls == None and a_cache_urls == None:
            aprint("No available webcache found.")
        else:
            print("")

        new_line = False
        if e_cache_urls != None:
            new_line = True
            print(Printer.to_lightblue(" - Events/Pulls Web Cache -"))
            self.__print_cached_urls(e_cache_urls)
        
        if a_cache_urls != None:
            if new_line:
                print("")
            print(Printer.to_lightblue(" - Announcements Web Cache -"))
            self.__print_cached_urls(a_cache_urls)
    
    def __print_cached_urls(self, url_list):
        for idx, url in enumerate(url_list):
            print(f"[{Printer.to_lightpurple(f'URL {idx+1}')}] " + url)



    # =================================================
    # ========| STREAMING ASSETS FUNCTIONS | ==========
    # =================================================
    
    def streaming_assets(self):
        aprint("Decoding streaming assets...")
        
        headers = [Printer.to_lightblue(title) for title in ["Title", "Details (binary)"]]
        
        sa_binary_dict = self.streaming_assets_controller.get_sa_binary_version()
        sa_client_dict = self.streaming_assets_controller.get_sa_client_config()
        sa_dev_dict = self.streaming_assets_controller.get_sa_dev_config()
        
        master_dict = merge_dicts(sa_binary_dict, sa_client_dict, sa_dev_dict)
        
        if len(master_dict) > 0:
            master_list = [[Printer.to_lightpurple(title), "\n".join(data) if isinstance(data, list) else data] for title, data in master_dict.items() if title != "Other"]
            if "Other" in master_dict.keys():
                data = master_dict["Other"]
                master_list.append([Printer.to_lightpurple("Other"), "\n".join(data) if isinstance(data, list) else data])
            
            table = tabulate.tabulate(master_list, headers)
            print("\n" + table + "\n")
        


    # =============================================
    # =========| PATH HELPER FUNCTIONS | ==========
    # =============================================
    
    def __get_screenshot_path(self):
        return os.path.normpath(os.path.join(self.config.root_path, "Game", "StarRail_Data", "ScreenShots"))

    def __get_log_path(self):
        return os.path.normpath(os.path.join(self.config.root_path, "logs"))

    def __get_game_config_path(self):
        return os.path.normpath(os.path.join(self.config.root_path, "Game", "config.ini"))
    
    def fetch_game_version(self):
        config = configparser.ConfigParser()
        config.read(self.__get_game_config_path())
        game_version = config.get('General', 'game_version')
        return game_version
    
    
    
    # =============================================
    # ======| START/STOP HELPER FUNCTIONS | =======
    # =============================================
    
    def wait_to_start(self, timeout = 30) -> bool:
        starting_time = time.time()
        while time.time() - starting_time < timeout:
            if self.is_running():
                return True
            time.sleep(0.5)
        return False

    def is_running(self) -> bool:
        return self.get_starrail_process() != None
    
    def is_focused(self) -> bool:
        hsr_proc = self.get_starrail_process()
        if hsr_proc == None:
            return False
        
        focused_pid = ProcessHandler.get_focused_pid()
        if hsr_proc.pid == focused_pid:
            return True
        return False
    
    def get_starrail_process(self) -> psutil.Process:
        EXE_BASENAME = os.path.basename(self.config.game_path)
        
        for p in psutil.process_iter(['pid', 'name', 'exe']):
            # name == EXE_BASENAME is for optimization only (proceed only if filename is the same)
            if p.info["name"] == EXE_BASENAME:

                    try:
                        starrail_proc = psutil.Process(p.info['pid'])
                        if self.proc_is_starrail(starrail_proc):
                            
                            # If the cached PID isn't the current PID, reset it
                            if self.config.instance_pid != starrail_proc.pid:
                                self.config.instance_pid = starrail_proc.pid
                                self.config.save_current_config()
                            
                            return starrail_proc
                    
                    except psutil.NoSuchProcess:
                        continue
        return None
    
    def proc_is_starrail(self, starrail_proc: psutil.Process):
        return starrail_proc.is_running() and Path(starrail_proc.exe()) == Path(self.config.game_path)



    