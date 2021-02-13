serial-proxy
=====

The serial-proxy is a command line tool that proxies serial ports to each other.

## Usage

```
serialproxy -h
usage: serialproxy [-h] [--port1-baudrate PORT1_BAUDRATE]
                   [--port2-baudrate PORT2_BAUDRATE] [--verbose]
                   port1 port2

positional arguments:
  port1                 Path of serial port 1
  port2                 Path of serial port 2

optional arguments:
  -h, --help            show this help message and exit
  --port1-baudrate PORT1_BAUDRATE
                        Baudrate of serial port 1
  --port2-baudrate PORT2_BAUDRATE
                        Baudrate of serial port 2
  --verbose, -V         Enable dump to console
```

To stop it, use `Ctrl + C`.

A example is as follows.

```
$ serialproxy /dev/ttyUSB0 /dev/ttyUSB1
```

## Change Log

### 0.2.0

Added verbose option.

### 0.1.0

Initial release.

## License

MIT
