#The MockGPIO class is a fake implementation of the RPi.GPIO module that emulates the behavior of GPIO pins without actually interacting with the hardware.
#It is useful for testing and debugging GPIO-related code, and can be used in place of the real RPi.GPIO module when running tests or simulations.

from unittest.mock import MagicMock, Mock

# Create a mock class to emulate RPi.GPIO
class MockGPIO(object):
    
    BCM = 1
    OUT = 1
    IN = 0
    LOW = 0
    
    def __init__(self):
        self.pin_map = {}
    
    def setmode(self, mode):
        pass
    
    def setup(self, pin, mode):
        pass
    
    def output(self, pin, value):
        self.pin_map[pin] = value
        
    def input(self, pin):
        return self.pin_map.get(pin, 0)
    
    def cleanup(self):
        pass

# Create an instance of MockGPIO
#mock_gpio = MockGPIO()

# Test output function
#mock_gpio.output(4, 1)
#assert mock_gpio.pin_map[4] == 1

# Test input function
#mock_gpio.pin_map[5] = 1
#assert mock_gpio.input(5) == 1
#assert mock_gpio.input(6) == 0



class MFRC522:
    def __init__(self):
        self.mem = [0] * 1024
    
    def MFRC522_Reset(self):
        pass
    
    def Write_MFRC522(self, addr, val):
        self.mem[addr] = val
    
    def Read_MFRC522(self, addr):
        return self.mem[addr]
    
    def Close_MFRC522(self):
        pass
    
    def SetBitMask(self, reg, mask):
        pass
    
    def AntennaOn(self):
        pass
    
    def AntennaOff(self):
        pass
    
    def MFRC522_ToCard(self, command, send_data):
        pass
    
    def MFRC522_Anticoll(self):
        pass
    
    def CalulateCRC(self, pIndata):
        pass
    
    def MFRC522_SelectTag(self, uid):
        pass
    
    def MFRC522_Auth(self, command, block_address, key, uid):
        pass
    
    def MFRC522_StopCrypto1(self):
        pass
    
    def MFRC522_Read(self, block_address):
        pass
    
    def MFRC522_Write(self, block_address, write_data):
        pass
    
    def MFRC522_DumpClassic1K(self, key, uid):
        pass









