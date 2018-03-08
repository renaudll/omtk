import datetime
import logging

from omtk.qt_widgets.ui import widget_logger
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets, QtCompat

log = logging.getLogger('omtk')

def log_level_to_str(level):
    if level >= logging.CRITICAL:
        return 'Critical'
    if level >= logging.ERROR:
        return 'Error'
    if level >= logging.WARNING:
        return 'Warning'
    return 'Info'


class UiLoggerModel(QtCore.QAbstractTableModel):
    HEADER = ('Date', 'Type', 'Message')

    ROW_LEVEL = 1
    ROW_MESSAGE = 2
    ROW_DATE = 0

    COLOR_FOREGROUND_ERROR = QtGui.QColor(0, 0, 0)
    COLOR_FOREGROUND_WARNING = QtGui.QColor(255, 255, 0)
    COLOR_FOREGROUND_INFO = None
    COLOR_FOREGROUND_DEBUG = QtGui.QColor(128, 128, 128)

    COLOR_BACKGROUND_ERROR = QtGui.QColor(255, 0, 0)
    COLOR_BACKGROUND_WARNING = None
    COLOR_BACKGROUND_INFO = None
    COLOR_BACKGROUND_DEBUG = None

    def __init__(self, parent, data, *args):
        super(UiLoggerModel, self).__init__(parent, *args)
        self.items = data
        self.header = self.HEADER

    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == QtCore.Qt.ForegroundRole:
            record = self.items[index.row()]
            level = record.levelno
            if level >= logging.ERROR:
                return self.COLOR_FOREGROUND_ERROR
            if level >= logging.WARNING:
                return self.COLOR_FOREGROUND_WARNING
            if level <= logging.DEBUG:
                return self.COLOR_FOREGROUND_DEBUG
            return self.COLOR_FOREGROUND_INFO

        if role == QtCore.Qt.BackgroundColorRole:
            record = self.items[index.row()]
            level = record.levelno
            if level >= logging.ERROR:
                return self.COLOR_BACKGROUND_ERROR
            if level >= logging.WARNING:
                return self.COLOR_BACKGROUND_WARNING
            if level <= logging.DEBUG:
                return self.COLOR_BACKGROUND_DEBUG
            return self.COLOR_BACKGROUND_INFO

        if role != QtCore.Qt.DisplayRole:
            return None

        record = self.items[index.row()]
        col_index = index.column()
        if col_index == self.ROW_LEVEL:
            level = record.levelno
            return log_level_to_str(level)
        elif col_index == self.ROW_MESSAGE:
            return record.message
        elif col_index == self.ROW_DATE:
            return str(datetime.datetime.fromtimestamp(record.created))
        else:
            Exception("Unexpected row. Expected 0 or 1, got {0}".format(
                col_index
            ))

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def add(self, item):
        num_items = len(self.items)
        self.beginInsertRows(QtCore.QModelIndex(), num_items, num_items)
        self.items.append(item)
        self.endInsertRows()

    def reset(self):
        """Backport of Qt4 .reset method()"""
        self.beginResetModel()
        self.endResetModel()


class UiLoggerProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        super(UiLoggerProxyModel, self).__init__(*args, **kwargs)
        self._log_level_interest = logging.WARNING
        self._log_search_query = None

    def set_loglevel_filter(self, loglevel, update=True):
        self._log_level_interest = loglevel
        if update:
            self.reset()

    def set_log_query(self, query, update=True):
        self._log_search_query = query if query else None
        if update:
            self.reset()

    def filterAcceptsRow(self, source_row, index):
        model = self.sourceModel()
        record = model.items[source_row]

        # Filter using query
        if self._log_search_query:
            query = self._log_search_query.lower()
            if not query in record.message.lower():
                return False

        # Filter using log level
        level = record.levelno
        if level < self._log_level_interest:
            return False

        return True

    def reset(self):
        """Backport of Qt4 .reset method()"""
        self.beginResetModel()
        self.endResetModel()


class WidgetLogger(QtWidgets.QWidget):
    onRecordAdded = QtCore.Signal()

    def __init__(self, parent=None):
        super(WidgetLogger, self).__init__(parent=parent)
        self._logger = None

        self.ui = widget_logger.Ui_Form()
        self.ui.setupUi(self)

        #
        # Configure logging view
        #

        # Used to store the logging handlers
        self._logging_handlers = []
        # Used to store the records so our TableView can filter them
        self._logging_records = []
        # Used to store what log level we are interested.
        # We use a separated value here since we might want to keep other log handlers active (external files, script editor, etc)
        self._logging_level = logging.WARNING

        table_model = UiLoggerModel(self, self._logging_records)
        table_proxy_model = UiLoggerProxyModel(self)
        table_proxy_model.setSourceModel(table_model)
        table_proxy_model.setDynamicSortFilter(False)
        self.ui.tableView_logs.setModel(table_proxy_model)
        # self.ui.tableView_logs.setModel(self._table_log_model)

        header = self.ui.tableView_logs.horizontalHeader()
        header.setStretchLastSection(True)
        QtCompat.setSectionResizeMode(header, QtWidgets.QHeaderView.ResizeToContents)

        # Connect events
        self.ui.comboBox_log_level.currentIndexChanged.connect(self.update_log_search_level)
        self.ui.lineEdit_log_search.textChanged.connect(self.update_log_search_query)
        self.ui.pushButton_logs_clear.pressed.connect(self.on_log_clear)
        self.ui.pushButton_logs_save.pressed.connect(self.on_log_save)

    def set_logger(self, logger):
        if self._logger:
            self.remove_logger_handler()
        self._logger = logger
        self.create_logger_handler()

    def model(self):
        return self.ui.tableView_logs.model().sourceModel()

    def create_logger_handler(self):
        class QtHandler(logging.Handler):
            """Custom Qt Handler for our logger"""

            def __init__(self, main_class):
                """
                Initialize the handler
                """
                logging.Handler.__init__(self)
                self._widget = main_class

            def emit(self, record):
                """
                When the handler emit something, update the table view messages
                :param record: The record that been emitted
                :return:
                """
                # TODO - Find a solution for the problem where if the UI is not closed correctly,
                # tableView_log is not valid
                self._widget._logging_records.append(record)
                try:
                    self._widget.ui.tableView_logs.model().reset()
                    self._widget.ui.tableView_logs.scrollToBottom()
                except:
                    self._widget.remove_logger_handler()
                try:
                    self._widget.onRecordAdded.emit()
                except Exception, e:
                    log.error(e)

        handler = QtHandler(self)

        # handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        assert(self._logger)
        self._logger.addHandler(handler)
        self._logging_handlers.append(handler)

    def remove_logger_handler(self):
        if self._logging_handlers:
            for handler in self._logging_handlers:
                self._logger.removeHandler(handler)
            self._logging_handlers = []

    def update_log_search_query(self):
        query = self.ui.lineEdit_log_search.text()
        self.ui.tableView_logs.model().set_log_query(query)

    def update_log_search_level(self):
        index = self.ui.comboBox_log_level.currentIndex()
        model = self.ui.tableView_logs.model()
        if index == 0:
            model.set_loglevel_filter(logging.ERROR)
        elif index == 1:
            model.set_loglevel_filter(logging.WARNING)
        elif index == 2:
            model.set_loglevel_filter(logging.INFO)
        elif index == 3:
            model.set_loglevel_filter(logging.DEBUG)

    def _save_logs(self, path):
        with open(path, 'w') as fp:
            # Write header
            fp.write('Date,Level,Message\n')

            # Write content
            for record in self._logging_records:
                fp.write('{0},{1},{2}\n'.format(
                    str(datetime.datetime.fromtimestamp(record.created)),
                    log_level_to_str(record.levelno),
                    record.message
                ))

    def on_log_save(self):
        default_name = datetime.datetime.now().strftime("%Y-%m-%d-%Hh%Mm%S")
        if self.root:
            default_name = '{0}_{1}'.format(default_name, self.root.name)

        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save logs", '{0}.log'.format(default_name), ".log")
        if path:
            self._save_logs(path)

    def on_log_clear(self):
        del self._logging_records[:]
        self.ui.tableView_logs.model().reset()
