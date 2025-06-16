# sounds.py – Clase VS1053 adaptada para ESP32 y MicroPython
from machine import Pin, SPI
import time

class VS1053:
    def __init__(self, spi, rst, dreq, xdcs, xcs, sdcs, mountpoint="/fc"):
        self.rst = rst
        self.dreq = dreq
        self.xdcs = xdcs
        self.xcs = xcs
        self.sdcs = sdcs
        self.mountpoint = mountpoint
        self.spi = spi

        # Inicializar pines
        for p in (rst, xdcs, xcs, sdcs):
            p.init(Pin.OUT, value=1)
        dreq.init(Pin.IN)

        self.reset()

    def reset(self):
        self.sdcs.value(1)
        self.xdcs.value(1)
        self.xcs.value(1)
        self.rst.value(0)
        time.sleep_ms(100)
        self.rst.value(1)
        while not self.dreq.value():
            pass
        self.sci_write(0x00, 0x0804)  # MODE: set SM_SDINEW

    def spi_write(self, cs, data):
        cs.value(0)
        self.spi.write(data)
        cs.value(1)

    def sci_write(self, addr, value):
        while not self.dreq.value():
            pass
        buf = bytearray([0x02, addr, value >> 8, value & 0xFF])
        self.spi_write(self.xcs, buf)

    def sci_read(self, addr):
        while not self.dreq.value():
            pass
        buf = bytearray([0x03, addr, 0, 0])
        res = bytearray(4)
        self.xcs.value(0)
        self.spi.write_readinto(buf, res)
        self.xcs.value(1)
        return (res[2] << 8) | res[3]

    def data_write(self, buf):
        idx = 0
        length = len(buf)
        while idx < length:
            if self.dreq.value():
                n = min(32, length - idx)
                self.spi_write(self.xdcs, buf[idx:idx + n])
                idx += n

    def set_volume(self, left, right):
        # 0 (max) to 254 (min volume)
        left = min(max(left, 0), 254)
        right = min(max(right, 0), 254)
        self.sci_write(0x0B, (left << 8) | right)

    def play_file(self, f):
        print("Reproduciendo archivo...")
        try:
            while True:
                buf = f.read(512)
                if not buf:
                    break
                self.data_write(buf)
        except Exception as e:
            print("Error durante reproducción:", e)
        print("Reproducción finalizada.")
