from input import map_to_steering
from output import send_control
from data_types import WheelRotation
import serial

ser = serial.Serial('/dev/ttyACM0')
ser.flushInput()

if __name__ == '__main__':
    while True:
        try:
            ser_bytes = ser.readline()
            ser_string = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
            (left, right) = ser_string.split(",")
            wheel_rotation = WheelRotation(float(left), float(right))
            steering = map_to_steering(wheel_rotation)
            print(steering)
            #send_control(steering)
        except:
            print("Keyboard Interrupt")
            break