import random
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt import QtGui
from qgis.PyQt.QtGui import QIcon, QPixmap
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QListWidgetItem,
    QAction,
    QDockWidget,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
)
from qgis.PyQt import QtCore
from qgis.PyQt.QtCore import pyqtSignal, Qt

# from qgis.PyQt import QtCore, QtWidgets #, QtWebEngineWidgets
from PyQt5 import *
from PyQt5.QtCore import QUrl
import plotly.express as px
from PyQt5.QtWebKitWidgets import QWebView
import pandas as pd
import os

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.join(os.path.dirname(__file__), "ui", "dashboard.ui"))
)


class SpeckleDashboard(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()
    dataStorage = None

    dataNumeric: dict = {}
    dataText: dict = {}

    current_filter: str = ""
    current_index: int = -1
    selectionDropdown: QtWidgets.QComboBox
    dataWidget: QtWidgets.QListWidget
    chart: QWidget
    browser = None
    existing_web: int = 0

    def __init__(self, parent=None):
        """Constructor."""
        super(SpeckleDashboard, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.browser = QWebView(self)  # https://github.com/qgis/QGIS/issues/26048
        self.setupUi(self)

        self.selectionDropdown.clear()
        self.selectionDropdown.addItems(["area", "property value"])
        self.selectionDropdown.setCurrentIndex(0)

        self.selectionDropdown.currentIndexChanged.connect(self.populateUI)

    def setup(self):
        self.dataWidget.clear()
        for i, (key, val) in enumerate(self.dataNumeric.items()):
            # property_filter = self.selectionDropdown.currentText()
            if self.current_filter in key or key in self.current_filter:
                listItem = QListWidgetItem(f"{key}: {val}")
                self.dataWidget.addItem(listItem)

    def populateUI(self, force=0):
        print(self.selectionDropdown.currentIndex())
        print(self.current_filter)
        if self.selectionDropdown.currentText() == "":
            self.current_filter = "area"
            self.current_index = 0
            self.setup()
            self.selectionDropdown.setIndex(0)

            self.createChart()
        elif self.selectionDropdown.currentText() != self.current_filter:
            self.current_filter = self.selectionDropdown.currentText()
            self.current_index = self.selectionDropdown.currentIndex()
            self.setup()
            self.createChart()
        if force == 1:
            self.setup()
            self.createChart()

    def update(self):
        self.dataNumeric = {}
        self.dataText = {}

        for i in range(10):
            # keys = ["key1", "key2", "key3", "key4", "key5"]
            # key = keys[random.randint(0, 4)]
            value = random.randint(10, 100)
            self.dataNumeric.update({"index": i, f"area {random.randint(1, 4)}": value})
        for i in range(10):
            # keys = ["key1", "key2", "key3", "key4", "key5"]
            # key = keys[random.randint(0, 4)]
            value = random.randint(10, 100)
            self.dataNumeric.update(
                {
                    "index": i + 10,
                    f"property value {random.randint(1, 4)}": [
                        value,
                        value * 0.5,
                        value * 2,
                    ],
                }
            )

        r"""
        layer = getLayerByName(self.dataStorage.project, "Speckle_dashboard")
        fields = layer.fields()
        for i, key in enumerate(fields.names()):
            if key in ["Branch URL", "commit_id", "updated"]:
                continue

            value = None
            variant = fields.at(i).type()

            if "value" in key:
                value = []
            if "area" in key:
                value = 0

            for feat in layer.getFeatures():
                if isinstance(value, List):
                    if feat[key] is not None:
                        list_vals = (
                            feat[key]
                            .replace("[", "")
                            .replace("]", "")
                            .replace("'", "")
                            .split(",")
                        )
                        value.extend([x for x in list_vals if x != ""])
                        print(value)

                elif isinstance(value, float) or isinstance(value, int):
                    if feat[key] is not None:
                        value += feat[key]

            self.dataNumeric.update({key: value})
        """

        self.populateUI(force=1)

    def createChart(self):
        # https://stackoverflow.com/questions/60522103/how-to-have-plotly-graph-as-pyqt5-widget
        print("PRINT DATAFRAME")
        df = pd.DataFrame.from_dict(self.dataNumeric, orient="index", columns=["value"])
        df2 = df.reset_index()
        print(df2)

        property_filter = str(self.selectionDropdown.currentText())
        if len(property_filter) <= 1:
            property_filter = "area"
        df2 = df2[df2["index"].str.lower().str.contains(property_filter)]
        print(df2)

        if "area" in property_filter:
            fig = px.pie(
                df2,
                values="value",
                names="index",
                title="Land use distribution",
                hole=0.5,
            )

        elif "value" in property_filter:
            all_column_vals = df2["value"].to_list()

            all_column_vals_separated = []
            [all_column_vals_separated.extend(x) for x in all_column_vals]

            all_vals = [float(x) for x in all_column_vals_separated]
            df2 = pd.DataFrame([{property_filter: val} for val in all_vals])
            fig = px.histogram(df2, x=property_filter, title="Property values")
        else:
            df2 = df2.loc["area" in df2["index"]]
            fig = px.pie(
                df2, values="value", names="index", title="Land use distribution"
            )
        print(df2)

        # remove all buttons
        # try:
        #    for i in reversed(range(self.chart.layout.count())):
        #        self.chart.layout.itemAt(i).widget().setParent(None)
        # except: pass

        if self.existing_web == 0:
            self.browser = QWebView(self)

        self.browser.setHtml(fig.to_html(include_plotlyjs="cdn"))
        # self.browser.setUrl(QUrl("https://speckle.xyz/streams/e2effcfa27/commits/f76cedd9a6"))

        self.chart.layout = QHBoxLayout(self.chart)
        self.browser.setMaximumHeight(400)

        if self.existing_web == 0:
            self.chart.layout.addWidget(self.browser)
            self.existing_web = 1

        return
        # https://www.pythonguis.com/tutorials/plotting-pyqtgraph/

        graphWidget = pg.PlotWidget()

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # plot data: x, y values
        graphWidget.plot(hour, temperature)

        # remove all buttons
        try:
            for i in reversed(range(self.chart.layout.count())):
                self.chart.layout.itemAt(i).widget().setParent(None)
        except:
            pass

        self.chart.layout = QHBoxLayout(self.chart)
        self.chart.layout.addWidget(graphWidget)

        # set the QWebEngineView instance as main widget
        # self.setCentralWidget(plot_widget)
