import argparse
import sys
import time
from datetime import datetime
from threading import Thread

from serial import Serial  # type: ignore


class DumpInterface:

    def output(self, timestamp: datetime, src: str, dest: str, data: bytes):
        raise NotImplementedError


class NoneDump(DumpInterface):

    def output(self, timestamp: datetime, src: str, dest: str, data: bytes):
        pass


class ConsoleDump(DumpInterface):

    def output(self, timestamp: datetime, src: str, dest: str, data: bytes):
        flow = '%s -> %s' % (src, dest)
        print(timestamp, flow, data)
        sys.stdout.flush()


class Transfer:

    def __init__(self, src: Serial, dest: Serial, dump: DumpInterface):
        self._src = src
        self._dest = dest
        self._alive = False
        self._th = Thread(target=self.process, daemon=True)
        self._dump = dump

    def start(self):
        self._alive = True
        self._th.start()

    def stop(self):
        self._alive = False
        self._th.join()

    def process(self):
        while self._alive:
            b = self._src.read(self._src.in_waiting or 1)
            if not b:
                continue
            buf = b
            while True:
                b = self._src.read(self._src.in_waiting or 1)
                if not b:
                    break
                buf += b
            self._dest.write(buf)
            self._dump.output(datetime.now(), self._src.name,
                              self._dest.name, buf)


def run(port1: str, port2: str, port1_baudrate: int, port2_baudrate: int, dump: bool):
    com1 = Serial(port1, port1_baudrate, timeout=.5)
    com2 = Serial(port2, port2_baudrate, timeout=.5)

    dump = ConsoleDump() if dump else NoneDump()
    t1 = Transfer(com1, com2, dump)
    t2 = Transfer(com2, com1, dump)

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
    parser.add_argument('port1', help='Path of serial port 1')
    parser.add_argument('port2', help='Path of serial port 2')
    parser.add_argument('--port1-baudrate', type=int,
                        default=115200,
                        help='Baudrate of serial port 1')
    parser.add_argument('--port2-baudrate', type=int,
                        default=115200,
                        help='Baudrate of serial port 2')
    parser.add_argument('--verbose', '-V', action='store_true',
                        help='Enable dump to console')
    args = parser.parse_args()
    run(args.port1, args.port2, args.port1_baudrate,
        args.port2_baudrate, args.verbose)


if __name__ == '__main__':
    main()
