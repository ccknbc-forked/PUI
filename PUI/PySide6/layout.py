from .. import *
from .base import *

class QtHBox(QtBaseLayout):
    def update(self, prev):
        if prev and hasattr(prev, "ui"):
            self.ui = prev.ui
        else:
            from PySide6 import QtWidgets
            self.ui = QtWidgets.QHBoxLayout()
            self.ui.setObjectName(self.key)

class QtVBox(QtBaseLayout):
    def update(self, prev):
        if prev and hasattr(prev, "ui"):
            self.ui = prev.ui
        else:
            from PySide6 import QtWidgets
            self.ui = QtWidgets.QVBoxLayout()
            self.ui.setObjectName(self.key)