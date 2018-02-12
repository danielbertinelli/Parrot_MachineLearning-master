import serial

s = serial.Serial('COM3', baudrate=115200, timeout=None, rtscts=True, dsrdtr=True)  # open serial port


class CommunicationManager():

    def open_serial_port(self):
        s.write(bytearray([255, 7, 3]))  # starting communications with serial port

    def send_data_request(self):
        s.write(bytearray([255, 8, 7, 0, 0, 0, 0]))  # acceleration data request



    def read_data(self,):
        bytesToRead = s.inWaiting()
        inbyte = s.read(bytesToRead)
        return bytesToRead, inbyte

    def close_serial_port(self):
        s.write(bytearray([255, 9, 3]))  # stop transmitting
        s.close()
