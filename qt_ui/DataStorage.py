from datetime import datetime
import inspect
from typing import List, Optional, Tuple, Union, Any
import webbrowser

try:
    from specklepy_qt_ui.qt_ui.utils.logger import logToUser
except ModuleNotFoundError:
    from speckle.specklepy_qt_ui.qt_ui.utils.logger import logToUser

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
    workspace = ""

    custom_lat: Optional[float] = None
    custom_lon: Optional[float] = None

    crs_offset_x: Optional[float] = 0
    crs_offset_y: Optional[float] = 0
    crs_rotation: Optional[float] = 0

    current_layer_crs_offset_x: Optional[float] = None
    current_layer_crs_offset_y: Optional[float] = None
    current_layer_crs_rotation: Optional[float] = None

    current_layers: Union[List[Tuple[Any, str, str]], None] = None
    saved_layers: Union[List, None] = None
    all_layers: Union[List, None] = None

    elevationLayer: None
    savedTransforms: Union[List, None] = None
    transformsCatalog: Union[List, None] = None

    matrix = None  # if receiving instance with transform

    latestHostApp: str = ""
    latestActionReport: Optional[list] = None
    latestActionFeaturesReport: Optional[list] = None
    latestActionTime: str = ""
    latestTransferTime: datetime = None
    latestConversionTime: datetime = None
    latestActionLayers: Optional[list] = None
    latestActionUnits: str = ""

    flat_report_receive: dict = {}
    flat_report_latest: dict = {}

    def __init__(self):
        # print("hello")
        # self.streamsToFollow.append(("https://speckle.xyz/streams/17b0b76d13/branches/random_tests", "", "09a0f3e41a"))
        self.transformsCatalog = [
            "Convert Raster Elevation to a 3d Mesh",
            "Set Raster as a Texture for the Elevation Layer",
            "Extrude polygons by selected attribute (randomly populate NULL values)",
            "Extrude polygons by selected attribute (ignore NULL values)",
            "Extrude polygons by selected attribute (randomly populate  NULL values) and project on 3d elevation",
            "Extrude polygons by selected attribute (ignore NULL values) and project on 3d elevation",
        ]
        self.savedTransforms = []
        self.all_layers = []
        self.current_layers = []
        self.saved_layers = []
        self.accounts = []
        self.elevationLayer = None
        self.latestActionReport = []
        self.latestActionFeaturesReport = []
        self.latestActionLayers = []

    def check_for_accounts(self):
        try:

            def go_to_manager():
                webbrowser.open("https://speckle-releases.netlify.app/")

            accounts = get_local_accounts()
            self.accounts = accounts
            if len(accounts) == 0:
                logToUser(
                    "No accounts were found. Please remember to install the Speckle Manager and setup at least one account",
                    level=1,
                    url="https://speckle-releases.netlify.app/",
                    func=inspect.stack()[0][3],
                    plugin=self.dockwidget,
                )  # , action_text="Download Manager", callback=go_to_manager)
                return False
            for acc in accounts:
                if acc.isDefault:
                    self.default_account = acc
                    self.active_account = acc
                    break
            return True
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3])
            return
