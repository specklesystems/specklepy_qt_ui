
import inspect
from typing import List, Optional, Tuple, Union, Any
import webbrowser

from speckle.utils.panel_logging import logToUser 
from specklepy.core.api.credentials import get_local_accounts

class DataStorage:
    
    plugin_version = "0.0.99"

    project = None
    accounts = None
    active_account = None
    default_account = None

    currentCRS = None
    currentUnits = "m"
    currentOriginalUnits = ""

    custom_lat: Optional[float] = None
    custom_lon: Optional[float] = None
    
    crs_offset_x: Optional[float] = None 
    crs_offset_y: Optional[float] = None 
    crs_rotation: Optional[float] = None 

    current_layers: Union[List[Tuple[Any, str, str]], None] = None 
    saved_layers: Union[List, None] = None 
    sending_layers: None
    all_layers: Union[List, None] = None 

    elevationLayer: None 
    savedTransforms: Union[List, None] = None
    transformsCatalog: Union[List, None] = None

    def __init__(self):
        print("hello")
        #self.streamsToFollow.append(("https://speckle.xyz/streams/17b0b76d13/branches/random_tests", "", "09a0f3e41a"))
        self.transformsCatalog = ["Convert Raster Elevation to a 3d Mesh",
                                  "Set Raster as a Texture for the Elevation Layer",
                                  "Extrude polygons by selected attribute (randomly populate NULL values)",
                                  "Extrude polygons by selected attribute (ignore NULL values)",
                                  "Extrude polygons by selected attribute (randomly populate  NULL values) and project on 3d elevation",
                                  "Extrude polygons by selected attribute (ignore NULL values) and project on 3d elevation"
                                  ] 
        self.savedTransforms = []
        self.all_layers = []
        self.current_layers = []
        self.saved_layers = []
        self.accounts = [] 
        self.elevationLayer = None 

    def check_for_accounts(self):
        try:
            def go_to_manager():
                webbrowser.open("https://speckle-releases.netlify.app/")
            accounts = get_local_accounts()
            self.accounts = accounts
            if len(accounts) == 0:
                logToUser("No accounts were found. Please remember to install the Speckle Manager and setup at least one account", level = 1, url="https://speckle-releases.netlify.app/", func = inspect.stack()[0][3], plugin = self.dockwidget) #, action_text="Download Manager", callback=go_to_manager)
                return False
            for acc in accounts:
                if acc.isDefault: 
                    self.default_account = acc 
                    self.active_account = acc 
                    break 
            return True
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3])
            return
        