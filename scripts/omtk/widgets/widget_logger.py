"""
Widget that display a logger records.
"""
import datetime
import logging

from omtk.widgets.ui import widget_logger
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets, QtCompat


_COLOR_FOREGROUND_ERROR = QtGui.QColor(0, 0, 0)
_COLOR_FOREGROUND_WARNING = QtGui.QColor(255, 255, 0)
_COLOR_FOREGROUND_INFO = None
_COLOR_FOREGROUND_DEBUG = QtGui.QColor(128, 128, 128)

_COLOR_BACKGROUND_ERROR = QtGui.QColor(255, 0, 0)
_COLOR_BACKGROUND_WARNING = None
_COLOR_BACKGROUND_INFO = None
_COLOR_BACKGROUND_DEBUG = None

_AVAILABLE_LEVELS = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]

_ROLE_FILTER = QtCore.Qt.UserRole + 1


class CustomLoggingHandler(logging.Handler):
    """
    Custom Qt Handler for our logger
    """

    def __init__(self, model):
        """
        :param model: The model to add new log records to
        :type model: LogRecordModel
        """
        logging.Handler.__init__(self)
        self._model = model

    def emit(self, record):
        """
        :param record: The record that been emitted
        :type record: logging.LogRecord
        """
        self._model.add_record(record)


class LogRecordModel(QtGui.QStandardItemModel):
    """
    Qt model for displaying log records.
    """

    def __init__(self, parent=None):
        """
        :param parent: Optional parent
        :type parent: QtCore.QObject
        """
        super(LogRecordModel, self).__init__(parent)

        self.setHorizontalHeaderLabels(["Date", "Type", "Message"])

    def add_record(self, record):
        """
        :param record: The record to add
        :type record: logging.LogRecord
        """
        color_fb, color_bg = _get_text_color_from_level(record.levelno)
        timestamp, level, message = _get_record_info(record)

        items = [QtGui.QStandardItem(label) for label in (timestamp, level, message)]
        for item in items:
            item.setData(record, QtCore.Qt.UserRole)
            item.setData(message, _ROLE_FILTER)
            if color_fb:
                item.setForeground(color_fb)
            if color_bg:
                item.setBackground(color_bg)

        self.appendRow(items)

    def get_records(self):
        """
        Fetch the stored records
        """
        return [
            self.data(self.index(row, 0), QtCore.Qt.UserRole)
            for row in range(self.rowCount())
        ]

    def clear_records(self):
        """
        Clear the model from existing records.
        """
        self.removeRows(0, self.rowCount())


class LogRecordProxyModel(QtCore.QSortFilterProxyModel):
    """
    Qt proxy model that filter log records by their level of content.
    """

    def __init__(self, *args, **kwargs):
        super(LogRecordProxyModel, self).__init__(*args, **kwargs)
        self._filter_level = logging.WARNING
        self.setFilterRole(_ROLE_FILTER)
        self.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setDynamicSortFilter(False)

    def set_filter_level(self, level):
        """
        :param int level: The minimum log record level to display
        """
        self._filter_level = level
        self.invalidateFilter()

    def filterAcceptsRow(self, row, parent):  # pylint: disable=invalid-name
        """
        Determine if a row should be visible.
        Re-implement QtCore.QSortFilterProxyModel.filterAcceptsRow.

        :param int row: The row to check
        :param parent: The parent index
        :type parent: QtCore.QModelIndex
        :return: Should the row be visible?
        :rtype: bool
        """
        model = self.sourceModel()
        index = model.index(row, 0)
        record = model.data(index, QtCore.Qt.UserRole)

        # Filter using log level
        level = record.levelno
        if level < self._filter_level:
            return False

        return super(LogRecordProxyModel, self).filterAcceptsRow(row, parent)


class WidgetLogger(QtWidgets.QWidget):
    """
    Qt Widgets that display a logger entries.
    """
    def __init__(self, parent=None):
        """
        :param parent: An optional parent widget
        :type parent: QtWidgets.QWidget
        """
        super(WidgetLogger, self).__init__(parent=parent)

        self.ui = widget_logger.Ui_Form()
        self.ui.setupUi(self)

        # Configure view model
        self.model = LogRecordModel()
        self.proxy_model = LogRecordProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        self.ui.tableView_logs.setModel(self.proxy_model)

        # Configure view header
        header = self.ui.tableView_logs.horizontalHeader()
        header.setStretchLastSection(True)
        QtCompat.setSectionResizeMode(header, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.tableView_logs.verticalHeader().hide()

        # Connect events
        self.ui.lineEdit_log_search.textChanged.connect(self._on_search_text_changed)
        self.ui.comboBox_log_level.currentIndexChanged.connect(
            self._on_search_level_changed
        )
        self.ui.pushButton_logs_clear.pressed.connect(self._on_clear_records)
        self.ui.pushButton_logs_save.pressed.connect(self._on_save_records)
        self.model.rowsInserted.connect(self._on_record_added)

    def register_logger(self, logger):
        """
        :param logger: The logger to listen to
        :type logger: logging.Logger
        """
        handler = CustomLoggingHandler(self.model)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    def _on_search_text_changed(self):
        """
        Called when the user change the search text.
        """
        query = self.ui.lineEdit_log_search.text()
        self.proxy_model.setFilterWildcard(query)

    def _on_search_level_changed(self):
        """
        Called when the user change the search level drop down menu.
        """
        index = self.ui.comboBox_log_level.currentIndex()
        model = self.ui.tableView_logs.model()
        model.set_filter_level(_AVAILABLE_LEVELS[index])

    def _on_save_records(self):
        """
        Called when the user click on the save logs button.
        """
        default_name = datetime.datetime.now().strftime("%Y-%m-%d-%Hh%Mm%S")

        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save logs", "%s.log" % default_name, ".log"
        )
        if path:
            records = self.model.get_records()
            _export_records_to_csv(records, path)

    def _on_clear_records(self):
        """
        Called when the user click on the clear logs button.
        """
        self.model.clear_records()

    def _on_record_added(self, *_):
        """
        Called when a new log record is added.
        This will ensure the scrollbar is always at the bottom.
        """
        self.ui.tableView_logs.scrollToBottom()


def _log_level_to_str(level):
    """
    Convert a log level to it's human readable representation.

    :param int level: A log level
    :return: A human readable string
    :rtype: str
    """
    if level >= logging.CRITICAL:
        return "Critical"
    if level >= logging.ERROR:
        return "Error"
    if level >= logging.WARNING:
        return "Warning"
    return "Info"


def _get_record_info(record):
    """
    :param record: A log record
    :type record: logging.LogRecord
    :return: The record timestamp, type and message
    :rtype: tuple[str, str, str]
    """
    return (
        str(datetime.datetime.fromtimestamp(record.created)),
        _log_level_to_str(record.levelno),
        record.getMessage(),
    )


def _get_text_color_from_level(level):
    """
    Return the text foreground and background color to use for a provided record level.

    :param int level: A log record level
    :return: A foreground and background color
    :rtype: tuple[QtGui.QColor or None, QtGui.QColor or None]
    """
    if level >= logging.ERROR:
        return _COLOR_FOREGROUND_ERROR, _COLOR_BACKGROUND_ERROR
    if level >= logging.WARNING:
        return _COLOR_FOREGROUND_WARNING, _COLOR_BACKGROUND_WARNING
    if level <= logging.DEBUG:
        return _COLOR_FOREGROUND_DEBUG, _COLOR_BACKGROUND_DEBUG

    return _COLOR_FOREGROUND_INFO, _COLOR_BACKGROUND_INFO


def _export_records_to_csv(records, path):
    """
    :param records: A list of log records
    :type records: list of logging.LogRecord
    :param str path: A file path to write to
    """
    with open(path, "w") as steam:
        steam.write("Date,Level,Message\n")

        for record in records:
            steam.write("%s,%s,%s\n" % _get_record_info(record))
