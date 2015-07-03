import spidev

# ReverseBits function from http://tightdev.net/SpiDev_Doc.pdf
def ReverseBits(byte):
    byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
    byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
    byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)
    return byte

class ssd1803a:
    spi = None

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.mode = 3
        self.spi.max_speed_hz = 1000000

        # from manual (EA DOGM204-A)
        init = [0x3a, 0x09, 0x06, 0x1e, 0x39, 0x1b, 0x6e, 0x57, 0x7f, 0x38, 0x0c, 0x01]

        for byte in init:
        	self.send_byte(byte)

    def send_byte(self, byte, write=0):
    	if write > 0:
    		cmd = 0xfa
    	else:
    		cmd = 0xf8
    	byte = ReverseBits(byte)
    	self.spi.xfer2([cmd, byte & 0xf0, (byte & 0xf) << 4])

    def cmd_clear(self):
        self.send_byte(0x01)

    def dis_print_lines(self, lines):
        self.cmd_clear()

    	for line in lines:
    		line = line[0:20]
    		self.dis_print(line)
    		if len(line) < 20:
    			self.dis_print(' ' * (20-len(line)))

    def dis_print(self, str):
    	for chr in list(str):
    		self.send_byte(ord(chr), 1)
