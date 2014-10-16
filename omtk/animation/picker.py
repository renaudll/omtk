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

    _dagpath = 'test'
    _command_language = 'python'

    def __init__(self, **kwargs):
        self.width = HitBox._default_width # todo: remove
        self.height = HitBox._default_height # todo: remove
        self.posx = HitBox._default_posx # todo: remove
        self.posy = HitBox._default_posy # todo: remove
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

    # todo: convert to property
    def set_position(self, newpos):
        if not isinstance(newpos, QtCore.QPoint): raise IOError
        self.posx = newpos.x()
        self.posy = newpos.y()
        self._hitbox.moveTo(QtCore.QPoint(self.posx, self.posy))

    def draw(self, qp):
        #if self.need_update is True:
        qp.drawRect(self._hitbox)
        qp.fillRect(self._hitbox, HitBox._color_selected if self.selected else HitBox._color_unselected)
        qp.drawText(self._hitbox, QtCore.Qt.AlignCenter, self.label)
        #self.need_update = False

    def execute(self):
        if self._command_language == 'python':
            from maya import cmds
            cmds.select(self._dagpath)
        else:
            raise NotImplementedError('Invalid command_language: {0}'.format(self._command_language))

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
        # Clear if the user miss
        if len(items) == 0:
            for h in self.hitboxes:
                h.selected = False
            return

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

    def hitboxes_from_pos(self, x, y, **kwargs):
        return next((h for h in self.hitboxes if h.contains(x, y)), None)

    def hitboxes_from_qrect(self, rect, **kwargs):
        # Hack: Ensure that the rectangle always have at least a size of 1
        # This allow us to painlessly implement click selection
        if rect.width() == 0: rect.setWidth(1)
        if rect.height() == 0: rect.setHeight(1)

        log.debug('Selecting using rectangle {0}'.format(rect))
        return [h for h in self.hitboxes if h.intersect(rect)]

    def selectPoint(self, x, y, **kwargs):
        hitbox = self.hitboxes_from_pos(x, y, **kwargs)
        if hitbox:
            log.debug('Hit {0}'.format(hitbox))
            self.select(hitbox, **kwargs)

    def selectRect(self, rect, **kwargs):
        hitboxes = self.hitboxes_from_qrect(rect)
        self.select(hitboxes)


    def offset_active(self, x, y):
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
        self.old_mouse_pos = None

        self.selected_items = None
        self.is_dragging = False

    def _get_selection_rect(self):
        mouse_pos = self.mapFromGlobal(QtGui.QCursor.pos())
        return_val = QtCore.QRect(self._selection_start, mouse_pos)
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

        self.selected_items = [h for h in self.core.hitboxes if h.is_selected]
        mouse_pos = self.mapFromGlobal(QtGui.QCursor.pos())

        # if the user click miss, clear selection
        hitbox = self.core.hitboxes_from_pos(mouse_pos.x(), mouse_pos.y())
        if not hitbox: # If nothing is clicked on
            log.debug("Changing state: mouseSelect")
            self.is_selecting = True
            self._selection_start = event.pos()
        elif hitbox.is_selected: # If the thing that is clicked on is selected
            log.debug("Changing state: mouseDrag")
            self.is_dragging = True
            self.dragged_items = {}
            for h in self.core.hitboxes:
                if h.is_selected:
                    self.dragged_items[h] = h._hitbox.topLeft()
            self.old_mouse_pos = mouse_pos
        else:
            log.debug("Changing state: mouseSelect")
            self.is_selecting = True
            self._selection_start = event.pos()


    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.update()

        if self.is_dragging:
            mouse_pos = self.mapFromGlobal(QtGui.QCursor.pos())
            delta = mouse_pos - self.old_mouse_pos
            for hitbox, old_pos in self.dragged_items.iteritems():
                #log.debug('Moving {0}'.format(hitbox))
                new_pos = old_pos + delta
                hitbox.set_position(new_pos)
            self.update()

    def mouseReleaseEvent(self, event):
        if self.is_selecting:
            mouse_pos = event.pos()
            x = self._selection_start.x()
            y = self._selection_start.y()
            w = mouse_pos.x() - x
            h = mouse_pos.y() - y
            qtSelectionRectangle = QtCore.QRect(x, y, w, h)
            self.core.selectRect(qtSelectionRectangle)
            self.is_selecting = False

        self.update()

        self.dragged_items = {}
        self.is_dragging = False

        log.debug("Exiting state")

        print self._selection_start
        print self.is_selecting
        print self.old_mouse_pos

        print self.selected_items
        print self.is_dragging


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
reload(pickerUI)
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
