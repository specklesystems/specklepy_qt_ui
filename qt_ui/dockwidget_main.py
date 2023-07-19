# -*- coding: utf-8 -*-

import inspect
import os

from specklepy_qt_ui.qt_ui.widget_transforms import MappingSendDialog
from specklepy_qt_ui.qt_ui.LogWidget import LogWidget
from specklepy_qt_ui.qt_ui.logger import logToUser
from specklepy_qt_ui.qt_ui.DataStorage import DataStorage
from specklepy_qt_ui.qt_ui.global_resources import (
    COLOR_HIGHLIGHT, 
    SPECKLE_COLOR, SPECKLE_COLOR_LIGHT, 
    ICON_LOGO, ICON_SEARCH, ICON_DELETE, ICON_DELETE_BLUE,
    ICON_SEND, ICON_RECEIVE, ICON_SEND_BLACK, ICON_RECEIVE_BLACK, 
    ICON_SEND_BLUE, ICON_RECEIVE_BLUE, 
    COLOR, BACKGR_COLOR, BACKGR_COLOR_LIGHT,
    ICON_XXL, ICON_RASTER, ICON_POLYGON, ICON_LINE, ICON_POINT, ICON_GENERIC,
)
from specklepy.logging.exceptions import (SpeckleException, GraphQLException)
from specklepy.logging import metrics


from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QCheckBox, QListWidgetItem, QHBoxLayout, QWidget 
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), os.path.join("ui", "dockwidget_main.ui") )
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
        #self.saveSurveyPoint.setFlat(True)
        self.saveLayerSelection.setFlat(True)
        self.reloadButton.setFlat(True)
        self.closeButton.setFlat(True)

        # https://stackoverflow.com/questions/67585501/pyqt-how-to-use-hover-in-button-stylesheet
        backgr_image_del = f"border-image: url({ICON_DELETE_BLUE});"
        self.streams_add_button.setIcon(QIcon(ICON_SEARCH))
        self.streams_add_button.setMaximumWidth(25)
        self.streams_add_button.setStyleSheet("QPushButton {padding:3px;padding-left:5px;border: none; text-align: left;} QPushButton:hover { " + f"background-color: rgb{str(COLOR_HIGHLIGHT)};" + f"{COLOR}" + " }")
        self.streams_remove_button.setIcon(QIcon(ICON_DELETE))
        self.streams_remove_button.setMaximumWidth(25)
        self.streams_remove_button.setStyleSheet("QPushButton {padding:3px;padding-left:5px;border: none; text-align: left; image-position:right} QPushButton:hover { " + f"background-color: rgb{str(COLOR_HIGHLIGHT)};" + f"{COLOR}" + " }") #+ f"{backgr_image_del}" 

        self.saveLayerSelection.setStyleSheet("QPushButton {text-align: right;} QPushButton:hover { " + f"{COLOR}" + " }")
        #self.saveSurveyPoint.setStyleSheet("QPushButton {text-align: right;} QPushButton:hover { " + f"{COLOR}" + " }")
        self.reloadButton.setStyleSheet("QPushButton {text-align: left;} QPushButton:hover { " + f"{COLOR}" + " }")
        self.closeButton.setStyleSheet("QPushButton {text-align: right;} QPushButton:hover { " + f"{COLOR}" + " }")


        self.sendModeButton.setStyleSheet("QPushButton {padding: 10px; border: 0px; " + f"color: rgb{str(SPECKLE_COLOR)};"+ "} QPushButton:hover { "  + "}" ) 
        self.sendModeButton.setIcon(QIcon(ICON_SEND_BLUE))
        
        self.receiveModeButton.setFlat(True)
        self.receiveModeButton.setStyleSheet("QPushButton {padding: 10px; border: 0px;}"+ "QPushButton:hover { "  + f"background-color: rgb{str(COLOR_HIGHLIGHT)};" + "}" ) 
        self.receiveModeButton.setIcon(QIcon(ICON_RECEIVE_BLACK))

        self.runButton.setStyleSheet("QPushButton {color: white;border: 0px;border-radius: 17px;padding: 10px;"+ f"{BACKGR_COLOR}" + "} QPushButton:hover { "+ f"{BACKGR_COLOR_LIGHT}" + " }")
        #self.runButton.setGeometry(0, 0, 150, 30)
        self.runButton.setMaximumWidth(200)
        self.runButton.setIcon(QIcon(ICON_SEND))

        # insert checkbox 
        l = self.verticalLayout

    def runSetup(self, plugin):
        
        #self.addDataStorage(plugin)
        self.addLabel(plugin)
        self.addProps(plugin)
        #self.createMappingDialog()

    def addProps(self, plugin):
        
        # add widgets that will only show on event trigger 
        logWidget = LogWidget(parent=self)
        self.layout().addWidget(logWidget)
        self.msgLog = logWidget 
        self.msgLog.dockwidget = self 
        
        self.msgLog.active_account = plugin.dataStorage.active_account
        self.msgLog.speckle_version = plugin.version

        self.setMapping.setFlat(True)
        self.setMapping.setStyleSheet("QPushButton {text-align: right;} QPushButton:hover { " + f"{COLOR}" + " }")
        
        self.crsSettings.setFlat(True)
        self.crsSettings.setStyleSheet("QPushButton {text-align: right;} QPushButton:hover { " + f"{COLOR}" + " }")
    
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
            text_label.setStyleSheet("border: 0px;"
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
                if isinstance(plugin.version, str): version = str(plugin.version)
            except: pass


            version_label = QtWidgets.QPushButton(version)
            version_label.setStyleSheet("border: 0px;"
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
            connect_box = QHBoxLayout(widget)
            connect_box.addWidget(text_label) #, alignment=Qt.AlignCenter) 
            connect_box.addWidget(version_label) 
            connect_box.setContentsMargins(0, 0, 0, 0)
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
            if self.msgLog.size().height() != 0: # visible
                self.msgLog.setGeometry(0, 0, self.msgLog.parentWidget.frameSize().width(), self.msgLog.parentWidget.frameSize().height()) #.resize(self.frameSize().width(), self.frameSize().height())
        except Exception as e:
            return

    def clearDropdown(self):
        try:
            self.streamBranchDropdown.clear()
            self.commitDropdown.clear()
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def reloadDialogUI(self, plugin):
        try:
            self.clearDropdown()
            self.populateUI(plugin) 
            self.enableElements(plugin)
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
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
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def closeEvent(self, event):
        try:
            self.closingPlugin.emit()
            event.accept()
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return
        
    def addMsg(self, text:str, level:int, url:str, blue:bool):
        self.msgLog.addButton(text, level, url, blue)

    def setupOnFirstLoad(self, plugin):
        try:
            
            self.msgLog.sendMessage.connect(self.addMsg)
            self.setMapping.clicked.connect(self.showMappingDialog)

            self.streams_add_button.clicked.connect( plugin.onStreamAddButtonClicked )
            self.reloadButton.clicked.connect(lambda: self.refreshClicked(plugin))
            self.closeButton.clicked.connect(lambda: self.closeClicked(plugin))

            self.sendModeButton.clicked.connect(lambda: self.setSendMode(plugin))
            self.layerSendModeDropdown.currentIndexChanged.connect( lambda: self.layerSendModeChange(plugin) )
            self.receiveModeButton.clicked.connect(lambda: self.setReceiveMode(plugin))

            self.streamBranchDropdown.currentIndexChanged.connect( lambda: self.runBtnStatusChanged(plugin) )
            self.commitDropdown.currentIndexChanged.connect( lambda: self.runBtnStatusChanged(plugin) )

            self.closingPlugin.connect(plugin.onClosePlugin)
            return 
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def onClickLogo(self):
        import webbrowser
        url = "https://speckle.systems/"
        webbrowser.open(url, new=0, autoraise=True)

    def refreshClicked(self, plugin):
        try:
            try:
                metrics.track("Connector Action", plugin.dataStorage.active_account, {"name": "Refresh", "connector_version": str(plugin.version)})
            except Exception as e:
                logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=plugin.dockwidget )
            
            plugin.reloadUI()
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def closeClicked(self, plugin):
        try:
            try:
                metrics.track("Connector Action", plugin.dataStorage.active_account, {"name": "Close", "connector_version": str(plugin.version)})
            except Exception as e:
                logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=plugin.dockwidget )
            
            plugin.onClosePlugin()
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def setSendMode(self, plugin):
        try:
            plugin.btnAction = 0 # send 
            color = f"color: rgb{str(SPECKLE_COLOR)};"
            self.sendModeButton.setStyleSheet("border: 0px;"
                                        f"color: rgb{str(SPECKLE_COLOR)};"
                                        "padding: 10px;")
            self.sendModeButton.setIcon(QIcon(ICON_SEND_BLUE))
            self.sendModeButton.setFlat(False)
            self.receiveModeButton.setFlat(True)
            self.receiveModeButton.setStyleSheet("QPushButton {border: 0px; color: black; padding: 10px; } QPushButton:hover { " + f"background-color: rgb{str(COLOR_HIGHLIGHT)};" +  " };")
            self.receiveModeButton.setIcon(QIcon(ICON_RECEIVE_BLACK))
            self.runButton.setProperty("text", " SEND")
            self.runButton.setIcon(QIcon(ICON_SEND))

            # enable sections only if in "saved streams" mode 
            if self.layerSendModeDropdown.currentIndex() == 1: self.layersWidget.setEnabled(True)
            self.saveLayerSelection.setEnabled(True)
            self.commitLabel.setEnabled(False)
            self.commitDropdown.setEnabled(False)
            self.messageLabel.setEnabled(True)
            self.messageInput.setEnabled(True)
            self.layerSendModeDropdown.setEnabled(True)
            self.setMapping.setEnabled(True)

            self.runBtnStatusChanged(plugin)
            return
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return
    
    def setReceiveMode(self, plugin):
        try:
            plugin.btnAction = 1 # receive 
            color = f"color: rgb{str(SPECKLE_COLOR)};"
            self.receiveModeButton.setStyleSheet("border: 0px;"
                                        f"color: rgb{str(SPECKLE_COLOR)};"
                                        "padding: 10px;")
            self.sendModeButton.setIcon(QIcon(ICON_SEND_BLACK))
            self.sendModeButton.setStyleSheet("QPushButton {border: 0px; color: black; padding: 10px;} QPushButton:hover { " + f"background-color: rgb{str(COLOR_HIGHLIGHT)};"  + " };")
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

            self.runBtnStatusChanged(plugin)
            return
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def completeStreamSection(self, plugin):
        return

    def populateUI(self, plugin):
        try:
            self.populateLayerSendModeDropdown()
            self.populateProjectStreams(plugin)

            self.runBtnStatusChanged(plugin)
            self.runButton.setEnabled(False) 
            
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return
    
    def runBtnStatusChanged(self, plugin):
        try:
            commitStr = str(self.commitDropdown.currentText())
            branchStr = str(self.streamBranchDropdown.currentText())

            if plugin.btnAction == 1: # on receive
                if commitStr == "": 
                    self.runButton.setEnabled(False) 
                else: 
                    self.runButton.setEnabled(True) 
            
            if plugin.btnAction == 0: # on send 
                if branchStr == "": 
                    self.runButton.setEnabled(False) 
                elif self.layerSendModeDropdown.currentIndex() == 1 and len(plugin.dataStorage.current_layers) == 0: # saved layers; but the list is empty 
                    self.runButton.setEnabled(False)
                else:
                    self.runButton.setEnabled(True)
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return
            

    def layerSendModeChange(self, plugin, runMode = None):
        try:
            if self.layerSendModeDropdown.currentIndex() == 0 or runMode == 1: # by manual selection OR receive mode
                self.layersWidget.setEnabled(False)
                
            elif self.layerSendModeDropdown.currentIndex() == 1 and (runMode == 0 or runMode is None): # by saved AND when Send mode
                self.layersWidget.setEnabled(True)
            
            branchStr = str(self.streamBranchDropdown.currentText())
            if self.layerSendModeDropdown.currentIndex() == 0:
                if branchStr == "": self.runButton.setEnabled(False) # by manual selection
                else: self.runButton.setEnabled(True) # by manual selection
            elif self.layerSendModeDropdown.currentIndex() == 1: self.runBtnStatusChanged(plugin) # by saved

        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def populateSavedLayerDropdown(self, plugin):
        
        try:
            print(self.dataStorage.saved_layers)
            if not self: return
            self.layersWidget.clear()

            self.dataStorage.current_layers.clear() 
            layers = self.dataStorage.saved_layers
            if not layers: return 
            
            for i, layer in enumerate(layers):
                self.dataStorage.current_layers.append(layer) 
                listItem = self.fillLayerList(layer[0], layer[2])
                self.layersWidget.addItem(listItem)

            self.layersWidget.setIconSize(QtCore.QSize(20, 20))
            self.runBtnStatusChanged(plugin)
        except Exception as e: 
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def populateSelectedLayerDropdown(self, plugin):
        
        try:
            if not self: return
            self.layersWidget.clear()

            for layer_tuple in plugin.dataStorage.current_layers:
                listItem = self.fillLayerList(layer_tuple[0], layer_tuple[2]) 
                self.layersWidget.addItem(listItem)

            self.layersWidget.setIconSize(QtCore.QSize(20, 20))
            self.runBtnStatusChanged(plugin)
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def fillLayerList(self, layer, layerType = "generic"):
        try:
            icon_xxl = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", " size-xxl.png") 
            listItem = QListWidgetItem(layer.name()) 

            try: # if QGIS
                from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsIconUtils 

                if isinstance(layer, QgsRasterLayer) and layer.width()*layer.height() > 1000000:
                        listItem.setIcon(QIcon(icon_xxl))
                
                elif isinstance(layer, QgsVectorLayer) and layer.featureCount() > 20000: 
                        listItem.setIcon(QIcon(icon_xxl))
                else:
                    from qgis.core import QgsIconUtils 
                    icon = QgsIconUtils().iconForLayer(layer)
                    listItem.setIcon(icon)
                    #print(icon)
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
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return


    def enableElements(self, plugin):
        try:
            self.sendModeButton.setEnabled(plugin.is_setup)
            self.receiveModeButton.setEnabled(plugin.is_setup)
            self.runButton.setEnabled(plugin.is_setup)
            self.streams_add_button.setEnabled(plugin.is_setup)
            if plugin.is_setup is False: self.streams_remove_button.setEnabled(plugin.is_setup) 
            self.streamBranchDropdown.setEnabled(plugin.is_setup)
            self.layerSendModeDropdown.setEnabled(plugin.is_setup)
            self.commitLabel.setEnabled(False)
            self.commitDropdown.setEnabled(False)
            self.show()
            self.setSendMode(plugin)
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return
    
    def populateProjectStreams(self, plugin):
        return 

    def onActiveStreamChanged(self, plugin):
        try:
            if not self: return
            index = self.streamList.currentIndex()
            if (len(plugin.current_streams) == 0 and index ==1) or (len(plugin.current_streams)>0 and index == len(plugin.current_streams)): 
                self.populateProjectStreams(plugin)
                plugin.onStreamCreateClicked()
                return
            if len(plugin.current_streams) == 0: return
            if index == -1: return

            try: plugin.active_stream = plugin.current_streams[index]
            except: plugin.active_stream = None

            self.populateActiveStreamBranchDropdown(plugin)
            self.populateActiveCommitDropdown(plugin)
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return
        
    def populateLayerSendModeDropdown(self):
        if not self: return
        try:
            self.layerSendModeDropdown.clear()
            self.layerSendModeDropdown.addItems(
                ["Send selected layers", "Send saved layers"]
            )
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def populateActiveStreamBranchDropdown(self, plugin):
        if not self: return
        try:
            if plugin.active_stream is None: return
            self.streamBranchDropdown.clear()
            if isinstance(plugin.active_stream[1], SpeckleException): 
                logToUser("Some streams cannot be accessed", level = 1, plugin = self)
                return
            elif plugin.active_stream is None or plugin.active_stream[1] is None or plugin.active_stream[1].branches is None:
                return
            self.streamBranchDropdown.addItems(
                [f"{branch.name}" for branch in plugin.active_stream[1].branches.items]
            )
            self.streamBranchDropdown.addItems(["Create New Branch"])
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            return

    def populateActiveCommitDropdown(self, plugin):
        if not self: return
        try:
            self.commitDropdown.clear()
            if plugin.active_stream is None: return
            branchName = self.streamBranchDropdown.currentText()
            if branchName == "": return
            if branchName == "Create New Branch": 
                self.streamBranchDropdown.setCurrentText("main")
                plugin.onBranchCreateClicked()
                return
            branch = None
            if isinstance(plugin.active_stream[1], SpeckleException): 
                logToUser("Some streams cannot be accessed", level = 1, plugin = self)
                return
            elif plugin.active_stream[1]:
                for b in plugin.active_stream[1].branches.items:
                    if b.name == branchName:
                        branch = b
                        break
            
            self.commitDropdown.addItem("Latest commit from this branch")

            commits = []
            for commit in branch.commits.items:
                sourceApp = str(commit.sourceApplication).replace(" ","").split(".")[0].split("-")[0]
                commits.append(f"{commit.id}"+ " | " + f"{sourceApp}" + " | " + f"{commit.message}")
            self.commitDropdown.addItems(commits)
        except Exception as e:
            logToUser(e, level = 2, func = inspect.stack()[0][3], plugin=self)
            print(str(e) + "::" + str(inspect.stack()[0][3]))
            return

    def onStreamRemoveButtonClicked(self, plugin):
        return 

    def cancelOperations(self):
        return 
