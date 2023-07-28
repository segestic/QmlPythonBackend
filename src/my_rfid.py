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
        self.continue_reading = True #for rfid - not used again
        self.pause_read = False #for rfid - by default reading is not paused

    @pyqtSlot()
    def start_reading(self):
        self.running = True
        self.rfid_thread = threading.Thread(target=self.resume_read_session)  # Create the thread
        self.rfid_thread.start()

    @pyqtSlot()
    def stop_reading(self):
        self.pause_read_session()
        self.running = False

    #function not needed... depreceated
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


    #custom function that should be in library, but created it
    def antennaStatus(self):
        temp = self.MIFAREReader.Read_MFRC522(0x14) #TxControlReg = 0x14
        print ('Antenna status is ', temp)
        notSwitchedOn = (~(temp & 0x03)) #if not same state ( i.e ~NOT 0x03 and 0x03)
        if notSwitchedOn == -1: #on is -4, off is -1
            print ("Antenna is off and state is ", notSwitchedOn)
            return 0
        else:
            print ("Antenna is on")
            return 1


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

    #only two functions will be used - pause_read_session and resume_read_session which act as a wrapper for below function read_rfid
    def read_rfid(self):
        #antenna on will be used to start rfid and antenna off will be used to pause
        #while self.continue_reading: - i don't need a while loop again
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
                #stop reading
                self.pause_read = False #card has been scanned so current reading is not paused
            else:
                print ("Authentication error")


    #switches off antenna alone....
    def pause_read_session(self):
        self.pause_read = True
        self.MIFAREReader.AntennaOff()
        print('cancel cancel')


    def resume_read_session(self):
        if self.pause_read == True:
            print('Switching on antenna alone. A read session is on')
            self.MIFAREReader.AntennaOn()
        else:
            print ('switchin on antenna and creating a read session')
            self.MIFAREReader.AntennaOn() and self.read_rfid()



#if self.antennaStatus() == 1:
#print ('Antenna is already on')
