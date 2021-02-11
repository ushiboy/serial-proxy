import argparse
import time
from threading import Thread

from serial import Serial  # type: ignore


class Transfer:

    def __init__(self, src: Serial, dest: Serial):
        self._src = src
        self._dest = dest
        self._alive = False
        self._th = Thread(target=self.process, daemon=True)

    def start(self):
        self._alive = True
        self._th.start()

    def stop(self):
        self._alive = False
        self._th.join()

    def process(self):
        while self._alive:
            b = self._src.read(self._src.in_waiting or 1)
            if b:
                self._dest.write(b)


def run(port1: str, port2: str, port1_baudrate: int, port2_baudrate: int):
    com1 = Serial(port1, port1_baudrate, timeout=.5)
    com2 = Serial(port2, port2_baudrate, timeout=.5)

    t1 = Transfer(com1, com2)
    t2 = Transfer(com2, com1)

    t1.start()
    t2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        t1.stop()
        t2.stop()
        com1.close()
        com2.close()


def main():
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
    run(args.port1, args.port2, args.port1_baudrate, args.port2_baudrate)


if __name__ == '__main__':
    main()
