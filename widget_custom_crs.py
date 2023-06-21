import inspect
import os
from typing import List, Tuple, Union
from specklepy_qt_ui.DataStorage import DataStorage
from specklepy_qt_ui.logger import logToUser

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QCheckBox, QListWidgetItem, QHBoxLayout, QWidget 
from PyQt5.QtCore import pyqtSignal

from specklepy.api.client import SpeckleClient

from specklepy_qt_ui.global_resources import COLOR

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.join(os.path.dirname(__file__), "ui", "custom_crs.ui") )
)

class CustomCRSDialog(QtWidgets.QWidget, FORM_CLASS):

    name_field: QtWidgets.QLineEdit = None
    description_field: QtWidgets.QLineEdit = None
    dialog_button_box: QtWidgets.QDialogButtonBox = None
    saveSurveyPoint: QtWidgets.QPushButton = None
    speckle_client: Union[SpeckleClient, None] = None
    dataStorage: DataStorage = None 

    #Events
    handleCRSCreate = pyqtSignal(str,str)

    def __init__(self, parent=None, speckle_client: SpeckleClient = None):
        super(CustomCRSDialog,self).__init__(parent,QtCore.Qt.WindowStaysOnTopHint)
        self.speckle_client = speckle_client
        self.setupUi(self)
        self.setWindowTitle("CustomCRS")

        #self.saveSurveyPoint.setFlat(True)
        #self.saveSurveyPoint.setStyleSheet("QPushButton {text-align: left;} QPushButton:hover { " + f"{COLOR}" + " }")
        #self.saveOffsets.setFlat(True)
        #self.saveOffsets.setStyleSheet("QPushButton {text-align: left;} QPushButton:hover { " + f"{COLOR}" + " }")

        #self.label_offsets.setEnabled(False)
        self.offsetX.setEnabled(False)
        self.offsetY.setEnabled(False)
        self.rotation.setEnabled(False)
        #self.saveOffsets.setEnabled(False)
        
        
        self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(self.onCancelClicked)
        self.modeDropdown.currentIndexChanged.connect(self.onModeChanged)

        self.populateModeDropdown()
        self.populateSurveyPoint()
    
    def onModeChanged(self):
        try:
            if not self: return
            index = self.modeDropdown.currentIndex()
            if index == 0:
                #self.label_customCRS.setEnabled(True)
                self.surveyPointLat.setEnabled(True)
                self.surveyPointLon.setEnabled(True)
                #self.saveSurveyPoint.setEnabled(True)
                
                #self.label_offsets.setEnabled(False)
                self.offsetX.setEnabled(False)
                self.offsetY.setEnabled(False)
                self.rotation.setEnabled(False)
                #self.saveOffsets.setEnabled(False)

            elif index == 1:
                #self.label_customCRS.setEnabled(False)
                self.surveyPointLat.setEnabled(False)
                self.surveyPointLon.setEnabled(False)
                #self.saveSurveyPoint.setEnabled(False)
                
                #self.label_offsets.setEnabled(True)
                self.offsetX.setEnabled(True)
                self.offsetY.setEnabled(True)
                self.rotation.setEnabled(True)
                #self.saveOffsets.setEnabled(True)

        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3])
            return
        
    def populateModeDropdown(self):
        if not self: return
        try:
            self.modeDropdown.clear()
            self.modeDropdown.addItems(
                ["Create custom CRS", "Add offsets / rotation to the current Project CRS"]
            )
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return
        
    def populateSurveyPoint(self):
        if not self:
            return
        try:
            self.surveyPointLat.clear()
            self.surveyPointLon.clear()
            if self.dataStorage.custom_lat is not None and self.dataStorage.custom_lon is not None:
                self.surveyPointLat.setText(str(self.dataStorage.custom_lat))
                self.surveyPointLon.setText(str(self.dataStorage.custom_lon))
            
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def onOkClicked(self):
        return
        try:
            self.close()
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3])
            return

    def onCancelClicked(self):
        try:
            self.close()
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3])
            return

    def onAccountSelected(self, index):
        try:
            account = self.speckle_accounts[index]
            self.speckle_client = SpeckleClient(account.serverInfo.url, account.serverInfo.url.startswith("https"))
            self.speckle_client.authenticate_with_token(token=account.token)
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3])
            return
