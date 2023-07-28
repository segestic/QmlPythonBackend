#################################CHECK PLATFORM if not platform, use fake_gpio###################
import platform

if platform.machine() == 'aarch64':
    import RPi.GPIO as GPIO
    import mfrc522
    MFRC522 = mfrc522
    import signal
else:
    print("This script is designed to run on a Raspberry Pi with RPi.GPIO module and mfrc522SS module installed.")
    from .fake_gpio import MockGPIO, MFRC522
    GPIO = MockGPIO()
################################################################################################
import threading
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot
import time

class RfidBackend(QObject):
    rfidAddressChanged = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._rfid = ""
        self.MIFAREReader = MFRC522.MFRC522()
        self.running = True # for threading
        self.rfid_thread = None  # Initialize the thread variable
        self.continue_reading = True #for rfid
        self.proceed_read = False #for rfid

    @pyqtSlot()
    def start_reading(self):
        self.running = True
        self.rfid_thread = threading.Thread(target=self.read_rfid)  # Create the thread
        self.rfid_thread.start()

    @pyqtSlot()
    def stop_reading(self):
        self.cancel_read_session()
        self.running = False

    @pyqtSlot()
    def start_antenna(self):
        self.running = True
        self.rfid_thread = threading.Thread(target=self.resume_read_session)  # Create the thread
        self.rfid_thread.start()

    @pyqtProperty(str, notify=rfidAddressChanged)
    def my_rfid_address(self):
        return self._rfid


    @pyqtSlot()
    # Capture SIGINT for cleanup when the script is aborted
    def end_read(signal,frame):
        global continue_reading
        print ("Ctrl+C captured, ending read.")
        continue_reading = False
        GPIO.cleanup()


    def AntennaStatus(self):
        temp = self.MIFAREReader.Read_MFRC522(self.TxControlReg)
        if temp & 0x03:
            print ("Antenna is on")
            return 1
        else:
            print ("Antenna is off")
            return 0

    # Hook the SIGINT
    #signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    #MIFAREReader = MFRC522.MFRC522()

    # Welcome message
    print ("Welcome to the MFRC522 data read example")
    #print ("Press Ctrl-C to stop.")


    def read_id7(self):
        id = None
        while not id:
            (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
            if status != self.READER.MI_OK:
                return None
            (status, uid) = self.READER.MFRC522_Anticoll()
            if status != self.READER.MI_OK:
                return None
            n = 0
            for i in range(0, 5):
                n = n * 256 + uid[i]
            id = n
        return id


    def uid_to_num(self, uid):
      n = 0
      for i in range(0, 5):
              n = n * 256 + uid[i]
      return n


    #testing on non aarch64 platform...
    def read_rfid2(self):
        demo_result = '101022'
        while True:
            print ("infinite loop starts........")
            time.sleep(5)
            self._rfid = demo_result
            break
        self.rfidAddressChanged.emit(self._rfid)


    def read_rfid(self):
        while self.continue_reading:
            # Scan for cards
            (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status == self.MIFAREReader.MI_OK:
                print ("Card detected")

            # Get the UID of the card
            (status,uid) = self.MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == self.MIFAREReader.MI_OK:
                # Print UID
                id = self.uid_to_num(uid)
                self._rfid = str(id)
                self.rfidAddressChanged.emit(str(self._rfid))

                print('UID is ', id)

                print ('ID before conversion is ', id)

                ###ends

                # Check if authenticated #defined as MI_OK = 0
                if status == self.MIFAREReader.MI_OK:
                    print ("card detected")
                    #MIFAREReader.MFRC522_StopCrypto1()
                else:
                    print ("Authentication error")



    def cancel_read_session(self):
        #self.MIFAREReader.MFRC522_StopCrypto1() #stops  Anticoll from working
        #GPIO.cleanup()
        self.MIFAREReader.AntennaOff()
        print('cancel cancel')


    def resume_read_session(self):
        if self.AntennaStatus == 1:
            print ('Antenna is already on')
        else:
            print('switching on antenna')
            self.MIFAREReader.AntennaOn()

