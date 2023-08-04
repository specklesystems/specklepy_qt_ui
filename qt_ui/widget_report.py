import inspect
import os
from typing import List, Tuple, Union
from specklepy_qt_ui.qt_ui.DataStorage import DataStorage
from specklepy_qt_ui.qt_ui.logger import logToUser

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QCheckBox, QListWidgetItem, QHBoxLayout, QWidget 
from PyQt5.QtCore import pyqtSignal

from specklepy.core.api.client import SpeckleClient

from specklepy_qt_ui.qt_ui.global_resources import COLOR

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.join(os.path.dirname(__file__), "ui", "report.ui") )
)

class ReportDialog(QtWidgets.QWidget, FORM_CLASS):

    report_text: QtWidgets.QLineEdit = None
    dataStorage: DataStorage = None 

    def __init__(self, parent=None):
        
        super(ReportDialog,self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.setWindowTitle("Report")  
        
        #self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(self.onCancelClicked)
        #self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText("More Info")
    