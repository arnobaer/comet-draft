import webbrowser
import sys, os

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .. import PLUGINS_DIR
from .. import CONTENTS_URL

from .PluginTabWidget import PluginTabWidget
from .PreferencesDialog import PreferencesDialog

class MainWindow(QtWidgets.QMainWindow):
    """Main window class providing plugins.

    Keyword arguments:
    - setup -- a loaded setup instance
    - parent -- widget parent
    """

    def __init__(self, setup, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setup = setup
        self.setWindowTitle(self.tr("Comet"))
        self.resize(800, 600)
        # Create actions and toolbars
        self.createActions()
        self.createMenus()
        self.createToolbar()
        self.createStatusBar()
        # Create central tab widget
        self.pluginTabWidget = PluginTabWidget(self)
        self.setCentralWidget(self.pluginTabWidget)
        # Create preferences dialog
        self.preferencesDialog = PreferencesDialog(self)
        self.preferencesDialog.hide()

    def createActions(self):
        """Create actions."""
        # Action for quitting the program.
        self.quitAct = QtWidgets.QAction(self.tr("&Quit"), self)
        self.quitAct.setShortcut(QtGui.QKeySequence.Quit)
        self.quitAct.setStatusTip(self.tr("Quit the programm"))
        self.quitAct.triggered.connect(self.close)
        # Preferences.
        self.preferencesAct = QtWidgets.QAction(self.tr("&Preferences"), self)
        self.preferencesAct.setStatusTip(self.tr("Configure the application"))
        self.preferencesAct.triggered.connect(self.onPreferences)
        # Action for starting a measurement.
        self.startAct = QtWidgets.QAction(self.tr("&Start"), self)
        self.startAct.setStatusTip(self.tr("Start measurement"))
        self.startAct.triggered.connect(self.onStart)
        self.startAct.setCheckable(True)
        # Action for stopping a measurement.
        self.stopAct = QtWidgets.QAction(self.tr("S&top"), self)
        self.stopAct.setStatusTip(self.tr("Stop measurement"))
        self.stopAct.triggered.connect(self.onStop)
        self.stopAct.setCheckable(True)
        self.stopAct.setChecked(True)
        self.stopAct.setEnabled(False)
        # Action group for measurement control
        self.measureActGroup = QtWidgets.QActionGroup(self)
        self.measureActGroup.addAction(self.startAct)
        self.measureActGroup.addAction(self.stopAct)
        self.measureActGroup.setExclusive(True)
        # Open contents URL.
        self.contentsAct = QtWidgets.QAction(self.tr("&Contents"), self)
        self.contentsAct.setShortcut(QtGui.QKeySequence(Qt.Key_F1))
        self.contentsAct.setStatusTip(self.tr("Visit manual on github pages"))
        self.contentsAct.triggered.connect(self.onShowContents)

    def createMenus(self):
        """Create menus."""
        # File menu
        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.fileMenu.addAction(self.quitAct)
        # Edit menu
        self.editMenu = self.menuBar().addMenu(self.tr("&Edit"))
        self.editMenu.addAction(self.preferencesAct)
        # Measurement menu
        self.measureMenu = self.menuBar().addMenu(self.tr("&Measure"))
        self.measureMenu.addActions(self.measureActGroup.actions())
        # Help menu
        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.contentsAct)

    def createToolbar(self):
        """Create main toolbar and pin to top area."""
        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.addActions(self.measureActGroup.actions())

    def createStatusBar(self):
        """Create status bar."""
        self.statusBar()

    def loadPlugins(self):
        """Load plugins specified in config/<setup>/settings.yml"""
        self.pluginTabWidget.clear()
        for plugin in self.setup.settings.get("plugins", []):
            self.pluginTabWidget.loadPlugin(plugin)

    def onPreferences(self):
        """Show preferences dialog."""
        self.preferencesDialog.show()
        self.preferencesDialog.raise_()

    def onStart(self):
        """Starting a measurement."""
        self.startAct.setEnabled(not self.startAct.isEnabled())
        self.stopAct.setEnabled(not self.stopAct.isEnabled())
        self.pluginTabWidget.onStart()

    def onStop(self):
        """Stopping current measurement."""
        self.startAct.setEnabled(not self.startAct.isEnabled())
        self.stopAct.setEnabled(not self.stopAct.isEnabled())
        self.pluginTabWidget.onStop()

    def onShowContents(self):
        """Open web browser and open contents."""
        webbrowser.open_new_tab(CONTENTS_URL)

    def closeEvent(self, event):
        """On window close event."""
        result = QtWidgets.QMessageBox.question(None,
            self.tr("Confirm quit"),
            self.tr("Are you sure to quit?"),
            QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

