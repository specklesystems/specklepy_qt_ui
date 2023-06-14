
from typing import List, Tuple, Union, Any 


class DataStorage:
    
    project = None
    accounts = None
    active_account = None
    default_account = None
    currentCRS = None
    currentUnits = "m"
    current_layers: Union[List[Tuple[Any, str, str]], None] = None 
    saved_layers: Union[List, None] = None 
    sending_layers: None
    all_layers: Union[List, None] = None 
    elevationLayer: None 
    savedTransforms: Union[List, None] = None
    transformsCatalog: Union[List, None] = None
    plugin_version = "0.0.99"

    def __init__(self):
        print("hello")
        #self.streamsToFollow = []
        #self.streamsToFollow.append(("https://speckle.xyz/streams/17b0b76d13/branches/random_tests", "", "09a0f3e41a"))
        self.transformsCatalog = ["Convert Raster Elevation to a 3d Mesh",
                                  "Set Raster as a Texture for the Elevation Layer",
                                  "Extrude polygons by selected attribute (randomly populate NULL values)",
                                  "Extrude polygons by selected attribute (ignore NULL values)",
                                  "Extrude polygons by selected attribute (randomly populate  NULL values) and project on 3d elevation",
                                  "Extrude polygons by selected attribute (ignore NULL values) and project on 3d elevation"
                                  ] 
        self.savedTransforms = []
        all_layers = []
        current_layers = []
        self.accounts = [] 
        self.elevationLayer = None
        #from specklepy_qt_ui.project_vars import set_transformations


        