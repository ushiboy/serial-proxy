import argparse
import time
from threading import Thread

from serial import Serial


def main(port1: str, port2: str, port1_baudrate: int, port2_baudrate: int):
    com1 = Serial(port1, port1_baudrate, timeout=1)
    com2 = Serial(port2, port2_baudrate, timeout=1)

    def pipe1():
        while True:
            b = com1.read(com1.in_waiting or 1)
            if b:
                com2.write(b)

    def pipe2():
        while True:
            b = com2.read(com2.in_waiting or 1)
            if b:
                com1.write(b)

    th1 = Thread(target=pipe1, daemon=True)
    th2 = Thread(target=pipe2, daemon=True)
    th1.start()
    th2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='serialproxy')
    parser.add_argument('port1', help='Serial port 1')
    parser.add_argument('port2', help='Serial port 1')
    parser.add_argument('--port1-baudrate', type=int,
                        default=115200,
                        help='baudrate port1')
    parser.add_argument('--port2-baudrate', type=int,
                        default=115200,
                        help='baudrate port2')
    args = parser.parse_args()
    main(args.port1, args.port2, args.port1_baudrate, args.port2_baudrate)
