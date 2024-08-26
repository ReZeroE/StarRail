

import re
import os
import tabulate
from starrail.utils.utils import *

SUBMODULE_NAME = "SR-DB"

class StarRailBinaryDecoder:
    def __init__(self):
        self.decoded_count = 0
    
    def decode_raw_binary_file(self, file_path, min_length=8):
        """
        Extract readable strings from a binary file.
        Expecting length > given min_length parameter.
        
        :param file_path: Path to the binary file
        :param min_length: Minimum length of strings to extract
        :return: list of extracted strings
        """
        with open(file_path, 'rb') as file:
            binary_content = file.read()
        
        # Use regular expression to find readable strings
        pattern = re.compile(b'[ -~]{%d,}' % min_length)
        strings = pattern.findall(binary_content)
        
        # Decode bytes to strings
        decoded_strings = [s.decode('utf-8', errors='ignore') for s in strings]
        self.decoded_count += 1
        return decoded_strings

    def user_decode(self, file_path=None, min_length=8):
        if not file_path:
            aprint("Binary File Path: ", end="")
            user_input = input("").strip().lower().replace("\"", "")
            if not os.path.isfile(user_input):
                aprint(Printer.to_lightred(f"Invalid path: {user_input}"))
                return
            file_path = user_input
        
        results = []
        try:
            results = self.decode_raw_binary_file(file_path, min_length)
        except Exception:
            aprint(f"File cannot be decoded.", submodule_name=SUBMODULE_NAME)
        
        if len(results) == 0:
            aprint("No results are found.", submodule_name=SUBMODULE_NAME)
            return
        
        headers = [Printer.to_purple(title) for title in ["Index", "Content"]]
        data = [[Printer.to_lightblue(idx), content] for idx, content in enumerate(results)]
        print(tabulate.tabulate(data, headers))