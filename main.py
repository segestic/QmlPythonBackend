## This Python file uses the following encoding: utf-8
#import sys
#from pathlib import Path

#from PySide2.QtGui import QGuiApplication
#from PySide2.QtQml import QQmlApplicationEngine


#if __name__ == "__main__":
#    app = QGuiApplication(sys.argv)
#    engine = QQmlApplicationEngine()
#    qml_file = Path(__file__).resolve().parent / "main.qml"
#    engine.load(str(qml_file))
#    if not engine.rootObjects():
#        sys.exit(-1)
#    sys.exit(app.exec_())


import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from backend import Backend
from my_ip import IPBackend


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    # Create an instance of the backend
    backend = Backend()
    ipbackend = IPBackend()

    # Create the QML engine
    engine = QQmlApplicationEngine()

    # Expose the backend instance to the QML frontend
    engine.rootContext().setContextProperty("backend", backend)
    engine.rootContext().setContextProperty("ipbackend", ipbackend)

    # Load the QML file
    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())


#pip install PyQt5
