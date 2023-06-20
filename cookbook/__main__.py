import sys
sys.path.append("..")

from .vbox import *
from .hbox import *
from .label import *
from .text import *
from .button import *
from .checkbox import *
from .radiobutton import *
from .combobox import *
from .modal import *
from .progressbar import *
from .timeline import *
from .textfield import *
from .scroll import *
from .canvas import *
from .tab import *
from .binding import *

# Qt specific example
from .qtwidget import *
from .qtmdi import *
from .qtsplitter import *

from .config import *

from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.style import Style
from pygments.formatters import HtmlFormatter

import inspect
from types import FunctionType

def extract_wrapped(decorated):
    if not hasattr(decorated, "__closure__"):
        return decorated
    closure = (c.cell_contents for c in decorated.__closure__)
    return next((c for c in closure if isinstance(c, FunctionType)), None)

# reloadium: after_reload
def after_reload(actions):
    PUIView.reload()

pages = [
    ("Vbox", VBoxExample),
    ("HBox", HBoxExample),
    ("Label", LabelExample),
    ("Text", TextExample),
    ("Button", ButtonExample),
    ("Checkbox", CheckboxExample),
    ("RadioButton", RadioButtonExample),
    ("Combobox", ComboboxExample),
    ("ProgressBar", ProgressBarExample),
    ("TimelineView", TimelineViewExample),
    ("TextField", TextFieldExample),
    ("Scroll", ScrollExample),
    ("Canvas", CanvasExample),
    ("Tab", TabExample),
    ("State Binding", BindingExample),
]

if PUI_BACKEND == "PySide6":
    pages.extend([
        ("WidgetWrapper", QtWidgetExample),
        ("MDI", QtMdiExample),
        ("Splitter", QtSplitterExample),
        ("Modal", ModalExample),
    ])

state = State()
state.page = pages[0]

class Example(Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tkinter(theme="classic") # macOS's aqua doesn't respect background setting for some widgets

    def content(self):
        with Window(title="PUI Cookbook", maximize=True):

            if PUI_BACKEND == "PySide6":
                with MenuBar():
                    with Menu("Menu"):
                        MenuAction("Action").trigger(print, "action")
                        MenuAction("Action2").trigger(print, "action2")
                        with Menu("Menu2"):
                            MenuAction("Action3").trigger(print, "action3")
                            MenuAction("Action4").trigger(print, "action4")
                    with Menu("Menu3"):
                            MenuAction("Action5")
                            MenuAction("Action6")

            with HBox():
                with VBox():
                    Label("Example")
                    with Scroll():
                        with VBox():
                            for p in pages:
                                Label(p[0]).click(self.select, p)
                            Spacer()

                with VBox().layout(weight=1):
                    Label("Code")
                    with Scroll():
                        code = inspect.getsource(extract_wrapped(state.page[1]))
                        if Html.supported:
                            formatter = HtmlFormatter()
                            formatter.noclasses = True
                            formatter.nobackground = True
                            highlighted_code = highlight(code, Python3Lexer(), formatter)
                            Html(highlighted_code).layout(padding=10).qt(StyleSheet={"background":"#0a0c0d"})
                        else:
                            Text(code)

                with VBox().layout(weight=1):
                    Label("Result")
                    state.page[1]()

    def select(self, page):
        print("select", page[0])
        state.page = page

root = Example()
root.run()
