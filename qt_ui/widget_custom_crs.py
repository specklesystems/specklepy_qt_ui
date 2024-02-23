import inspect
import os
from typing import List, Tuple, Union

try:
    from specklepy_qt_ui.qt_ui.DataStorage import DataStorage
    from specklepy_qt_ui.qt_ui.utils.logger import logToUser
    from specklepy_qt_ui.qt_ui.utils.global_resources import COLOR
except ModuleNotFoundError:
    from speckle.specklepy_qt_ui.qt_ui.DataStorage import DataStorage
    from speckle.specklepy_qt_ui.qt_ui.utils.logger import logToUser
    from speckle.specklepy_qt_ui.qt_ui.utils.global_resources import COLOR

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QCheckBox, QListWidgetItem, QHBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal

from specklepy.core.api.client import SpeckleClient


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.join(os.path.dirname(__file__), "ui", "custom_crs.ui"))
)


class CustomCRSDialog(QtWidgets.QWidget, FORM_CLASS):
    name_field: QtWidgets.QLineEdit = None
    description: QtWidgets.QLineEdit = None
    dialog_button_box: QtWidgets.QDialogButtonBox = None
    saveSurveyPoint: QtWidgets.QPushButton = None
    speckle_client: Union[SpeckleClient, None] = None
    dataStorage: DataStorage = None

    # Events
    # handleCRSCreate = pyqtSignal(str,str)

    def __init__(self, parent=None):
        super(CustomCRSDialog, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.setWindowTitle("Set project center on Send/Receive")

        # self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(self.onCancelClicked)
        self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(
            "More Info"
        )
        self.modeDropdown.currentIndexChanged.connect(self.onModeChanged)

    def onModeChanged(self):
        try:
            if not self:
                return
            index = self.modeDropdown.currentIndex()
            if index == 1:  # custom crs
                self.surveyPointLat.show()
                self.surveyPointLon.show()
                self.degreeSignX.show()
                self.degreeSignY.show()
                self.label_survey.show()

                self.offsetX.hide()
                self.offsetY.hide()
                self.label_offsets.hide()
                self.offsetXDegreeSign.hide()
                self.offsetYDegreeSign.hide()
                self.description.setText(
                    "Use this option when you don't have to use a specific CRS.\
                                         \n\nThis will change your Project CRS to a new custom CRS.\
                                         \n\nHint: right-click on the canvas -> Copy Coordinate -> EPSG:4326. "
                )

            elif index == 0:  # offsets
                self.surveyPointLat.hide()
                self.surveyPointLon.hide()
                self.degreeSignX.hide()
                self.degreeSignY.hide()
                self.label_survey.hide()

                self.offsetX.show()
                self.offsetY.show()
                self.label_offsets.show()
                # if self.dataStorage.currentOriginalUnits == 'degrees':
                self.offsetXDegreeSign.show()
                self.offsetYDegreeSign.show()

                units = self.dataStorage.currentOriginalUnits
                print(units)
                if units == "degrees":
                    self.offsetXDegreeSign.setText("°")
                    self.offsetYDegreeSign.setText("°")
                elif units is not None:
                    self.offsetXDegreeSign.setText(str(units).lower()[0])
                    self.offsetYDegreeSign.setText(str(units).lower()[0])
                else:
                    self.offsetXDegreeSign.hide()
                    self.offsetYDegreeSign.hide()

                try:
                    authid = self.dataStorage.currentCRS.authid()
                except:
                    try:
                        authid = self.dataStorage.currentCRS.name
                    except:
                        authid = str(self.dataStorage.currentCRS)

                text = f"Use this option when your project requires a use of a specific CRS. \
                        \n\nThis will only affect Speckle data properties, not your Project CRS.\
                        \n\nHint: your current project CRS is '{authid}' and using units '{self.dataStorage.currentOriginalUnits}'."

                if units == "degrees":
                    text += "\nThis CRS is not recommended if data was sent or needs to be \
                            \nreceived in a non-GIS application."

                self.description.setText(text)

            self.populateSurveyPoint()
            self.populateOffsets()
            self.populateRotation()

        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3])
            return

    def populateModeDropdown(self):
        if not self:
            return
        try:
            self.modeDropdown.clear()
            self.modeDropdown.addItems(
                [
                    "Add offsets / rotation to the current Project CRS",
                    "Create custom CRS",
                ]
            )
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def populateSurveyPoint(self):
        if not self:
            return
        try:
            self.surveyPointLat.clear()
            self.surveyPointLon.clear()
            if (
                self.dataStorage.custom_lat is not None
                and self.dataStorage.custom_lon is not None
            ):
                self.surveyPointLat.setText(str(self.dataStorage.custom_lat))
                self.surveyPointLon.setText(str(self.dataStorage.custom_lon))
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def populateRotation(self):
        if not self:
            return
        try:
            self.rotation.clear()
            if self.dataStorage.crs_rotation is not None:
                self.rotation.setText(str(self.dataStorage.crs_rotation))
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def populateOffsets(self):
        try:
            self.offsetX.clear()
            self.offsetY.clear()
            if (
                self.dataStorage.crs_offset_x is not None
                and self.dataStorage.crs_offset_y is not None
            ):
                self.offsetX.setText(str(self.dataStorage.crs_offset_x))
                self.offsetY.setText(str(self.dataStorage.crs_offset_y))

        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def onOkClicked(self):
        return
        try:
            self.close()
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3])
            return
