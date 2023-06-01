from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot

class Backend(QObject):
    def __init__(self):
        super().__init__()
        self._backend_variable = 10

    # Define a signal to emit when the backend variable changes
    backendVariableChanged = pyqtSignal(int)

    #frontend-getter - qml property getter from backend
    # Define a property to expose the backend variable to QML
    @pyqtProperty(int, notify=backendVariableChanged)
    def backendVariable(self):
        return self._backend_variable


    # Define a slot to receive the frontend variable and update the backend variable
    #setter
    @pyqtSlot(int)
    def setBackendVariable(self, value):
        self._backend_variable = value
        self.backendVariableChanged.emit(self._backend_variable)


    #getter
    # Define a function that can be called from the QML frontend
    @pyqtSlot(result=int)
    def backendFunction(self):
        self._backend_variable += 5
        self.backendVariableChanged.emit(self._backend_variable)
        return self._backend_variable





#########################################################
#from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot


#class Backend(QObject):
#    def __init__(self):
#        super().__init__()
#        self._backendVariable = ""

#    # Define a signal to emit when the backend variable changes
#    backendVariableChanged = pyqtSignal(str)

#    # Define a property to expose the backend variable to QML
#    @pyqtProperty(str, notify=backendVariableChanged)
#    def backendVariable(self):
#        return self._backendVariable

#    # Define a slot to receive the frontend variable and update the backend variable
#    @pyqtSlot(str)
#    def setBackendVariable(self, value):
#        self._backendVariable = value
#        self.backendVariableChanged.emit(self._backendVariable)

#    # Define a function that can be called from the QML frontend
#    @pyqtSlot(result=str)
#    def backendFunction(self):
#        return self._backendVariable

