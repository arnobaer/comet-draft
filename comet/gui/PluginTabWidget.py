import importlib

from PyQt5 import QtWidgets

class PluginTabWidget(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super(PluginTabWidget, self).__init__(parent)

    def loadPlugin(self, name):
        plugin = importlib.import_module("comet.plugins.{}".format(name))
        self.addTab(getattr(plugin, name)(self), name)

    def onStart(self):
        """Propagate start event to plugin widgets."""
        for index in range(self.count()):
            widget = self.widget(index)
            widget.onStart()

    def onStop(self):
        """Propagate stop event to plugin widgets."""
        for index in range(self.count()):
            widget = self.widget(index)
            widget.onStop()
