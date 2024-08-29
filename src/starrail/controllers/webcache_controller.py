
import os
import re
import sys
import shutil
from pathlib import Path

from enum import Enum
from starrail.config.config_handler import StarRailConfig

from starrail.utils.utils import aprint, Printer
from starrail.constants import WEBCACHE_IGNORE_FILETYPES
from starrail.utils.binary_decoder import StarRailBinaryDecoder


SUBMODULE_NAME = "SR-WCC"


class StarRailWebCacheBinaryFile(Enum):
    WEBCACHE_DATA0 = "data_0"
    WEBCACHE_DATA1 = "data_1"   # Anncouncements
    WEBCACHE_DATA2 = "data_2"   # Events/Pulls


class StarRailWebCacheController:
    def __init__(self, starrail_config: StarRailConfig):
        self.starrail_config = starrail_config
        self.binary_decoder = StarRailBinaryDecoder()
        
    # =============================================
    # ============| DRIVER FUNCTIONS | ============
    # =============================================
    
    def get_decoded_webcache(self, webcache_binary_file: StarRailWebCacheBinaryFile):
        decoded_strings = self.decode_webcache(webcache_binary_file)
        if decoded_strings == None:
            return None
        
        filtered_urls = self.parse_webcache(decoded_strings, webcache_binary_file)
        return filtered_urls
        
    def get_announcements_cache(self):
        return self.get_decoded_webcache(StarRailWebCacheBinaryFile.WEBCACHE_DATA1)
    
    def get_events_cache(self):
        return self.get_decoded_webcache(StarRailWebCacheBinaryFile.WEBCACHE_DATA2)
    
    
    # =============================================
    # ==========| SUBDRIVER FUNCTIONS | ===========
    # =============================================

    def decode_webcache(self, webcache_binary_file: StarRailWebCacheBinaryFile):

        # Get webCache path (varying webcache versioning)
        def get_webcache_path():
            webcache_path = ""
            webcache_semi_path = Path(os.path.join(self.starrail_config.innr_path, "StarRail_Data", "webCaches"))
            
            try:
                version_dirs = [d for d in webcache_semi_path.iterdir() if d.is_dir()]
                if len(version_dirs) > 0:
                    version_dir = version_dirs[0]
                    webcache_path = os.path.join(self.starrail_config.innr_path, "StarRail_Data", "webCaches", version_dir, "Cache", "Cache_Data", webcache_binary_file.value)
                    return webcache_path
                else:
                    return None
            except Exception as ex:
                return None

        file_path = get_webcache_path()
        if file_path == None or not os.path.isfile(file_path):
            return None
        
        aprint(f"Decoding {webcache_binary_file.value} ({Printer.to_lightgrey(file_path)}) ...", submodule_name=SUBMODULE_NAME)
        
        try:
            return self.binary_decoder.decode_raw_binary_file(file_path)
        except PermissionError:
            aprint(f"{Printer.to_lightred('Web cache is LOCKED.')} Web cache is only available when the game is not running.", submodule_name=SUBMODULE_NAME)
        return None
    
    
    def parse_webcache(self, decoded_strings, webcache_file: StarRailWebCacheBinaryFile):
        if webcache_file == StarRailWebCacheBinaryFile.WEBCACHE_DATA0:
            pass
        if webcache_file == StarRailWebCacheBinaryFile.WEBCACHE_DATA1:
            return self.filter_urls("webstatic.mihoyo.com/hkrpg/announcement", decoded_strings)
        if webcache_file == StarRailWebCacheBinaryFile.WEBCACHE_DATA2:
            return self.filter_urls("webstatic.mihoyo.com/hkrpg/event", decoded_strings)
        return None
    
    # =============================================
    # ============| HELPER FUNCTIONS | ============
    # =============================================
    
    def filter_urls(self, target_sequence: str, decoded_strings):
        # Filter out URLs without the target sequence and end with the ignoring file types
        filtered_urls = []
        for url in decoded_strings:
            url = url.strip()
            if target_sequence in url and not self.should_ignore(url):
                match = re.search("https.*", url)
                if match != None:
                    filtered_urls.append(match.group(0)) 
        return filtered_urls
    
    
    def should_ignore(self, url: str):
        # Should ignore current URL because of its file type
        for ignoring_file_type in WEBCACHE_IGNORE_FILETYPES:
            if url.endswith(ignoring_file_type):
                return True
        return False