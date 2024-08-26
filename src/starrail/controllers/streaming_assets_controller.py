import os
import re
import sys
from pathlib import Path

from enum import Enum
from starrail.config.config_handler import StarRailConfig

from starrail.utils.utils import aprint, Printer
from starrail.constants import WEBCACHE_IGNORE_FILETYPES
from starrail.utils.binary_decoder import StarRailBinaryDecoder


SUBMODULE_NAME = "SR-SAC"


class StarRailStreamingAssetsBinaryFile(Enum):
    SA_BinaryVersion    = "BinaryVersion.bytes"
    SA_ClientConfig     = "ClientConfig.bytes"
    SA_DevConfig        = "DevConfig.bytes"   


class StarRailStreamingAssetsController:
    def __init__(self, starrail_config: StarRailConfig):
        self.starrail_config = starrail_config
        self.binary_decoder = StarRailBinaryDecoder()
        
    # =============================================
    # ============| DRIVER FUNCTIONS | ============
    # =============================================
    
    def get_decoded_streaming_assets(self, sa_binary_file: StarRailStreamingAssetsBinaryFile):
        decoded_strings = self.decode_streaming_assets(sa_binary_file)
        if decoded_strings == None:
            return None
        
        filtered_dict = self.parse_webcache(decoded_strings, sa_binary_file)
        return filtered_dict
        

    def get_sa_binary_version(self):
        return self.get_decoded_streaming_assets(StarRailStreamingAssetsBinaryFile.SA_BinaryVersion)
    
    def get_sa_client_config(self):
        return self.get_decoded_streaming_assets(StarRailStreamingAssetsBinaryFile.SA_ClientConfig)
    
    def get_sa_dev_config(self):
        return self.get_decoded_streaming_assets(StarRailStreamingAssetsBinaryFile.SA_DevConfig)
    
    
    # =============================================
    # ==========| SUBDRIVER FUNCTIONS | ===========
    # =============================================
    
    def decode_streaming_assets(self, sa_binary_file: StarRailStreamingAssetsBinaryFile):
        file_path = os.path.join(self.starrail_config.root_path, "Game", "StarRail_Data", "StreamingAssets", sa_binary_file.value)
        aprint(f"Decoding {Printer.to_lightgrey(file_path)} ...", submodule_name=SUBMODULE_NAME)
        
        if Path(file_path).exists():
            return self.binary_decoder.decode_raw_binary_file(file_path)
        return None
    
    
    def parse_webcache(self, decoded_strings, sa_binary_file: StarRailStreamingAssetsBinaryFile):
        data_dict = dict()
        
        if sa_binary_file == StarRailStreamingAssetsBinaryFile.SA_BinaryVersion:
            for string in decoded_strings:
                string = string.strip()
                
                if re.search("PRODWin[0-9]{1}.[0-9]{1}.[0-9]{1}", string) != None:
                    data_dict["Detailed Version"] = string
                
                elif re.search("V[0-9]{1}.[0-9]{1}", string) != None:
                    data_dict["Version"] = string
                
                elif re.search("[0-9]{8}-[0-9]{4}", string) != None:
                    data_dict["Datetime String"] = string
                    
                else:
                    try:
                        endpoints = data_dict["Other"]
                        endpoints.append(string)
                        data_dict["Other"] = endpoints
                    except KeyError:
                        data_dict["Other"] = [string]
        
        
        if sa_binary_file == StarRailStreamingAssetsBinaryFile.SA_ClientConfig:
            for string in decoded_strings:
                string = string.strip()
                
                match = re.search("https.*", string)
                if string.startswith("com."):
                    data_dict["Application Identifier"] = string
                
                
                elif match != None:
                    try:
                        endpoints = data_dict["Server Endpoints"]
                        endpoints.append(match.group(0))
                        data_dict["Service Endpoints"] = endpoints
                    except KeyError:
                        data_dict["Service Endpoints"] = [match.group(0)]
                
                else:
                    try:
                        endpoints = data_dict["Unknown"]
                        endpoints.append(string)
                        data_dict["Unknown"] = endpoints
                    except KeyError:
                        data_dict["Unknown"] = [string]  
                        

        if sa_binary_file == StarRailStreamingAssetsBinaryFile.SA_DevConfig:
            for string in decoded_strings:
                string = string.strip()
                
                if re.search("V[0-9]{1}.[0-9]{1}", string) != None:
                    
                    if "EngineRelease" in string:
                        data_dict["Engine Version"] = string
                    else:
                        data_dict["Unknown Version"] = string
                
                else:
                    try:
                        endpoints = data_dict["Unknown"]
                        endpoints.append(string)
                        data_dict["Unknown"] = endpoints
                    except KeyError:
                        data_dict["Unknown"] = [string]
        
        
        if len(data_dict) > 0:
            return data_dict
        return None
    