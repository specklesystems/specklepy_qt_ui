import inspect
import os
from typing import List, Tuple, Union
from specklepy_qt_ui.qt_ui.DataStorage import DataStorage

# from specklepy_qt_ui.qt_ui.utils.logger import logToUser

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QCheckBox, QListWidgetItem, QHBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal

from specklepy.core.api.client import SpeckleClient

from specklepy_qt_ui.qt_ui.utils.global_resources import COLOR

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.join(os.path.dirname(__file__), "ui", "report.ui"))
)


class ReportDialog(QtWidgets.QWidget, FORM_CLASS):
    report_label: QtWidgets.QLabel = None
    report_text: QtWidgets.QTextEdit = None
    dataStorage: DataStorage = None

    def __init__(self, parent=None):
        super(ReportDialog, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.runAllSetup()

    def runAllSetup(self):
        self.setWindowTitle("Report (Speckle)")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        self.report_label.setWordWrap(True)
        self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(
            self.onOkClicked
        )

        return
        # self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText("More Info")

    def assembleReport(self):
        try:
            if self.dataStorage is None:
                return
            reportList = self.dataStorage.latestActionReport
            if reportList is None:
                return

            operation = ""
            total_layers = 0
            total_objects = 0
            text = ""
            sending = True

            # details
            last_report = ""
            last_report += "Details:" + "\n"
            for item in reportList:
                line = "✅ "
                try:  # if sending
                    line += f'{item["feature_id"]}: {item["obj_type"]}'
                    operation = f"Sent at {self.dataStorage.latestActionTime}"
                except:  # if receiving
                    sending = False
                    line += f'{item["speckle_id"]}: {item["obj_type"]}'
                    operation = f"Received at {self.dataStorage.latestActionTime}"

                # edit based on the type
                if "Layer" in item["obj_type"]:
                    total_layers += 1
                    if item["errors"] != "":
                        line += f', errors: {item["errors"]}'
                        line = "⚠️" + line[1:]
                    line = "\n" + line
                else:
                    if item["errors"] != "":
                        line += f', errors: {item["errors"]}'
                        line = "❌ " + line[1:]
                    else:
                        total_objects += 1
                    line = "__ " + line

                last_report += line + "\n"

            text += f"Operation: {operation}\n"
            text += f"Total: {total_layers} layer{'' if str(total_layers).endswith('1') else 's'}, {total_objects} feature{'' if str(total_objects).endswith('1') else 's'}\n\n"
            if sending is False:
                try:
                    text += f"Host application: {self.dataStorage.latestHostApp}\n\n"
                except:
                    pass

            # layers and transformations (if applicable)
            text += "Layers and transformations (if applicable):" + "\n"
            for i, layer in enumerate(self.dataStorage.latestActionLayers):
                # print(self.dataStorage.latestActionLayers)
                name = layer  # if isinstance(layer, str) else layer.name()
                try:
                    transformExists = 0
                    for item in self.dataStorage.savedTransforms:
                        layer_name = item.split("  ->  ")[0].split(" ('")[0]
                        transform_name = item.split("  ->  ")[1]
                        if layer_name == name:
                            text += (
                                f"{i+1}. {layer_name}  ->  '{transform_name}'" + "\n"
                            )
                            transformExists += 1
                            break
                    if transformExists == 0:
                        text += f"{i+1}. {name} \n"
                except Exception as e:
                    print(e)
            text += "\n"

            # add info about the offsets
            text += "Project CRS: " + self.dataStorage.project.crs().authid() + "\n"
            units = self.dataStorage.latestActionUnits
            text += (
                "Project CRS units: "
                + units
                + f"{' (not supported, treated as Meters)' if 'degrees' in units else ''}"
                + "\n"
            )
            text += (
                "Project CRS WKT: \n" + self.dataStorage.project.crs().toWkt() + "\n\n"
            )
            text += (
                f"CRS offsets: x={self.dataStorage.crs_offset_x}, y={self.dataStorage.crs_offset_y}"
                + "\n"
            )
            text += f"CRS rotation: {self.dataStorage.crs_rotation}°" + "\n\n"

            text += last_report

            return operation, total_layers, total_objects, text
        except Exception as e:
            print(e)
            return

    def applyReport(self):
        result = self.assembleReport()
        if result is None:
            print("no report generated")
            return
        operation, total_layers, total_objects, report = result
        # self.report_label.setText(f"Operation: {operation}\nTotal: {total_layers} layer{'' if str(total_layers).endswith('1') else 's'}, {total_objects} feature{'' if str(total_objects).endswith('1') else 's'}")
        self.report_text.setText(report)

    def onOkClicked(self):
        self.close()
