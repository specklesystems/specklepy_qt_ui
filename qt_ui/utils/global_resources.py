import os

# colors
COLOR_HIGHLIGHT = (210, 210, 210, 1)
SPECKLE_COLOR = (59, 130, 246, 1)
SPECKLE_COLOR_LIGHT = (69, 140, 255, 1)
ICON_LOGO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "logo-slab-white@0.5x.png"
)

ERROR_COLOR = (255, 150, 150, 1)
ERROR_COLOR_LIGHT = (255, 210, 210, 1)

COLOR = f"color: rgba{str(SPECKLE_COLOR)};"
BACKGR_COLOR_TRANSPARENT = f"background-color: rgba(0,0,0,0);"
BACKGR_COLOR_HIGHLIGHT = f"background-color: rgba{str(COLOR_HIGHLIGHT)};"
BACKGR_COLOR = f"background-color: rgba{str(SPECKLE_COLOR)};"
BACKGR_COLOR_LIGHT = f"background-color: rgba{str(SPECKLE_COLOR_LIGHT)};"
BACKGR_COLOR_GREY = f"background-color: rgba(220,220,220,1);"

BACKGR_ERROR_COLOR = f"background-color: rgba{str(ERROR_COLOR)};"
BACKGR_ERROR_COLOR_LIGHT = f"background-color: rgba{str(ERROR_COLOR_LIGHT)};"

NEW_GREY = BACKGR_COLOR_GREY.replace("1);", "0.2);")
NEW_GREY_HIGHLIGHT = BACKGR_COLOR_HIGHLIGHT.replace("1);", "0.3);")

# images
ICON_SEARCH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "magnify.png"
)
ICON_OPEN_WEB = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "open-in-new.png"
)
ICON_REPORT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "chart-line.png"
)

ICON_DELETE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "delete.png"
)
ICON_DELETE_BLUE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "delete-blue.png"
)

ICON_SEND = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "cube-send.png"
)
ICON_RECEIVE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "cube-receive.png"
)

ICON_SEND_BLACK = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "cube-send-black.png"
)
ICON_RECEIVE_BLACK = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "cube-receive-black.png"
)

ICON_SEND_BLUE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "cube-send-blue.png"
)
ICON_RECEIVE_BLUE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "cube-receive-blue.png"
)

ICON_XXL = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "size-xxl.png"
)
ICON_RASTER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "legend_raster.png"
)
ICON_POLYGON = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "legend_polygon.png"
)
ICON_LINE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "legend_line.png"
)
ICON_POINT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "legend_point.png"
)
ICON_GENERIC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "legend_generic.png"
)
ICON_PIN_ACTIVE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "pin.png"
)
ICON_PIN_DISABLED = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "pin-outline.png"
)

