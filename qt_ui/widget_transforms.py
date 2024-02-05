
import os

try:
    from specklepy_qt_ui.qt_ui.DataStorage import DataStorage
except ModuleNotFoundError: 
    from speckle.specklepy_qt_ui.qt_ui.DataStorage import DataStorage

from PyQt5 import QtWidgets, uic, QtCore


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.join(os.path.dirname(__file__), "ui", "transforms.ui") )
)

class MappingSendDialog(QtWidgets.QWidget, FORM_CLASS):

    dialog_button: QtWidgets.QPushButton = None
    more_info: QtWidgets.QPushButton = None
    layerDropdown: QtWidgets.QComboBox
    transformDropdown: QtWidgets.QComboBox
    addTransform: QtWidgets.QPushButton
    removeTransform: QtWidgets.QPushButton
    transformationsList: QtWidgets.QListWidget
    elevationLayerDropdown: QtWidgets.QComboBox
    
    attrDropdown: QtWidgets.QComboBox
    dataStorage: DataStorage = None

    def __init__(self, parent=None):
        super(MappingSendDialog,self).__init__(parent,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.runAllSetup()

    def runAllSetup(self):
        self.setMinimumWidth(600)

        self.addTransform.setStyleSheet("QPushButton {color: black; padding:3px;padding-left:5px;border: none; } QPushButton:hover { background-color: lightgrey}")
        self.removeTransform.setStyleSheet("QPushButton {color: black; padding:3px;padding-left:5px;border: none; } QPushButton:hover { background-color: lightgrey}")
        
        self.addTransform.clicked.connect(self.onAddTransform)
        self.removeTransform.clicked.connect(self.onRemoveTransform)
        self.transformDropdown.currentIndexChanged.connect(self.populateLayersByTransform)
        self.transformDropdown.currentIndexChanged.connect(self.populateAttributesByLayer)
        self.layerDropdown.currentIndexChanged.connect(self.populateAttributesByLayer)
        #self.dialog_button.clicked.connect(self.saveElevationLayer)
        self.dialog_button.clicked.connect(self.onOkClicked)
        self.more_info.clicked.connect(self.onMoreInfo)
        return

    def runSetup(self):
        return 

    def populateSavedTransforms(self, dataStorage): #, savedTransforms: Union[List, None] = None, getLayer: Union[str, None] = None, getTransform: Union[str, None] = None):
        return

    def onAddTransform(self):
        return

    def onRemoveTransform(self):
        return

    def onOkClicked(self):
        try:
            self.close()
        except: pass 
    
    def populateLayers(self):
        return
    
    def populateLayersByTransform(self):
        return
    
    def populateAttributesByLayer(self):
        return

    def populateTransforms(self):
        return 

    def populateSavedElevationLayer(self, dataStorage): #, savedTransforms: Union[List, None] = None, getLayer: Union[str, None] = None, getTransform: Union[str, None] = None):
        return 
    
    def saveElevationLayer(self):
        return 
            
    def onMoreInfo(self):
        return 