
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore

from specklepy_qt_ui.qt_ui.utils import splitTextIntoLines 

def logToUser(msg: str, func=None, level: int = 2, plugin = None, url = "", blue = False):
      print("Log to user")
      msg = str(msg)
      if func is not None and func != "None": 
            print(msg + " " + url + "::" + str(func))
      else: 
            print(msg + " " + url )

      dockwidget = plugin
      try: 
            if url == "" and blue is False: # only for info messages
                  msg = addLevelSymbol(msg, level)
                  if func is not None: 
                        msg += "::" + str(func)
            
            if dockwidget is None: return
            
            new_msg = splitTextIntoLines(msg)
            dockwidget.msgLog.sendMessage.emit(new_msg, level, url, blue)
            
      except Exception as e: print(e); return 

def addLevelSymbol(msg: str, level: int):
      if level == 0: msg = "🛈 " + msg
      if level == 1: msg = "⚠️ " + msg
      if level == 2: msg = "❗ " + msg
      return msg 

def displayUserMsg(msg: str, func=None, level: int = 2): 
      try:
            window = createWindow(msg, func, level)
            window.exec_() 
      except Exception as e: print(e)

def createWindow(msg_old: str, func=None, level: int = 2):
      print("Create window")
      window = None
      try:
            # https://www.techwithtim.net/tutorials/pyqt5-tutorial/messageboxes/
            window = QMessageBox()
            msg = ""
            if len(msg_old)>80:
                  msg = splitTextIntoLines(msg_old)
            else: 
                  msg = msg_old
      
            window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            if level==0: 
                  window.setWindowTitle("Info (Speckle)")
                  window.setIcon(QMessageBox.Icon.Information)
            if level==1: 
                  window.setWindowTitle("Warning (Speckle)")
                  window.setIcon(QMessageBox.Icon.Warning)
            elif level==2: 
                  window.setWindowTitle("Error (Speckle)")
                  window.setIcon(QMessageBox.Icon.Critical)
            window.setFixedWidth(200)

            if func is not None:
                  window.setText(str(msg + "\n" + str(func)))
            else: 
                  window.setText(str(msg))
            print(window)
      except Exception as e: print(e)
      return window 

