#!/usr/bin/python

import htmlPy
import os

app = htmlPy.AppGUI(title=u"htmlPy Quickstart", maximized=True)

app.template_path = os.path.abspath("templates/")
app.static_path = os.path.abspath("static/")

app.template = ("index.html", {})

app.start()