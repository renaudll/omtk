import logging
from omtk.vendor.Qt import QtCore, QtWidgets, QtGui

from .ui import main_window_extended

log = logging.getLogger('omtk')


class MainWindowExtended(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowExtended, self).__init__()
        self.ui_logger = main_window_extended.Ui_MainWindow()
        self.ui_logger.setupUi(self)

        self._configure_widget_logger()

        self.set_logger(log)

    def set_logger(self, logger):
        self.ui_logger.widget_logger.set_logger(logger)

    def _configure_widget_logger(self):
        # Configure logger and status-bar
        self.ui_logger.dockWidget_logger.hide()
        self.ui_logger.widget_logger.onRecordAdded.connect(self.update_status_bar)

        # Hack: Skip subclassing QDockWidget to modify closeEvent
        def _logger_close_event(e):
            self.update_status_bar(force_show=True)
            e.accept()

        self.ui_logger.dockWidget_logger.closeEvent = _logger_close_event

        self._configure_statusbar()

    def _configure_statusbar(self):
        # Hack: Skip subclassing QStatusBar to modify mousePressEvent
        def _status_bar_mouse_press_event(e):
            self.ui_logger.dockWidget_logger.show()
            self.update_status_bar()

        statusbar = self.statusBar()
        statusbar.mousePressEvent = _status_bar_mouse_press_event
        self.update_status_bar()

    def update_status_bar(self, force_show=False):
        statusbar = self.statusBar()

        # No need for the status bar if the logger is visible
        if self.ui_logger.widget_logger.isVisible() and not force_show:
            statusbar.setStyleSheet('')
            statusbar.showMessage('')
            return

        # If the logger is now visible, the status bar will resume the logs.
        num_errors = 0
        num_warnings = 0
        model = self.ui_logger.widget_logger.model()
        for entry in model.items:
            if entry.levelno >= logging.ERROR:
                num_errors += 1
            elif entry.levelno >= logging.WARNING:
                num_warnings += 1

        # Define style
        stylesheet = ''
        if num_errors:
            stylesheet = "background-color: rgb(255, 000, 000); color: rgb(0, 0, 0);"
        elif num_warnings:
            stylesheet = "background-color: rgb(200, 200, 128); color: rgb(0, 0, 0);"
        statusbar.setStyleSheet(stylesheet)

        # Define message
        messages = []
        if num_errors:
            messages.append('{0} errors'.format(num_errors))
        elif num_warnings:
            messages.append('{0} warnings'.format(num_warnings))
        else:
            statusbar.setStyleSheet("")
        statusbar.showMessage(', '.join(messages))

    def closeEvent(self, *args):
        try:
            self.ui_logger.widget_logger.remove_logger_handler()
        except Exception, e:
            log.warning("Error removing logging handler: {0}:".format(e))
        super(MainWindowExtended, self).closeEvent(*args)
