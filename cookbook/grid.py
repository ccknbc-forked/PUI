from .config import *

@PUI
def GridExample():
    with Grid():
        Label("R=0 C=0").grid(row=0, column=0)
        Label("R=1 C=0").grid(row=1, column=0)
        Label("R=0 C=1, rowspan=2").grid(row=0, column=1, rowspan=2)
        Label("R=2 C=1").grid(row=2, column=1)

    Spacer()