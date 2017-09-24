#!/usr/bin/python

import os
# import sys

import PySide
import htmlPy

# from PyQt4 import QtGui
# Import back-end functionalities
from controllers import RegisterClass as RC
from controllers import ListDataClass as LDC
from controllers import RegisterDataClass as RDC
from controllers import UpdateDataClass as UDC
from controllers import RemoveDataClass as REDC
from controllers import LoginClass as LGC
from controllers import CommonClass as CC

# Initial config
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# GUI initializations
app = htmlPy.AppGUI(title=u"Password Manager - Created by Andre Poletto, Davi Kawasaki and Joao Vitor Bertoncini",
                    maximized=True, plugins=True)

# GUI configurations
app.static_path = os.path.join(BASE_DIR, "static/")
app.template_path = os.path.join(BASE_DIR, "templates/")

app.web_app.setMinimumWidth(1024)
app.web_app.setMinimumHeight(768)
app.window.setWindowIcon(PySide.QtGui.QIcon(BASE_DIR + "/static/img/icon.png"))

app.template = ("index.html", {"list": []})

# Binding of back-end functionalities with GUI

# Register back-end functionalities
app.bind(RC.Register(app))
app.bind(LDC.ListData(app))
app.bind(RDC.RegisterData(app))
app.bind(REDC.RemoveData(app))
app.bind(UDC.UpdateData(app))
app.bind(LGC.Login(app))
app.bind(CC.Common(app))

# Instructions for running application
if __name__ == "__main__":
    # The driver file will have to be imported everywhere in back-end.
    # So, always keep app.start() in if __name__ == "__main__" conditional
    app.start()
