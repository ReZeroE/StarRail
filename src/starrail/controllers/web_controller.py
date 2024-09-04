
import webbrowser
from starrail.constants import HOMEPAGE_URL, HOMEPAGE_URL_CN, HOYOLAB_URL, YOUTUBE_URL, BILIBILI_URL
from starrail.utils.utils import aprint, Printer

class StarRailWebController:
    def __init__(self):
        pass
    
    def homepage(self, cn=False):
        if cn:
            aprint(f"Opening Honkai: Star Rail's official home page (CN)...\n - {Printer.to_lightgrey(HOMEPAGE_URL_CN)}")
            webbrowser.open(HOMEPAGE_URL_CN)
        else:
            aprint(f"Opening Honkai: Star Rail's official home page...\n - {Printer.to_lightgrey(HOMEPAGE_URL)}")
            webbrowser.open(HOMEPAGE_URL)
        
    def hoyolab(self):
        aprint(f"Opening Honkai: Star Rail's HoyoLab page...\n - {Printer.to_lightgrey(HOYOLAB_URL)}")
        webbrowser.open(HOYOLAB_URL)
        
    def youtube(self):
        aprint(f"Opening Honkai: Star Rail's Youtube page...\n - {Printer.to_lightgrey(YOUTUBE_URL)}")
        webbrowser.open(YOUTUBE_URL)
        
    def bilibili(self):
        aprint(f"Opening Honkai: Star Rail's BiliBili page...\n - {Printer.to_lightgrey(BILIBILI_URL)}")
        webbrowser.open(BILIBILI_URL)