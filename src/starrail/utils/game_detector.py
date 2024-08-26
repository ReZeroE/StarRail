import os
import sys
import string
from pathlib import Path
from concurrent import futures
from multiprocessing import Manager

from starrail.constants import GAME_FILENAME, GAME_FILE_PATH
from starrail.exceptions.exceptions import *


class StarRailGameDetector:
    """
    Honkai Star Rail Game Detector - Finds the game on local drives
    """
    def get_local_drives(self):
        available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
        return available_drives

    def find_game_in_path(self, path, name, stop_flag):
        for root, _, files in os.walk(path):
            if stop_flag.value: # Check the shared flag value.
                return None
            
            # If game file in the directory
            if name in files:
                # Check if the game's entire path is in the path found
                abs_path = os.path.join(root, name)
                if os.path.normpath(GAME_FILE_PATH) in abs_path:
                    return os.path.join(root, name)
        return None

    def find_game(self, paths=[], name=GAME_FILENAME):
        for p in paths:
            if not os.path.exists(p):
                raise StarRailBaseException(f"Path does not exist. [{p}]")

        if len(paths) == 0:
            paths = self.get_local_drives()

        paths = [f"{path}\\" if path.endswith(":") and len(path) == 2 else path for path in paths]

        worker_threads = 1
        if os.cpu_count() > 1:
            worker_threads = os.cpu_count() - 1

        with futures.ProcessPoolExecutor(max_workers=worker_threads) as executor, Manager() as manager:
            stop_flag = manager.Value('b', False)   # Create a boolean shared flag.
            future_to_path = {executor.submit(self.find_game_in_path, path, name, stop_flag): path for path in paths}
            for future in futures.as_completed(future_to_path):
                result = future.result()
                if result is not None:
                    stop_flag.value = True # Set the flag to true when a result is found.
                    return result
        return None
