from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette

from ..gui import PluginWidget

class SamplePlugin(PluginWidget):

    def __init__(self, parent=None):
        super(SamplePlugin, self).__init__(parent)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)

    def onStart(self):
        palette = self.palette()
        palette.setColor(QPalette.Background, Qt.yellow)
        self.setPalette(palette)

    def onStop(self):
        palette = self.palette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)
