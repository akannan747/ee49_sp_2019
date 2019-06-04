# `busio` - CircuitPython I2C driver for MicroPython

class I2C:

    def __init__(self, scl, sda, frequency=400000):
        self.init(scl, sda, frequency)

    def init(self, scl, sda, frequency):
        self.deinit()
        from machine import I2C as _I2C
        from machine import Pin as _Pin
        self._i2c = _I2C(id=0, scl=_Pin(scl), sda=_Pin(sda), freq=frequency)

    def deinit(self):
        try:
            del self._i2c
        except AttributeError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.deinit()

    def scan(self):
        return self._i2c.scan()

    def readfrom_into(self, address, buffer, *, start=0, end=None):
        if start is not 0 or end is not None:
            if end is None:
                end = len(buffer)
            buffer = memoryview(buffer)[start:end]
        return self._i2c.readfrom_into(address, buffer)

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        if isinstance(buffer, str):
            buffer = bytes([ord(x) for x in buffer])
        if start is not 0 or end is not None:
            if end is None:
                return self._i2c.writeto(address, memoryview(buffer)[start:], stop=stop)
            else:
                return self._i2c.writeto(address, memoryview(buffer)[start:end], stop=stop)
        return self._i2c.writeto(address, buffer, stop=stop)

    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *, out_start=0, out_end=None, in_start=0, in_end=None, stop=False):
        return self._i2c.writeto_then_readfrom(address, buffer_out, buffer_in,
                                               out_start=out_start, out_end=out_end,
                                               in_start=in_start, in_end=in_end, stop=stop)