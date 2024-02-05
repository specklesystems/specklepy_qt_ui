# -*- coding: utf-8 -*-

from copy import copy
import inspect
import os

try:
    from specklepy_qt_ui.qt_ui.widget_transforms import MappingSendDialog
    from specklepy_qt_ui.qt_ui.LogWidget import LogWidget
    from specklepy_qt_ui.qt_ui.utils.logger import logToUser
    from specklepy_qt_ui.qt_ui.utils.utils import constructCommitURL
    from specklepy_qt_ui.qt_ui.DataStorage import DataStorage
    from specklepy_qt_ui.qt_ui.utils.global_resources import (
        COLOR_HIGHLIGHT,
        SPECKLE_COLOR,
        SPECKLE_COLOR_LIGHT,
        ICON_OPEN_WEB,
        ICON_REPORT,
        ICON_LOGO,
        ICON_SEARCH,
        ICON_DELETE,
        ICON_DELETE_BLUE,
        ICON_SEND,
        ICON_RECEIVE,
        ICON_SEND_BLACK,
        ICON_RECEIVE_BLACK,
        ICON_SEND_BLUE,
        ICON_RECEIVE_BLUE,
        COLOR,
        BACKGR_COLOR,
        BACKGR_COLOR_LIGHT,
        ICON_XXL,
        ICON_RASTER,
        ICON_POLYGON,
        ICON_LINE,
        ICON_POINT,
        ICON_GENERIC,
    )
except ModuleNotFoundError: 
    from speckle.specklepy_qt_ui.qt_ui.widget_transforms import MappingSendDialog
    from speckle.specklepy_qt_ui.qt_ui.LogWidget import LogWidget
    from speckle.specklepy_qt_ui.qt_ui.utils.logger import logToUser
    from speckle.specklepy_qt_ui.qt_ui.utils.utils import constructCommitURL
    from speckle.specklepy_qt_ui.qt_ui.DataStorage import DataStorage
    from speckle.specklepy_qt_ui.qt_ui.utils.global_resources import (
        COLOR_HIGHLIGHT,
        SPECKLE_COLOR,
        SPECKLE_COLOR_LIGHT,
        ICON_OPEN_WEB,
        ICON_REPORT,
        ICON_LOGO,
        ICON_SEARCH,
        ICON_DELETE,
        ICON_DELETE_BLUE,
        ICON_SEND,
        ICON_RECEIVE,
        ICON_SEND_BLACK,
        ICON_RECEIVE_BLACK,
        ICON_SEND_BLUE,
        ICON_RECEIVE_BLUE,
        COLOR,
        BACKGR_COLOR,
        BACKGR_COLOR_LIGHT,
        ICON_XXL,
        ICON_RASTER,
        ICON_POLYGON,
        ICON_LINE,
        ICON_POINT,
        ICON_GENERIC,
    )

from specklepy.logging.exceptions import SpeckleException, GraphQLException
from specklepy.logging import metrics


from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QCheckBox, QListWidgetItem, QHBoxLayout, QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), os.path.join("ui", "dockwidget_main.ui"))
)


class SpeckleQGISDialog(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()
    streamList: QtWidgets.QComboBox
    sendModeButton: QtWidgets.QPushButton
    receiveModeButton: QtWidgets.QPushButton
    streamBranchDropdown: QtWidgets.QComboBox
    layerSendModeDropdown: QtWidgets.QComboBox
    commitDropdown: QtWidgets.QComboBox
    layersWidget: QtWidgets.QListWidget
    saveLayerSelection: QtWidgets.QPushButton
    runButton: QtWidgets.QPushButton
    setMapping: QtWidgets.QPushButton
    experimental: QCheckBox
    msgLog: LogWidget = None
    dataStorage: DataStorage = None
    mappingSendDialog = None
    custom_crs_modal = None

    signal_1 = pyqtSignal(object)
    signal_2 = pyqtSignal(object)
    signal_3 = pyqtSignal(object)
    signal_4 = pyqtSignal(object)
    signal_5 = pyqtSignal(object)
    signal_6 = pyqtSignal(object)
    signal_remove_btn_url = pyqtSignal(str)
    signal_cancel_operation = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(SpeckleQGISDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.runAllSetup()

    def runAllSetup(self):
        self.streamBranchDropdown.setMaxCount(100)
        self.commitDropdown.setMaxCount(100)

        self.streams_add_button.setFlat(True)
        self.streams_remove_button.setFlat(True)
        self.commit_web_view.setFlat(True)
        self.reportBtn.setFlat(True)
        # self.saveSurveyPoint.setFlat(True)
        self.saveLayerSelection.setFlat(True)
        self.reloadButton.setFlat(True)
        self.closeButton.setFlat(True)
        self.commit_web_view.setEnabled(False)

        # https://stackoverflow.com/questions/67585501/pyqt-how-to-use-hover-in-button-stylesheet
        backgr_image_del = f"border-image: url({ICON_DELETE_BLUE});"
        self.streams_add_button.setIcon(QIcon(ICON_SEARCH))
        self.streams_add_button.setMaximumWidth(25)
        self.streams_add_button.setStyleSheet(
            "QPushButton {padding:3px;padding-left:5px;border: none; text-align: left;} QPushButton:hover { "
            + f"background-color: rgba{str(COLOR_HIGHLIGHT)};"
            + f"{COLOR}"
            + " }"
        )

        self.commit_web_view.setIcon(QIcon(ICON_OPEN_WEB))
        self.commit_web_view.setMaximumWidth(25)
        self.commit_web_view.setStyleSheet(
            "QPushButton {padding:3px;padding-left:5px;border: none; text-align: left;} QPushButton:hover { "
            + f"background-color: rgba{str(COLOR_HIGHLIGHT)};"
            + f"{COLOR}"
            + " }"
        )

        self.reportBtn.setIcon(QIcon(ICON_REPORT))
        self.reportBtn.setMaximumWidth(25)
        self.reportBtn.setStyleSheet(
            "QPushButton {padding:3px;padding-left:5px;border: none; text-align: left;} QPushButton:hover { "
            + f"background-color: rgba{str(COLOR_HIGHLIGHT)};"
            + f"{COLOR}"
            + " }"
        )

        self.streams_remove_button.setIcon(QIcon(ICON_DELETE))
        self.streams_remove_button.setMaximumWidth(25)
        self.streams_remove_button.setStyleSheet(
            "QPushButton {padding:3px;padding-left:5px;border: none; text-align: left; image-position:right} QPushButton:hover { "
            + f"background-color: rgba{str(COLOR_HIGHLIGHT)};"
            + f"{COLOR}"
            + " }"
        )  # + f"{backgr_image_del}"

        self.saveLayerSelection.setStyleSheet(
            "QPushButton {text-align: right;} QPushButton:hover { " + f"{COLOR}" + " }"
        )
        # self.saveSurveyPoint.setStyleSheet("QPushButton {text-align: right;} QPushButton:hover { " + f"{COLOR}" + " }")
        self.reloadButton.setStyleSheet(
            "QPushButton {text-align: left;} QPushButton:hover { " + f"{COLOR}" + " }"
        )
        self.closeButton.setStyleSheet(
            "QPushButton {text-align: right;} QPushButton:hover { " + f"{COLOR}" + " }"
        )

        self.sendModeButton.setStyleSheet(
            "QPushButton {padding: 10px; border: 0px; "
            + f"color: rgba{str(SPECKLE_COLOR)};"
            + "} QPushButton:hover { "
            + "}"
        )
        self.sendModeButton.setIcon(QIcon(ICON_SEND_BLUE))

        self.receiveModeButton.setFlat(True)
        self.receiveModeButton.setStyleSheet(
            "QPushButton {padding: 10px; border: 0px;}"
            + "QPushButton:hover { "
            + f"background-color: rgba{str(COLOR_HIGHLIGHT)};"
            + "}"
        )
        self.receiveModeButton.setIcon(QIcon(ICON_RECEIVE_BLACK))

        self.runButton.setStyleSheet(
            "QPushButton {color: white;border: 0px;border-radius: 17px;padding: 10px;"
            + f"{BACKGR_COLOR}"
            + "} QPushButton:hover { "
            + f"{BACKGR_COLOR_LIGHT}"
            + " }"
        )
        # self.runButton.setGeometry(0, 0, 150, 30)
        self.runButton.setMaximumWidth(200)
        self.runButton.setIcon(QIcon(ICON_SEND))

        # insert checkbox
        l = self.verticalLayout

    def runSetup(self, plugin):
        # self.addDataStorage(plugin)
        self.addLabel(plugin)
        self.addProps(plugin)
        # self.createMappingDialog()

    def addProps(self, plugin):
        # add widgets that will only show on event trigger
        logWidget = LogWidget(parent=self)
        logWidget.dataStorage = self.dataStorage

        self.layout().addWidget(logWidget)
        self.msgLog = logWidget
        self.msgLog.dockwidget = self

        self.msgLog.active_account = plugin.dataStorage.active_account
        self.msgLog.speckle_version = plugin.version

        self.setMapping.setFlat(True)
        self.setMapping.setStyleSheet(
            "QPushButton {text-align: right;} QPushButton:hover { " + f"{COLOR}" + " }"
        )

        self.crsSettings.setFlat(True)
        self.crsSettings.setStyleSheet(
            "QPushButton {text-align: right;} QPushButton:hover { " + f"{COLOR}" + " }"
        )

    def addDataStorage(self, plugin):
        self.dataStorage = plugin.dataStorage
        try:
            self.dataStorage.project = plugin.project
        except:
            self.dataStorage.project = plugin.qgis_project

    def createMappingDialog(self):
        if self.mappingSendDialog is None:
            self.mappingSendDialog = MappingSendDialog(None)
            self.mappingSendDialog.dataStorage = self.dataStorage

        self.mappingSendDialog.runSetup()

    def showMappingDialog(self):
        # updata DataStorage
        self.mappingSendDialog.runSetup()
        self.mappingSendDialog.show()

    def addLabel(self, plugin):
        try:
            exitIcon = QPixmap(ICON_LOGO)
            exitActIcon = QIcon(exitIcon)

            # create a label
            text_label = QtWidgets.QPushButton(" for QGIS")
            text_label.setStyleSheet(
                "border: 0px;"
                "color: white;"
                f"{BACKGR_COLOR}"
                "top-margin: 40 px;"
                "padding: 10px;"
                "padding-left: 20px;"
                "font-size: 15px;"
                "height: 30px;"
                "text-align: left;"
            )
            text_label.setIcon(exitActIcon)
            text_label.setIconSize(QtCore.QSize(300, 93))
            text_label.setMinimumSize(QtCore.QSize(100, 40))
            text_label.setMaximumWidth(200)

            version = ""
            try:
                if isinstance(plugin.version, str):
                    version = str(plugin.version)
            except:
                pass

            version_label = QtWidgets.QPushButton(version)
            version_label.setStyleSheet(
                "border: 0px;"
                "color: white;"
                f"{BACKGR_COLOR}"
                "padding-top: 15px;"
                "padding-left: 0px;"
                "margin-left: 0px;"
                "font-size: 10px;"
                "height: 30px;"
                "text-align: left;"
            )

            widget = QWidget()
            widget.setStyleSheet(f"{BACKGR_COLOR}")
            boxLayout = QHBoxLayout(widget)
            boxLayout.addWidget(text_label)  # , alignment=Qt.AlignCenter)
            boxLayout.addWidget(version_label)
            boxLayout.setContentsMargins(0, 0, 0, 0)
            self.setWindowTitle("SpeckleQGIS")
            self.setTitleBarWidget(widget)
            self.labelWidget = text_label
            self.labelWidget.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            self.labelWidget.clicked.connect(self.onClickLogo)
        except Exception as e:
            logToUser(e)

    def resizeEvent(self, event):
        try:
            QtWidgets.QDockWidget.resizeEvent(self, event)
            if self.msgLog.size().height() != 0:  # visible
                self.msgLog.setGeometry(
                    0,
                    0,
                    self.msgLog.parentWidget.frameSize().width(),
                    self.msgLog.parentWidget.frameSize().height(),
                )  # .resize(self.frameSize().width(), self.frameSize().height())
        except Exception as e:
            return

    def clearDropdown(self):
        try:
            self.streamBranchDropdown.clear()
            self.commitDropdown.clear()
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def reloadDialogUI(self, plugin):
        try:
            self.clearDropdown()
            self.populateUI(plugin)
            self.enableElements(plugin)
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def run(self, plugin):
        try:
            # Setup events on first load only!
            self.setupOnFirstLoad(plugin)
            # Connect streams section events
            self.completeStreamSection(plugin)
            # Populate the UI dropdowns
            self.populateUI(plugin)
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def closeEvent(self, event):
        try:
            self.closingPlugin.emit()
            event.accept()
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def addMsg(self, obj: dict):
        self.msgLog.addButton(obj)

    def setupOnFirstLoad(self, plugin):
        try:
            # print("setupOnFirstLoad")
            self.msgLog.sendMessage.connect(self.addMsg)
            self.setMapping.clicked.connect(self.showMappingDialog)
            self.reportBtn.clicked.connect(self.msgLog.showReport)

            self.streams_add_button.clicked.connect(plugin.onStreamAddButtonClicked)
            self.commit_web_view.clicked.connect(
                lambda: plugin.openUrl(
                    constructCommitURL(
                        plugin.active_stream,
                        plugin.active_branch.id,
                        plugin.active_commit.id,
                    )
                )
            )
            self.reloadButton.clicked.connect(lambda: self.refreshClicked(plugin))
            self.closeButton.clicked.connect(lambda: self.closeClicked(plugin))

            self.sendModeButton.clicked.connect(lambda: self.setSendMode(plugin))
            self.layerSendModeDropdown.currentIndexChanged.connect(
                lambda: self.layerSendModeChange(plugin)
            )
            self.receiveModeButton.clicked.connect(lambda: self.setReceiveMode(plugin))

            # self.streamBranchDropdown.currentIndexChanged.connect( lambda: self.runBtnStatusChanged(plugin) )
            self.commitDropdown.currentIndexChanged.connect(
                lambda: self.setActiveCommit(plugin)
            )
            self.commitDropdown.currentIndexChanged.connect(
                lambda: self.runBtnStatusChanged(plugin)
            )

            self.closingPlugin.connect(plugin.onClosePlugin)
            return
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def onClickLogo(self):
        import webbrowser

        url = "https://speckle.systems/"
        webbrowser.open(url, new=0, autoraise=True)

        try:
            metrics.track(
                "Connector Action",
                self.dataStorage.active_account,
                {
                    "name": "Logo Click",
                    "connector_version": str(self.dataStorage.plugin_version),
                },
            )
        except Exception as e:
            print(e)

    def refreshClicked(self, plugin):
        try:
            try:
                metrics.track(
                    "Connector Action",
                    plugin.dataStorage.active_account,
                    {"name": "Refresh", "connector_version": str(plugin.version)},
                )
            except Exception as e:
                logToUser(
                    e, level=2, func=inspect.stack()[0][3], plugin=plugin.dockwidget
                )

            plugin.reloadUI()
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def closeClicked(self, plugin):
        try:
            try:
                metrics.track(
                    "Connector Action",
                    plugin.dataStorage.active_account,
                    {"name": "Close", "connector_version": str(plugin.version)},
                )
            except Exception as e:
                logToUser(
                    e, level=2, func=inspect.stack()[0][3], plugin=plugin.dockwidget
                )

            plugin.onClosePlugin()
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def setSendMode(self, plugin):
        try:
            plugin.btnAction = 0  # send
            color = f"color: rgba{str(SPECKLE_COLOR)};"
            self.sendModeButton.setStyleSheet(
                "border: 0px;" f"color: rgba{str(SPECKLE_COLOR)};" "padding: 10px;"
            )
            self.sendModeButton.setIcon(QIcon(ICON_SEND_BLUE))
            self.sendModeButton.setFlat(False)
            self.receiveModeButton.setFlat(True)
            self.receiveModeButton.setStyleSheet(
                "QPushButton {border: 0px; color: black; padding: 10px; } QPushButton:hover { "
                + f"background-color: rgba{str(COLOR_HIGHLIGHT)};"
                + " };"
            )
            self.receiveModeButton.setIcon(QIcon(ICON_RECEIVE_BLACK))
            self.runButton.setProperty("text", " SEND")
            self.runButton.setIcon(QIcon(ICON_SEND))

            # enable sections only if in "saved streams" mode
            if self.layerSendModeDropdown.currentIndex() == 1:
                self.layersWidget.setEnabled(True)
            self.saveLayerSelection.setEnabled(True)
            self.commitLabel.setEnabled(False)
            self.commitDropdown.setEnabled(False)
            self.messageLabel.setEnabled(True)
            self.messageInput.setEnabled(True)
            self.layerSendModeDropdown.setEnabled(True)
            self.setMapping.setEnabled(True)
            self.commit_web_view.setEnabled(False)

            self.runBtnStatusChanged(plugin)
            return
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def setReceiveMode(self, plugin):
        try:
            plugin.btnAction = 1  # receive
            color = f"color: rgba{str(SPECKLE_COLOR)};"
            self.receiveModeButton.setStyleSheet(
                "border: 0px;" f"color: rgba{str(SPECKLE_COLOR)};" "padding: 10px;"
            )
            self.sendModeButton.setIcon(QIcon(ICON_SEND_BLACK))
            self.sendModeButton.setStyleSheet(
                "QPushButton {border: 0px; color: black; padding: 10px;} QPushButton:hover { "
                + f"background-color: rgba{str(COLOR_HIGHLIGHT)};"
                + " };"
            )
            self.receiveModeButton.setIcon(QIcon(ICON_RECEIVE_BLUE))
            self.sendModeButton.setFlat(True)
            self.receiveModeButton.setFlat(False)
            self.runButton.setProperty("text", " RECEIVE")
            self.runButton.setIcon(QIcon(ICON_RECEIVE))
            self.commitLabel.setEnabled(True)
            self.commitDropdown.setEnabled(True)

            self.layersWidget.setEnabled(False)
            self.messageLabel.setEnabled(False)
            self.messageInput.setEnabled(False)
            self.saveLayerSelection.setEnabled(False)
            self.layerSendModeDropdown.setEnabled(False)
            self.setMapping.setEnabled(False)
            self.commit_web_view.setEnabled(True)

            self.runBtnStatusChanged(plugin)
            return
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def completeStreamSection(self, plugin):
        return

    def populateUI(self, plugin):
        try:
            self.populateLayerSendModeDropdown()
            self.populateProjectStreams(plugin)

            # self.runBtnStatusChanged(plugin)
            # self.runButton.setEnabled(False)

        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def setActiveCommit(self, plugin):
        try:
            # print("__setActiveCommit")
            # print(plugin.active_commit)
            if plugin.active_branch is None:
                if (
                    plugin.active_stream is not None
                    and plugin.active_stream[1] is not None
                ):
                    branchName = self.streamBranchDropdown.currentText()
                    for b in plugin.active_stream[1].branches.items:
                        if b.name == branchName:
                            branch = b
                            plugin.active_branch = b
                            break

            if plugin.active_branch is None:
                return
            # print(plugin.active_branch.name)

            current_id_text = str(self.commitDropdown.currentText()).split(" ")[0]
            # print(current_id_text)
            if current_id_text == "":  # populate commits still in progress
                return

            if len(plugin.active_branch.commits.items) > 0:
                if "Latest" in current_id_text:
                    plugin.active_commit = plugin.active_branch.commits.items[0]
                    return
                for c in plugin.active_branch.commits.items:
                    if c.id == current_id_text:
                        plugin.active_commit = c
                        return
                # only if not found:
                plugin.active_commit = plugin.active_branch.commits.items[0]
            else:
                plugin.active_commit = None
        except Exception as e:
            plugin.active_commit = None
            print(e)

    def runBtnStatusChanged(self, plugin):
        try:
            commitStr = str(self.commitDropdown.currentText())
            branchStr = str(self.streamBranchDropdown.currentText())

            if commitStr == "":  # populate commits still in progress
                return

            if plugin.btnAction == 1:  # on receive
                if commitStr == "":
                    self.runButton.setEnabled(False)
                else:
                    self.runButton.setEnabled(True)

            if plugin.btnAction == 0:  # on send
                if branchStr == "":
                    self.runButton.setEnabled(False)
                elif (
                    self.layerSendModeDropdown.currentIndex() == 1
                    and len(plugin.dataStorage.current_layers) == 0
                ):  # saved layers; but the list is empty
                    self.runButton.setEnabled(False)
                else:
                    self.runButton.setEnabled(True)
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def layerSendModeChange(self, plugin, runMode=None):
        try:
            if (
                self.layerSendModeDropdown.currentIndex() == 0 or runMode == 1
            ):  # by manual selection OR receive mode
                self.layersWidget.setEnabled(False)

            elif self.layerSendModeDropdown.currentIndex() == 1 and (
                runMode == 0 or runMode is None
            ):  # by saved AND when Send mode
                self.layersWidget.setEnabled(True)

            branchStr = str(self.streamBranchDropdown.currentText())
            if self.layerSendModeDropdown.currentIndex() == 0:
                if branchStr == "":
                    self.runButton.setEnabled(False)  # by manual selection
                else:
                    self.runButton.setEnabled(True)  # by manual selection
            elif self.layerSendModeDropdown.currentIndex() == 1:
                self.runBtnStatusChanged(plugin)  # by saved

        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def populateSavedLayerDropdown(self, plugin):
        try:
            # print(self.dataStorage.saved_layers)
            if not self:
                return
            self.layersWidget.clear()

            self.dataStorage.current_layers.clear()
            layers = self.dataStorage.saved_layers
            if not layers:
                return

            for i, layer in enumerate(layers):
                self.dataStorage.current_layers.append(layer)
                listItem = self.fillLayerList(layer[0], layer[2])
                self.layersWidget.addItem(listItem)

            self.layersWidget.setIconSize(QtCore.QSize(20, 20))
            self.runBtnStatusChanged(plugin)
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def populateSelectedLayerDropdown(self, plugin):
        try:
            if not self:
                return
            self.layersWidget.clear()

            for layer_tuple in plugin.dataStorage.current_layers:
                listItem = self.fillLayerList(layer_tuple[0], layer_tuple[2])
                self.layersWidget.addItem(listItem)

            self.layersWidget.setIconSize(QtCore.QSize(20, 20))
            self.runBtnStatusChanged(plugin)
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def fillLayerList(self, layer, layerType="generic"):
        try:
            listItem = QListWidgetItem(layer.name())

            try:  # if QGIS
                from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsIconUtils

                if (
                    isinstance(layer, QgsRasterLayer)
                    and layer.width() * layer.height() > 1000000
                ):
                    listItem.setIcon(QIcon(ICON_XXL))

                elif isinstance(layer, QgsVectorLayer) and layer.featureCount() > 20000:
                    listItem.setIcon(QIcon(ICON_XXL))
                else:
                    from qgis.core import QgsIconUtils

                    icon = QgsIconUtils().iconForLayer(layer)
                    listItem.setIcon(icon)
                    # print(icon)
            except Exception as e:
                print(e)
                icons = {
                    "generic": ICON_GENERIC,
                    "polygon": ICON_POLYGON,
                    "point": ICON_POINT,
                    "line": ICON_LINE,
                    "raster": ICON_RASTER,
                }
                icon = QIcon(icons[layerType])
                listItem.setIcon(icon)

            return listItem

        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def enableElements(self, plugin):
        try:
            self.sendModeButton.setEnabled(plugin.is_setup)
            self.receiveModeButton.setEnabled(plugin.is_setup)
            self.runButton.setEnabled(plugin.is_setup)
            self.streams_add_button.setEnabled(plugin.is_setup)
            self.commit_web_view.setEnabled(plugin.active_commit is not None)
            self.reportBtn.setEnabled(False)
            if plugin.is_setup is False:
                self.streams_remove_button.setEnabled(plugin.is_setup)
            self.streamBranchDropdown.setEnabled(plugin.is_setup)
            self.layerSendModeDropdown.setEnabled(plugin.is_setup)
            self.commitLabel.setEnabled(False)
            self.commitDropdown.setEnabled(False)
            self.show()
            self.setSendMode(plugin)
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def populateProjectStreams(self, plugin):
        return

    def onActiveStreamChanged(self, plugin):
        try:
            if not self:
                return
            index = self.streamList.currentIndex()
            if (len(plugin.current_streams) == 0 and index == 1) or (
                len(plugin.current_streams) > 0 and index == len(plugin.current_streams)
            ):
                self.populateProjectStreams(plugin)
                plugin.onStreamCreateClicked()
                return
            if len(plugin.current_streams) == 0:
                return
            if index == -1:
                return

            try:
                plugin.active_stream = plugin.current_streams[index]
            except:
                plugin.active_stream = None

            self.populateActiveStreamBranchDropdown(plugin)
            self.populateActiveCommitDropdown(plugin)
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def populateLayerSendModeDropdown(self):
        if not self:
            return
        try:
            self.layerSendModeDropdown.clear()
            self.layerSendModeDropdown.addItems(
                ["Send selected layers", "Send saved layers"]
            )
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def populateActiveStreamBranchDropdown(self, plugin):
        if not self:
            return
        try:
            # print("___ populateActiveStreamBranchDropdown___")
            # print(plugin.active_branch)
            if plugin.active_stream is None:
                return
            active_branch = copy(plugin.active_branch)
            active_commit = copy(plugin.active_commit)
            keep_branch = True  # case of search by URL
            if active_branch is None:  # case of populating from Saved Streams
                keep_branch = False
            # print(active_branch)

            # print(1)
            self.streamBranchDropdown.clear()  # activates "populate commit"
            # print(2)
            if isinstance(plugin.active_stream[1], SpeckleException):
                logToUser("Some streams cannot be accessed", level=1, plugin=self)
                return
            elif (
                plugin.active_stream is None
                or plugin.active_stream[1] is None
                or plugin.active_stream[1].branches is None
            ):
                return
            # print(3)
            # print(plugin.active_branch)

            # here the commit dropdown is triggered
            self.streamBranchDropdown.addItems(
                [f"{branch.name}" for branch in plugin.active_stream[1].branches.items]
            )
            # print(4)
            self.streamBranchDropdown.addItems(["Create New Branch"])
            # print(5)
            if keep_branch is True:
                plugin.active_branch = active_branch
                if active_commit is not None:
                    plugin.active_commit = active_commit
                elif len(plugin.active_branch.commits.items) > 0:
                    plugin.active_commit = plugin.active_branch.commits.items[0]
                # else:
                #    plugin.active_commit = plugin.active_branch.commits.items[0]
            # print(plugin.active_branch)

            # set index to current (if added from URL)
            if (
                plugin.active_branch is not None
                and plugin.active_branch in plugin.active_stream[1].branches.items
            ):
                # print("__________SET BRANCH TEXT")
                # print(plugin.active_branch.name)
                if keep_branch is True:
                    plugin.active_branch = active_branch
                    plugin.active_commit = active_commit
                # print(plugin.active_branch.name)
                self.streamBranchDropdown.setCurrentText(
                    plugin.active_branch.name
                )  # activates "populate commit"
                # print(6)

        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            return

    def populateActiveCommitDropdown(self, plugin):
        if not self:
            return
        try:
            # print("________populateActiveCommitDropdown")
            # print(plugin.active_commit)
            if plugin.active_stream is None:
                print("Active stream is None")
                return
            branchName = self.streamBranchDropdown.currentText()
            # print(f"CURRENT BRANCH TEXT: {branchName}")
            if branchName == "":
                return
            if branchName == "Create New Branch":
                self.streamBranchDropdown.setCurrentText("main")
                plugin.onBranchCreateClicked()
                return
            branch = None

            # print("__clear commit dropdwn")
            # print(plugin.active_commit)
            self.commitDropdown.clear()
            if isinstance(plugin.active_stream[1], SpeckleException):
                logToUser("Some streams cannot be accessed", level=1, plugin=self)
                return
            elif plugin.active_stream[1]:
                for b in plugin.active_stream[1].branches.items:
                    if b.name == branchName:
                        branch = b
                        plugin.active_branch = b
                        break

            if len(branch.commits.items) > 0:
                commits = []
                commits.append("")
                # commits.append("Latest commit from this branch")
                # self.commitDropdown.addItem("Latest commit from this branch")

                # commits = []
                for commit in branch.commits.items:
                    sourceApp = (
                        str(commit.sourceApplication)
                        .replace(" ", "")
                        .split(".")[0]
                        .split("-")[0]
                    )
                    commits.append(
                        f"{commit.id}"
                        + " | "
                        + f"{sourceApp}"
                        + " | "
                        + f"{commit.message}"
                    )
                self.commitDropdown.addItems(commits)

                # set index to current (if added from URL)
                if (
                    plugin.active_commit is not None
                    and plugin.active_commit in branch.commits.items
                ):
                    # print("set index to current (if added from URL) ")
                    # print(plugin.active_commit)
                    self.commitDropdown.setCurrentText(
                        f"{plugin.active_commit.id}"
                        + " | "
                        + f"{plugin.active_commit.sourceApplication}"
                        + " | "
                        + f"{plugin.active_commit.message}"
                    )
                else:  # overwrite active commit if plugin.active_commit is None:
                    # print("set index to 1st")
                    plugin.active_commit = branch.commits.items[0]
            else:
                plugin.active_commit = None

            self.commitDropdown.setItemText(0, "Latest commit from this branch")
            # enable or disable web view button
            # print("_________ENABLE OR DISABLE")
            # print(plugin.active_commit)
            # print(f"CURRENT TEXT2: {self.streamBranchDropdown.currentText()}")
            if plugin.active_commit is not None and plugin.btnAction == 1:
                self.commit_web_view.setEnabled(True)
            else:
                self.commit_web_view.setEnabled(False)

        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3], plugin=self)
            # print(str(e) + "::" + str(inspect.stack()[0][3]))
            return

    def onStreamRemoveButtonClicked(self, plugin):
        return

    def cancelOperations(self):
        return
