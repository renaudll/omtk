from omtk.libs.libQt import QtGui, QtCore, getMayaWindow
from omtk.libs import libSerialization
import logging, os
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Dynamic type creation for enum in python 2.7
def enum(**enums):
    return type('Enum', (), enums)

class HitBox(object):
    _default_width = 42
    _default_height = 42
    _default_posx = 0
    _default_posy = 0

    _color_selected = QtGui.QColor(128,128,128,128)
    _color_unselected = QtGui.QColor(0, 0, 0, 128)

    def __init__(self, **kwargs):
        self.width = HitBox._default_width
        self.height = HitBox._default_height
        self.posx = HitBox._default_posx
        self.posy = HitBox._default_posy
        self.label = 'debug'
        self.__dict__.update(kwargs)
        self._hitbox = QtCore.QRect(self.posx, self.posy, self.width, self.height)
        self.need_update = True
        self.is_selected = False

    @property
    def selected(self):
        return self.is_selected

    @selected.setter
    def selected(self, val):
        if self.is_selected != val:
            self.is_selected = val
            self.need_update = True

    def draw(self, qp):
        #if self.need_update is True:
        qp.drawRect(self._hitbox)
        qp.fillRect(self._hitbox, HitBox._color_selected if self.selected else HitBox._color_unselected)
        qp.drawText(self._hitbox, QtCore.Qt.AlignCenter, self.label)
        #self.need_update = False

    def __getattr__(self, attname):
        return getattr(self._hitbox, attname)

class PickerCore(object):
    def __init__(self):
        self.hitboxes = [
            HitBox(posx=20),
            HitBox(posx=80),
            HitBox(posx=140)
        ]

    def select(self, items, more=False):
        if not isinstance(items, list): items = [items]
        # todo: optimise
        if more is False:
            for hitbox in self.hitboxes:
                hitbox.selected = False
        for hitbox in items:
            hitbox.is_selected = True

    def draw(self, qt):
        for hitbox in self.hitboxes:
            hitbox.draw(qt)

    # DEPRECATED
    def selectPoint(self, x, y, **kwargs):
        hitbox = next((h for h in self.hitboxes if h.contains(x, y)), None)
        if hitbox:
            log.debug('Hit {0}'.format(hitbox))
            self.select(hitbox, **kwargs)

    def selectRect(self, rect, **kwargs):
        # Hack: Ensure that the rectangle always have at least a size of 1
        # This allow us to painlessly implement click selection
        if rect.width() == 0: rect.setWidth(1)
        if rect.height() == 0: rect.setHeight(1)

        log.debug('Selecting using rectangle {0}'.format(rect))
        hitboxes = [h for h in self.hitboxes if h.intersect(rect)]
        self.select(hitboxes)

    def offset_active(self, x, y):
        print x, y
        for hitbox in self.hitboxes:
            if hitbox.selected:
                hitbox._hitbox.moveTo(
                    hitbox.x() + x,
                    hitbox.y() + y
                )

class PickerWidget(QtGui.QWidget):
    def __init__(self, data, *args, **kwargs):
        self.core = data
        super(PickerWidget, self).__init__(*args, **kwargs)
        self._selection_start = QtCore.QPoint(0,0)
        self.is_selecting = False

    def _get_selection_rect(self):
        mouse_pos = self.mapFromGlobal(QtGui.QCursor.pos())
        return_val = QtCore.QRect(self._selection_start, mouse_pos)
        print return_val
        return return_val

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        self.core.draw(qp)

        # Draw selection rectangle
        if self.is_selecting:
            qSelectionRect = self._get_selection_rect()
            qp.drawRect(qSelectionRect)

        qp.end()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        log.debug('Click at {0}, {1}'.format(x, y))

        self.is_selecting = True
        self._selection_start = event.pos()

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.update()

    def mouseReleaseEvent(self, event):
        self.is_selecting = False

        mouse_pos = event.pos()
        x = self._selection_start.x()
        y = self._selection_start.y()
        w = mouse_pos.x() - x
        h = mouse_pos.y() - y
        qtSelectionRectangle = QtCore.QRect(x, y, w, h)
        self.core.selectRect(qtSelectionRectangle)
        self.update()


    def keyPressEvent(self, event):
        print event.key()
        if event.key() == 16777216: # Esc
            self.close()

        # Handle hitbox offset
        if event.key() == 16777235: # up
            self.core.offset_active(0, -6)
            self.update()
        elif event.key() == 16777237: # down
            self.core.offset_active(0, 6)
            self.update()
        elif event.key() == 16777234: # left
            self.core.offset_active(-6, 0)
            self.update()
        elif event.key() == 16777236: # right
            self.core.offset_active(6, 0)
            self.update()

import pickerUI
class PickerGUI(QtGui.QMainWindow, pickerUI.Ui_MainWindow):
    def __init__(self, parent=getMayaWindow()):
        super(PickerGUI, self).__init__(None)
        self.setupUi(self)
        self.core = PickerCore()

        # HACK: Replace widget by our custom widget
        self.verticalLayout.removeWidget(self.widget)
        self.widget = PickerWidget(self.core)
        self.verticalLayout.addWidget(self.widget)
        self.update()

        self.actionImport.triggered.connect(self.import_)
        self.actionExport.triggered.connect(self.export)

    def keyPressEvent(self, event):
        print event.key()
        if event.key() == 16777216: # Esc
            self.close()

        # Handle hitbox offset
        if event.key() == 16777235: # up
            self.core.offset_active(0, -6)
            self.update()
        elif event.key() == 16777237: # down
            self.core.offset_active(0, 6)
            self.update()
        elif event.key() == 16777234: # left
            self.core.offset_active(-6, 0)
            self.update()
        elif event.key() == 16777236: # right
            self.core.offset_active(6, 0)
            self.update()

    def export(self, path=None):
        if path is None:
            path = QtGui.QFileDialog.getSaveFileName()
        print path, type(path)
        if not isinstance(path, basestring):
            return
        print 'EXPORT'
        libSerialization.export_json_file(self.core, path)

    def import_(self, path=None):
        if path is None:
            path = QtGui.QFileDialog.getOpenFileName()
        if not isinstance(path, basestring) or not os.path.exists(path):
            return
        print 'IMPORTING'
        try:
            data = libSerialization.import_json_file(path)
            if isinstance(data, PickerCore):
                self.core = data
                self.update()
        except Exception, e:
            log.exception(e)


gui = None
def show():
    global gui
    gui = PickerGUI()
    gui.show()
