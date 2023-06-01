from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot
import subprocess

class IPBackend(QObject):
    def __init__(self):
        super().__init__()
        self._ip = ""

    ipAddressChanged = pyqtSignal(str)

    @pyqtProperty(str, notify=ipAddressChanged)
    def my_ip_address(self):
        result = subprocess.run(["ifconfig", "enp7s0"], capture_output=True, text=True)
        # Extract the IP address from the output
        output_lines = result.stdout.split("\n")
        for line in output_lines:
            if "inet " in line:
                ip_address = line.split()[1]
                print("IP address:", ip_address)
                self._ip = ip_address
                self.ipAddressChanged.emit(self._ip)
                return ip_address

