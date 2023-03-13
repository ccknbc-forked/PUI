from .. import *
# from .base import *
import flet as ft

class FWindow(PUIView):
    def __init__(self, title=None, size=None):
        super().__init__()
        self.ready = False
        self.title = title
        self.size = size

    def flet_app(self, page: ft.Page):
        self.ui = page
        self.ui.title = self.title
        self.ready = True
        self.update()

    def addChild(self, child):
        self.ui.add(child.ui)

    def removeChild(self, child):
        self.ui.remove(child.ui)

    def start(self):
        ft.app(self.flet_app)
