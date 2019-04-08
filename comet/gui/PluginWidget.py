import os

from PyQt5 import QtWidgets
from PyQt5 import uic

from .. import PLUGINS_DIR

class PluginWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(PluginWidget, self).__init__(parent)
        self.__autoLoadUi()

    def __autoLoadUi(self):
        basename = "{}.ui".format(self.__class__.__name__)
        filename = os.path.join(PLUGINS_DIR, basename)
        if os.path.isfile(filename):
            uic.loadUi(filename, self)

    def onStart(self):
        """Overload by custom plugin class."""
        pass

    def onStop(self):
        """Overload by custom plugin class."""
        pass
