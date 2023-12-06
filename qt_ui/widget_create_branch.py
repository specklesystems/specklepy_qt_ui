import inspect
import os
from typing import List, Tuple, Union

try:
    from specklepy_qt_ui.qt_ui.utils.logger import logToUser
except ModuleNotFoundError: 
    from speckle.specklepy_qt_ui.qt_ui.utils.logger import logToUser

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSignal

from specklepy.core.api.client import SpeckleClient


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.join(os.path.dirname(__file__), "ui", "create_branch.ui") )
)

class CreateBranchModalDialog(QtWidgets.QWidget, FORM_CLASS):

    name_field: QtWidgets.QLineEdit = None
    description_field: QtWidgets.QLineEdit = None
    dialog_button_box: QtWidgets.QDialogButtonBox = None
    speckle_client: Union[SpeckleClient, None] = None

    #Events
    handleBranchCreate = pyqtSignal(str,str)

    def __init__(self, parent=None, speckle_client: SpeckleClient = None):
        super(CreateBranchModalDialog,self).__init__(parent,QtCore.Qt.WindowStaysOnTopHint)
        self.speckle_client = speckle_client
        self.setupUi(self)
        self.setWindowTitle("Create New Branch")

        self.name_field.textChanged.connect(self.nameCheck)
        self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False) 
        self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.onOkClicked)
        self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.onCancelClicked)

    def nameCheck(self):
        try:
            if len(self.name_field.text()) >= 3:
                self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True) 
            else: 
                self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False) 
            return
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3])
            return

    def onOkClicked(self):
        try:
            name = self.name_field.text()
            description = self.description_field.text()
            self.handleBranchCreate.emit(name, description)
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
    r'''
    def onAccountSelected(self, index):
        try:
            account = self.speckle_accounts[index]
            self.speckle_client = SpeckleClient(account.serverInfo.url, account.serverInfo.url.startswith("https"))
            self.speckle_client.authenticate_with_token(token=account.token)
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3])
            return
    '''