from omtk.libs.libQt import QtGui, QtCore, getMayaWindow
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

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

    def click(self, x, y):
        hitbox = next((h for h in self.hitboxes if h.contains(x, y)), None)
        if hitbox:
            log.debug('Hit {0}'.format(hitbox))
            self.select(hitbox)

    def offset_active(self, x, y):
        print x, y
        for hitbox in self.hitboxes:
            hitbox._hitbox.moveTo(
                hitbox.x() + x,
                hitbox.y() + y
            )

import pickerUI
class PickerGUI(QtGui.QMainWindow, pickerUI.Ui_MainWindow):
    def __init__(self, parent=getMayaWindow()):
        super(PickerGUI, self).__init__(parent)
        self.setupUi(self)
        self.core = PickerCore()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        self.core.draw(qp)
        qp.end()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        log.debug('Click at {0}, {1}'.format(x, y))
        self.core.click(x, y)

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

gui = None
def show():
    global gui
    gui = PickerGUI()
    gui.show()
