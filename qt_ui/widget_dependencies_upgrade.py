import os
import urllib3
import requests
import requests_toolbelt
from specklepy.logging import metrics

try:
    from specklepy_qt_ui.qt_ui.DataStorage import DataStorage
except ModuleNotFoundError:
    from speckle.specklepy_qt_ui.qt_ui.DataStorage import DataStorage

from PyQt5 import QtWidgets, uic, QtCore

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.join(os.path.dirname(__file__), "ui", "dependencies.ui"))
)


class DependenciesUpgradeDialog(QtWidgets.QWidget, FORM_CLASS):
    report_label: QtWidgets.QLabel = None
    report_widget: QtWidgets.QTextEdit = None
    btn_cancel: QtWidgets.QPushButton = None
    btn_upgrade: QtWidgets.QPushButton = None
    report_text: str = ""
    dataStorage: DataStorage = None

    def __init__(self, parent=None):
        super(DependenciesUpgradeDialog, self).__init__(
            parent, QtCore.Qt.WindowStaysOnTopHint
        )
        self.setupUi(self)
        self.runAllSetup()

    def runAllSetup(self):
        self.setWindowTitle("Upgrade Python dependencies (Speckle)")
        self.setMinimumWidth(900)
        self.setMinimumHeight(600)
        self.report_label.setWordWrap(True)
        self.btn_cancel.clicked.connect(self.onOkClicked)
        self.btn_upgrade.clicked.connect(self.upgradeDependencies)
        self.btn_upgrade.setEnabled(True)
        self.report_text = f"""Speckle plugin requires changes in versions of some Python libraries: 
\nurllib3: from {urllib3.__version__} to 1.26.16
requests: from {requests.__version__} to 2.31.0
requests_toolbelt: from {requests_toolbelt.__version__} to 0.10.1
\nYou can use the button below run the upgrade automatically.
To do it manually, you can run 2 following commands from QGIS Plugins panel->Python Console, and then restart QGIS:
\n\ndef upgradeDependencies():
\timport subprocess
\tfrom speckle.utils.utils import get_qgis_python_path as path
\tresult = subprocess.run([path(), "-m", "pip", "install", "requests==2.31.0"],shell=True,timeout=1000,)
\tprint(result.returncode)
\tresult = subprocess.run([path(), "-m", "pip", "install", "urllib3==1.26.16"],shell=True,timeout=1000,)
\tprint(result.returncode)
\tresult = subprocess.run([path(), "-m", "pip", "install", "requests_toolbelt==0.10.1"],shell=True,timeout=1000,)
\tprint(result.returncode)
\nupgradeDependencies()
\n\n"""
        self.report_widget.setText(self.report_text)
        return

    def onOkClicked(self):
        self.close()

    def upgradeDependencies(self):
        try:
            metrics.track(
                "Connector Action",
                self.dataStorage.active_account,
                {
                    "name": "Resolve dependencies",
                    "connector_version": str(self.dataStorage.plugin_version),
                },
            )
        except Exception as e:
            print(e)

        self.report_widget.setText("It might take a moment...")
        self.btn_upgrade.setEnabled(False)
        res1, res2, res3 = self.runSubprocess()

        if res1.returncode == res2.returncode == res3.returncode == 0:
            self.report_widget.setText(
                "Libraries successfully upgraded. Please restart QGIS for Speckle to use the upgraded libraries."
            )
        else:
            self.report_widget.setText(
                f"Something went wrong. Here are the error logs: \n\n{res1}\n\n{res2}"
            )

    def runSubprocess(self):
        import subprocess

        try:
            from speckle.utils.utils import get_qgis_python_path as path
        except ModuleNotFoundError:
            from speckle.speckle.utils.utils import get_qgis_python_path as path

        result1 = subprocess.run(
            [path(), "-m", "pip", "install", "requests==2.31.0"],
            timeout=1000,
            capture_output=True,
        )
        result2 = subprocess.run(
            [path(), "-m", "pip", "install", "urllib3==1.26.16"],
            timeout=1000,
            capture_output=True,
        )
        result3 = subprocess.run(
            [path(), "-m", "pip", "install", "requests_toolbelt==0.10.1"],
            timeout=1000,
            capture_output=True,
        )
        return result1, result2, result3
