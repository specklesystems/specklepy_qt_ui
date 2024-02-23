import inspect
import os
from typing import List, Tuple, Union

try:
    from specklepy_qt_ui.qt_ui.DataStorage import DataStorage
    from specklepy_qt_ui.qt_ui.utils.global_resources import COLOR
    from specklepy_qt_ui.qt_ui.utils.utils import SYMBOL
except ModuleNotFoundError:
    from speckle.specklepy_qt_ui.qt_ui.DataStorage import DataStorage
    from speckle.specklepy_qt_ui.qt_ui.utils.global_resources import COLOR
    from speckle.specklepy_qt_ui.qt_ui.utils.utils import SYMBOL

# from specklepy_qt_ui.qt_ui.utils.logger import logToUser

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QCheckBox, QListWidgetItem, QHBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal

from specklepy.core.api.client import SpeckleClient


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
            reportList: List[dict] = self.dataStorage.latestActionReport
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
                    some_id = item["feature_id"].replace(SYMBOL, "\\")
                    line += f'{some_id}: {item["obj_type"]}'
                    operation = f"Sent at {self.dataStorage.latestActionTime}"
                except:  # if receiving
                    sending = False
                    some_id = item[list(item.keys())[0]].replace(SYMBOL, "\\")
                    line += f'{some_id}: {item["obj_type"]}'  # f'{item["speckle_id"]}: {item["obj_type"]}'
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
            try:
                crs = self.dataStorage.project.crs()
                text += "Project CRS: " + crs.authid() + "\n"
                crs_keyword = "CRS"
            except AttributeError:
                crs = self.dataStorage.project.activeMap.spatialReference
                crs_keyword = "Spatial Reference"
                text += f"Project {crs_keyword}: " + crs.name + "\n"
            units = self.dataStorage.latestActionUnits
            text += (
                f"Project {crs_keyword} units: "
                + units
                + f"{' (not supported, treated as Meters)' if 'degrees' in units else ''}"
                + "\n"
            )
            try:
                text += f"Project {crs_keyword} WKT: \n" + crs.toWkt() + "\n\n"
            except:
                text += f"Project {crs_keyword} WKT: \n" + crs.exportToString() + "\n\n"

            text += (
                f"{crs_keyword} offsets: x={self.dataStorage.crs_offset_x}, y={self.dataStorage.crs_offset_y}"
                + "\n"
            )
            text += f"{crs_keyword} rotation: {self.dataStorage.crs_rotation}°" + "\n\n"

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
