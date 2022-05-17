import asyncio
import serial_asyncio
import serial
import serial.tools.list_ports
from data_types import WheelRotation
from input import map_to_steering
from output import KeyboardOutput
from turtle_output import TurtleOutput


TURTLE = False


async def main():
    output = TurtleOutput() if TURTLE else KeyboardOutput()
    reader, _ = await serial_asyncio.open_serial_connection(url=get_arduino_port(), baudrate=57600)
    while True:
        try:
            ser_bytes = await reader.readline()
            ser_string = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")
            (left, right) = ser_string.split(",")
            wheel_rotation = WheelRotation(int(left), int(right))
            steering = map_to_steering(wheel_rotation)
            output.send_control(steering)
        except:
            print("Keyboard Interrupt")
            break


def get_arduino_port():
    comports = serial.tools.list_ports.comports()
    arduino_ports = [p.device for p in comports if p.manufacturer and 'Arduino' in p.manufacturer]
    if not arduino_ports:
        raise IOError("No Arduino found")
    return arduino_ports[0]


if __name__ == '__main__':
    asyncio.run(main())
