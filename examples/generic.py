import sys
sys.path.append("..")
import random
import PUI
PUI.BACKEND = random.choice(["Tk", "Qt5", "PySide6", "flet"])
from PUI import State
from PUI.generic import *

data = State()
class Example(Window):
    def __init__(self):
        super().__init__(title="blah")
        data.var = 0

    def content(self):
        with VBox() as scope:
            with HBox() as _:
                Button("-", self.on_minus)
                Label(f"{data.var}")
                Button("+", self.on_plus)

            with HBox() as _:
                for i in range(0, data.var):
                    Label(f"{i}")

    def on_minus(self):
        data.var -= 1

    def on_plus(self):
        data.var += 1

root = Example()
root.run()
