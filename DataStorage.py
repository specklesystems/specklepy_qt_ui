
from typing import List, Optional, Tuple, Union, Any 


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


        