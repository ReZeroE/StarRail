
import webbrowser
from starrail.constants import HOMEPAGE_URL, HOYOLAB_URL, YOUTUBE_URL
from starrail.utils.utils import aprint

class StarRailWebController:
    def __init__(self):
        pass
    
    def homepage(self):
        aprint("Opening Honkai: Star Rail's official home page...")
        webbrowser.open(HOMEPAGE_URL)
        
    def hoyolab(self):
        aprint("Opening Honkai: Star Rail's HoyoLab page...")
        webbrowser.open(HOYOLAB_URL)
        
    def youtube(self):
        aprint("Opening Honkai: Star Rail's Youtube page...")
        webbrowser.open(YOUTUBE_URL)