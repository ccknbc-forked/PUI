from .button import *
from .canvas import *
from .label import *
from .layout import *
from .progressbar import *
from .textfield import *
from .window import *

Window = QtWindow
HBox = QtHBox
VBox = QtVBox
Label = QtLabel
Button = QtButton
Canvas = QtCanvas
CanvasText = QtCanvasText
CanvasLine = QtCanvasLine
TextField = QtLineEdit
ProgressBar = QtProgressBar

def PUI(func):
    def func_wrapper(*args):
        class PUIViewWrapper(QPUIView):
            def __init__(self, name):
                self.name = name
                super().__init__()

            def content(self):
                return self.__wrapped_content__()

            def __wrapped_content__(self):
                return func(*args)
        ret = PUIViewWrapper(func.__name__)
        return ret

    return func_wrapper