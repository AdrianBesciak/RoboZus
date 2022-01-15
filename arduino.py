import serial
from time import sleep


class Arduino:
    def __init__(self, port_name):
        self.serial = serial.Serial(
            port='/dev/' + port_name,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.1
        )
        if not self.serial.isOpen():
            print("Couldn't open serial port!")
        else:
            sleep(1)

    def close_connection(self):
        self.serial.close()

    def send(self, command):
        self.serial.write(str.encode(command.__str__()))

    def read(self):
        return self.serial.read_until('\n').decode("utf-8")

    def get_distances(self):
        self.send('S')
        return self.read()

    def get_brightness_value(self):
        self.send('B')
        return self.read()
