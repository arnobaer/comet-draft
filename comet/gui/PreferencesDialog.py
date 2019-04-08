import logging
import sys, os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from ..core.SetupLoader import SetupLoader

def setCurrentEntry(widget, text):
    """Set current combo box entry by test, provided for convenince."""
    index = widget.findText(text)
    if index >= 0:
        widget.setCurrentIndex(index)

class PreferencesDialog(QtWidgets.QDialog):
    """Preferences dialog for application settings."""

    def __init__(self, parent=None):
        super(PreferencesDialog, self).__init__(parent)
        self.setWindowTitle(self.tr("Preferences"))
        self.setMinimumSize(400, 200)
        # Setup group box
        self.setupGroupBox = QtWidgets.QGroupBox(self.tr("Setup"), self)
        self.setupComboBox = QtWidgets.QComboBox()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.setupComboBox)
        self.setupGroupBox.setLayout(layout)
        # Buttonbox
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.onAccept)
        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.setupGroupBox)
        layout.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        self.loadSetups()
        self.loadSettings()

    def loadSetups(self):
        """Load available setups."""
        setups = SetupLoader().find()
        self.setupComboBox.clear()
        self.setupComboBox.addItems(setups)

    def loadSettings(self):
        """Load settings to dialog widgets."""
        activeSetup = QtCore.QSettings().value("setup")
        setCurrentEntry(self.setupComboBox, activeSetup)

    def writeSettings(self):
        """Write settings from dialog widgets."""
        activeSetup = self.setupComboBox.currentText()
        QtCore.QSettings().setValue("setup", activeSetup)
        logging.info("active setup: %s", activeSetup)

    def onAccept(self):
        """On dialog accept (apply button was clicked)."""
        self.writeSettings()
        self.accept()
