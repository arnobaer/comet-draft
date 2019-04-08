import sys, os

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .core.SetupLoader import SetupLoader
from .gui.MainWindow import MainWindow
from .gui.PreferencesDialog import PreferencesDialog

def main():

    application = QtWidgets.QApplication(sys.argv)

    # Create application settings
    application.setOrganizationName("HEPHY")
    application.setOrganizationDomain("hephy.at")
    application.setApplicationName("comet")

    # Initialize application settings
    QtCore.QSettings()

    # Raise preferences dialog on missing settings
    if not QtCore.QSettings().value("setup"):
        dialog = PreferencesDialog()
        dialog.exec_()
        del dialog

    # Load setup files
    setup = SetupLoader().load(QtCore.QSettings().value("setup"))

    # Create main window
    window = MainWindow(setup)
    window.show()
    window.raise_()

    # Load assigned plugins
    window.loadPlugins()

    application.exec_()


if __name__ == "__main__":
    main()
