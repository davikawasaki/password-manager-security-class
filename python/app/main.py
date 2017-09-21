import os
import htmlPy
from PyQt4 import QtGui

# Initial config
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# GUI initializations
app = htmlPy.AppGUI(title=u"Password Manager - Created by André Poletto, Davi Kawasaki and João Vitor Bertoncini", maximized=True, plugins=True)


# GUI configurations
app.static_path = os.path.join(BASE_DIR, "static/")
app.template_path = os.path.join(BASE_DIR, "templates/")

app.web_app.setMinimumWidth(1024)
app.web_app.setMinimumHeight(768)
app.window.setWindowIcon(QtGui.QIcon(BASE_DIR + "/static/img/favicon.ico"))

# Binding of back-end functionalities with GUI

# Import back-end functionalities
from securityApp import Register

# Register back-end functionalities
app.bind(Register())

# Instructions for running application
if __name__ == "__main__":
    # The driver file will have to be imported everywhere in back-end.
    # So, always keep app.start() in if __name__ == "__main__" conditional
    app.start()