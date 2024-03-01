import inspect
import os
from typing import List, Union
import urllib.parse

try:
    from specklepy_qt_ui.qt_ui.DataStorage import DataStorage
    from specklepy_qt_ui.qt_ui.utils.logger import logToUser
    from specklepy_qt_ui.qt_ui.utils.utils import constructCommitURLfromServerCommit
    from specklepy_qt_ui.qt_ui.utils.logger import displayUserMsg
except ModuleNotFoundError: 
    from speckle.specklepy_qt_ui.qt_ui.DataStorage import DataStorage
    from speckle.specklepy_qt_ui.qt_ui.utils.logger import logToUser
    from speckle.specklepy_qt_ui.qt_ui.utils.utils import constructCommitURLfromServerCommit
    from speckle.specklepy_qt_ui.qt_ui.utils.logger import displayUserMsg

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSignal

from specklepy.core.api.models import Stream, Branch, Commit
from specklepy.core.api.client import SpeckleClient
from specklepy.logging.exceptions import SpeckleException
from specklepy.core.api.credentials import get_local_accounts  # , StreamWrapper
from specklepy.core.api.wrapper import StreamWrapper
from specklepy.logging import metrics


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.join(os.path.dirname(__file__), "ui", "add_stream_modal.ui"))
)


class AddStreamModalDialog(QtWidgets.QWidget, FORM_CLASS):
    search_button: QtWidgets.QPushButton = None
    search_text_field: QtWidgets.QLineEdit = None
    search_results_list: QtWidgets.QListWidget = None
    dialog_button_box: QtWidgets.QDialogButtonBox = None
    accounts_dropdown: QtWidgets.QComboBox

    stream_results: List[Stream] = []
    branch_result: Branch = None
    commit_result: Commit = None
    speckle_client: Union[SpeckleClient, None] = None
    dataStorage: DataStorage = None

    # Events
    handleStreamAdd = pyqtSignal(object)

    def __init__(self, parent=None, speckle_client: SpeckleClient = None):
        super(AddStreamModalDialog, self).__init__(
            parent, QtCore.Qt.WindowStaysOnTopHint
        )
        self.speckle_client = speckle_client
        self.setupUi(self)
        self.setWindowTitle("Add Speckle stream")

        self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

    def connect(self):
        self.search_button.clicked.connect(self.onSearchClicked)
        self.search_results_list.currentItemChanged.connect(self.searchResultChanged)
        self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(
            self.onOkClicked
        )
        self.dialog_button_box.button(
            QtWidgets.QDialogButtonBox.Cancel
        ).clicked.connect(self.onCancelClicked)
        self.accounts_dropdown.currentIndexChanged.connect(self.onAccountSelected)
        self.populate_accounts_dropdown()

    def searchResultChanged(self):
        try:
            index = self.search_results_list.currentIndex().row()
            if index == -1:
                self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(
                    False
                )
            else:
                self.dialog_button_box.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(
                    True
                )
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3])
            return

    def getAllStreams(self):
        try:
            query = ""
            sw = None
            results = []
            if self.speckle_client is not None:
                results = self.speckle_client.stream.search(query)
                try:
                    metrics.track(
                        "Connector Action",
                        self.dataStorage.active_account,
                        {
                            "name": "Stream Search By Name",
                            "connector_version": str(self.dataStorage.plugin_version),
                        },
                    )
                except Exception as e:
                    logToUser(e, level=2, func=inspect.stack()[0][3])

            elif self.speckle_client is None:
                logToUser(
                    f"Account cannot be authenticated: {self.accounts_dropdown.currentText()}",
                    level=1,
                    func=inspect.stack()[0][3],
                )

            self.stream_results = results
            self.populateResultsList()

        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3])
            return

    def onSearchClicked(self):
        try:
            query = self.search_text_field.text()
            sw = None
            streams = []
            branch = None
            commit = None
            if "http" in query and len(query.split("/")) >= 3:  # URL
                sw = StreamWrapper(
                    query,
                )
                stream = sw.get_client().stream.get(
                    id=sw.stream_id, branch_limit=100, commit_limit=100
                )
                if isinstance(stream, Stream):
                    streams = [stream]

                    if sw.type == "branch":
                        branch_name = sw.branch_name
                        for br in stream.branches.items:
                            name = urllib.parse.quote(br.name)
                            if br.name == branch_name:
                                branch = br
                                break
                    if sw.type == "commit":
                        commit_id = sw.commit_id
                        for br in stream.branches.items:
                            for com in br.commits.items:
                                if com.id == commit_id:
                                    branch = br
                                    commit = com
                                    break
                elif isinstance(stream, Exception):
                    print(stream)
                try:
                    metrics.track(
                        "Connector Action",
                        self.dataStorage.active_account,
                        {
                            "name": "Stream Search By URL",
                            "connector_version": str(self.dataStorage.plugin_version),
                        },
                    )
                except Exception as e:
                    logToUser(e, level=2, func=inspect.stack()[0][3])

            elif self.speckle_client is not None:
                streams = self.speckle_client.stream.search(query)
                try:
                    metrics.track(
                        "Connector Action",
                        self.dataStorage.active_account,
                        {
                            "name": "Stream Search By Name",
                            "connector_version": str(self.dataStorage.plugin_version),
                        },
                    )
                except Exception as e:
                    logToUser(e, level=2, func=inspect.stack()[0][3])

            elif self.speckle_client is None:
                logToUser(
                    f"Account cannot be authenticated: {self.accounts_dropdown.currentText()}",
                    level=1,
                    func=inspect.stack()[0][3],
                )

            self.stream_results = streams
            self.branch_result = branch
            self.commit_result = commit
            self.populateResultsList(sw)

        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3])
            if isinstance(e, SpeckleException):
                displayUserMsg(e.message, level=2)
            else:
                displayUserMsg(str(e), level=2)
            return

    def populateResultsList(self, sw=None):
        try:
            self.search_results_list.clear()
            if isinstance(self.stream_results, SpeckleException):
                logToUser(
                    "Some streams cannot be accessed",
                    level=1,
                    func=inspect.stack()[0][3],
                )
                return
            for stream in self.stream_results:
                host = ""
                if sw is not None:
                    host = sw.get_account().serverInfo.url
                else:
                    host = self.speckle_client.account.serverInfo.url

                if isinstance(stream, SpeckleException):
                    logToUser(
                        "Some streams cannot be accessed",
                        level=1,
                        func=inspect.stack()[0][3],
                    )
                else:
                    self.search_results_list.addItems(
                        [
                            f"{stream.name}, {stream.id} | {host}"  # for stream in self.stream_results
                        ]
                    )
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3])
            return

    def onOkClicked(self):
        try:
            if isinstance(self.stream_results, SpeckleException):
                logToUser(
                    "Selected stream cannot be accessed: "
                    + str(self.stream_results.message),
                    level=1,
                    func=inspect.stack()[0][3],
                )
                return
            else:
                try:
                    index = self.search_results_list.currentIndex().row()
                    # stream = self.stream_results[index]
                    item = self.search_results_list.item(index)
                    url = constructCommitURLfromServerCommit(
                        item.text().split(" | ")[1],
                        item.text().split(", ")[1].split(" | ")[0],
                    )
                    sw = StreamWrapper(url)

                    try:
                        metrics.track(
                            "Connector Action",
                            self.dataStorage.active_account,
                            {
                                "name": "Stream Add From Search",
                                "connector_version": str(
                                    self.dataStorage.plugin_version
                                ),
                            },
                        )
                    except Exception as e:
                        logToUser(e, level=2, func=inspect.stack()[0][3])

                    # acc = sw.get_account() #get_local_accounts()[self.accounts_dropdown.currentIndex()]
                    self.handleStreamAdd.emit(
                        (sw, self.branch_result, self.commit_result)
                    )  # StreamWrapper(f"{acc.serverInfo.url}/streams/{stream.id}?u={acc.userInfo.id}"))
                    self.close()
                except Exception as e:
                    logToUser(
                        "Some streams cannot be accessed: " + str(e),
                        level=1,
                        func=inspect.stack()[0][3],
                    )
                    print(e)
                    return
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3])
            print(e)
            return

    def onCancelClicked(self):
        try:
            self.close()
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3])
            return

    def onAccountSelected(self, index=0):
        try:
            try:
                metrics.track(
                    "Connector Action",
                    self.dataStorage.active_account,
                    {
                        "name": "Account Select",
                        "connector_version": str(self.dataStorage.plugin_version),
                    },
                )
            except Exception as e:
                logToUser(e, level=2, func=inspect.stack()[0][3])

            account = self.speckle_accounts[index]
            self.speckle_client = SpeckleClient(
                account.serverInfo.url, account.serverInfo.url.startswith("https")
            )

            try:
                self.speckle_client.authenticate_with_token(token=account.token)
            except SpeckleException as ex:
                raise Exception(f"Dependencies versioning error: {ex.message}")

            self.getAllStreams()

        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3])
            return

    def populate_accounts_dropdown(self):
        try:
            # Populate the accounts comboBox
            self.speckle_accounts = get_local_accounts()
            self.accounts_dropdown.clear()
            self.accounts_dropdown.addItems(
                [
                    f"{acc.userInfo.name}, {acc.userInfo.email} | {acc.serverInfo.url}"
                    for acc in self.speckle_accounts
                ]
            )
        except Exception as e:
            logToUser(e, level=2, func=inspect.stack()[0][3])
            return
