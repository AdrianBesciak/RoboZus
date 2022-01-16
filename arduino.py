import serial
from time import sleep

dist_keys = ['right', 'front', 'left', 'back']


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
        data = ''
        while data == '':
            data = self.serial.read_until('\n').decode("utf-8")
        return data

    def get_distances(self):
        self.send('S')
        str = self.read()
        list = str.split('\n')[0].split(';')
        distances = {}
        for i in range(len(list)):
            if i < len(dist_keys):
                if 40 < int(list[i]) < 20000:
                    distances[dist_keys[i]] = int(list[i])
        return distances

    def get_brightness_value(self):
        self.send('B')
        return self.read()
