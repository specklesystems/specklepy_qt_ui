
import inspect
from typing import Any, List

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QHBoxLayout

import webbrowser
from specklepy.logging import metrics
from specklepy.core.api.credentials import Account

from specklepy_qt_ui.qt_ui.global_resources import (
    BACKGR_COLOR, BACKGR_COLOR_LIGHT, BACKGR_COLOR_GREY, BACKGR_COLOR_TRANSPARENT, BACKGR_COLOR_HIGHLIGHT
)
from specklepy_qt_ui.qt_ui.widget_report import ReportDialog 

class LogWidget(QWidget):
    
    msgs: List[str] = []
    used_btns: List[int] = []
    btns: List[QPushButton]
    max_msg: int
    sendMessage = pyqtSignal(object)
    dataStorage = None
    reportBtn = None

    active_account: Account
    speckle_version: str
    dockwidget: Any = None
    reportDialog: Any = None
    
    # constructor
    def __init__(self, parent=None):
        super(LogWidget, self).__init__(parent)
        self.parentWidget = parent
        print(self.parentWidget)
        self.max_msg = 8
        
        # create a temporary floating button 
        width = 0 #parent.frameSize().width()
        height = 0 # parent.frameSize().height()
        
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgba(250,250,250,80);")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 60, 10, 20)
        self.layout.setAlignment(Qt.AlignBottom) 
        self.setGeometry(0, 0, width, height)
        self.createBtns()

        self.hide() 

    def createBtns(self):
        # generate 100 buttons to use later
        self.btns = []
        for i in range(self.max_msg):
            button = QPushButton(f"👌 Error") # to '{streamName}' Sent , v
            #button.setStyleSheet("QPushButton {color: black; border: 0px;border-radius: 17px;padding: 20px;height: 40px;text-align: left;"+ f"{BACKGR_COLOR_GREY}" + "}")
            button.clicked.connect(lambda: self.btnClicked())
            #button.clicked.connect(lambda: self.hide())
            self.btns.append(button)

    # overriding the mouseReleaseEvent method
    def mouseReleaseEvent(self, event):
        print("Mouse Release Event")
        self.hide() 
        #self.parentWidget.hideError()

    def hide(self):
        print("___HIDE LOG WIDGET")
        
        self.setGeometry(0, 0, 0, 0)

        # remove all buttons
        for i in reversed(range(self.layout.count())): 
           #print(self.layout.itemAt(i))
           #print(self.layout.itemAt(i).widget())
           self.layout.itemAt(i).widget().setParent(None)

        self.createBtns()
        # remove list of used btns
        self.used_btns.clear()
        self.msgs.clear()

    def addButton(self, obj: dict):
        print("Add button")
        text: str = obj["text"]
        level: int = obj["level"]
        url: str  = obj["url"]
        blue: bool = obj["blue"]
        report: bool = obj["report"]

        self.setGeometry(0, 0, self.parentWidget.frameSize().width(), self.parentWidget.frameSize().height())
        
        # find index of the first unused button
        btn, index = self.getNextBtn()
        print(btn)
        btn.setAccessibleName(url)
        print(btn)
        btn.setText(text)
        self.resizeToText(btn)

        widget = QWidget()
        boxLayout = QHBoxLayout(widget)

        reportBtn = QPushButton(f"📈 Report") # to '{streamName}' Sent , v
        reportBtn.clicked.connect(lambda: self.showReport())
        new_grey = BACKGR_COLOR_GREY.replace("1);","0.2);")
        new_grey_highlight = BACKGR_COLOR_HIGHLIGHT.replace("1);","0.3);")
        reportBtn.setStyleSheet("QPushButton {color: white; border-radius: 17px;padding:0px;padding-left: 10px;padding-right: 10px;text-align: center;"+ f"{new_grey}" + "} QPushButton:hover { "+ f"{new_grey_highlight}" + " }")
        reportBtn.setMaximumWidth(150)

        spacer = QPushButton("")
        spacer.setStyleSheet("QPushButton {padding:0px;"+ f"{BACKGR_COLOR_TRANSPARENT}" + "}")
        spacer.setMaximumWidth(10)
        
        # add btns to widget layout 
        boxLayout.addWidget(btn) #, alignment=Qt.AlignCenter) 
        if report is True: 
            boxLayout.addWidget(reportBtn)
            boxLayout.addWidget(spacer)

        if url != "":
            widget.setStyleSheet("QWidget {border-radius: 17px;padding: 20px;height: 40px;text-align: left;"+ f"{BACKGR_COLOR}" + "} QWidget:hover { "+ f"{BACKGR_COLOR_LIGHT}" + " }")
            btn.setStyleSheet("QPushButton {color: white;border: 0px; padding:0px; padding-left: 10px;text-align: left;"+ f"{BACKGR_COLOR_TRANSPARENT}" + "}")
        else: # without url 
            if blue is False: 
                widget.setStyleSheet("QWidget {border-radius: 17px;padding: 20px;height: 40px;text-align: left;"+ f"{BACKGR_COLOR_GREY}" + "}")
                btn.setStyleSheet("QPushButton {color: black; border: 0px; padding:0px; padding-left: 10px;text-align: left;"+ f"{BACKGR_COLOR_TRANSPARENT}" + "}")
            else: # blue, no URL (after receive)
                widget.setStyleSheet("QWidget {border-radius: 17px;padding: 20px;height: 40px;text-align: left;"+ f"{BACKGR_COLOR}" + "}")
                btn.setStyleSheet("QPushButton {color: white;border: 0px; padding:0px; padding-left: 10px;text-align: left;"+ f"{BACKGR_COLOR_TRANSPARENT}" + "}")
        
        self.reportBtn = reportBtn 

        self.layout.addWidget(widget) #, alignment=Qt.AlignCenter) 
        self.msgs.append(text)
        self.used_btns.append(1)

    def showReport(self):
        self.reportDialog = ReportDialog()
        self.reportDialog.dataStorage = self.dataStorage
        self.reportDialog.applyReport()
        self.reportDialog.show()
        return
    
    def openURL(self, url: str = ""):
        try:
            metrics.track("Connector Action", self.dataStorage.active_account, {"name": "Open In Web", "connector_version": str(self.speckle_version)})
        except Exception as e:
            print(e)  
            print(inspect.stack()[0][3]) 
            
        if url is not None and url != "":
            webbrowser.open(url, new=0, autoraise=True)
        

    def btnClicked(self, url = ""):
        try:
            btn = self.sender()
            url = btn.accessibleName()

            if url == "" or not isinstance(url, str): 
                return
            elif isinstance(url, str): 
                if url.startswith("http"): 
                    self.openURL(url) 
                elif url.startswith("cancel"):
                    self.parentWidget.cancelOperations()

        except Exception as e: 
            print(e)
            pass #logger.logToUser(str(e), level=2, func = inspect.stack()[0][3])
        #self.hide()

    def getNextBtn(self):
        index = len(self.used_btns) # get the next "free" button 
        print(index)
        print(self.btns)

        if index >= len(self.btns): 
            # remove first button
            print(self.layout.itemAt(0).widget())
            self.layout.itemAt(0).widget().setParent(None)

            #self.used_btns.clear()
            self.createBtns()
            index = 0 

        btn = self.btns[index]
        print(btn)
        return btn, index 
    
    def getBtnByKeyword(self, keyword: str):
        try:
            new_btn = None
            for btn in self.btns:
                url = btn.accessibleName() 
                if keyword in url: 
                    new_btn = btn 
                    break
            return new_btn
        except Exception as e:
            print(e)
    
    def removeBtnUrl(self, keyword: str):
        try:
            btn = self.getBtnByKeyword(keyword)
            if btn is not None:
                btn.setAccessibleName("")
                btn.setStyleSheet("QPushButton {color: black; border: 0px; padding-left: 10px;text-align: left;"+ f"{BACKGR_COLOR_TRANSPARENT}" + "}")
                #widget.setStyleSheet("QWidget {border-radius: 17px;padding: 20px;height: 40px;text-align: left;"+ f"{BACKGR_COLOR_GREY}" + "}")
                #btn.setStyleSheet("QPushButton {color: black}")
                btn.parent().setStyleSheet("QWidget {border-radius: 17px;padding-left: 10px;height: 40px;text-align: left;"+ f"{BACKGR_COLOR_GREY}" + "}")
        
        except Exception as e:
            print(e)
        
    def resizeToText(self, btn):
        try:
            text = btn.text()
            #if len(text.split("\n"))>2:
            height = len(text.split("\n"))*25 + 20 
            btn.setMinimumHeight(height)
            return btn 
        except Exception as e: 
            print(e)
            return btn 