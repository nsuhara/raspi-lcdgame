"""i2clcd1602a/pcf8574t.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/8/23
python version  : 3.7.3
"""
import time

from smbus2 import SMBus

from i2clcd1602a.katakana import convert


class LCD():
    """LCD
    """
    SMBUS_REV1 = 0
    SMBUS_REV2 = 1

    I2C_ADDR = 0x27

    ENABLE_BIT = 0b00000100

    LINE_1 = 0x80
    LINE_2 = 0xC0
    LINE_SIZE = 16

    MODE_COMMAND = 0
    MODE_CHAR = 1
    MODE_OPTION_BACKLIGHT = 0x08

    CMD_INITIALISE = 0x33
    CMD_SET_4_BIT_MODE = 0x32
    CMD_CURSOR_MOVE_DIRECTION = 0x06
    CMD_TURN_CURSOR_OFF = 0x0C
    CMD_2_LINE_DISPLAY = 0x28
    CMD_CLEAR_DISPLAY = 0x01
    CMD_WAIT = 0.0005

    def __init__(self):
        self.smbus = SMBus(self.SMBUS_REV2)

        self._send(mode=self.MODE_COMMAND, bits=self.CMD_INITIALISE)
        self._send(mode=self.MODE_COMMAND, bits=self.CMD_SET_4_BIT_MODE)
        self._send(mode=self.MODE_COMMAND, bits=self.CMD_CURSOR_MOVE_DIRECTION)
        self._send(mode=self.MODE_COMMAND, bits=self.CMD_TURN_CURSOR_OFF)
        self._send(mode=self.MODE_COMMAND, bits=self.CMD_2_LINE_DISPLAY)
        self._send(mode=self.MODE_COMMAND, bits=self.CMD_CLEAR_DISPLAY)

    def destroy(self):
        """destroy
        """
        self._send(mode=self.MODE_COMMAND, bits=self.CMD_CLEAR_DISPLAY)
        self.smbus.close()

    def message(self, message, line):
        """message
        """
        message = convert(message=message)
        message = message[0:self.LINE_SIZE]
        message = message.ljust(self.LINE_SIZE, ' ')

        self._send(mode=self.MODE_COMMAND | self.MODE_OPTION_BACKLIGHT,
                   bits=line)

        for char in message:
            self._send(mode=self.MODE_CHAR | self.MODE_OPTION_BACKLIGHT,
                       bits=ord(char))

    def clear(self):
        """close
        """
        self._send(mode=self.MODE_COMMAND | self.MODE_OPTION_BACKLIGHT,
                   bits=self.CMD_CLEAR_DISPLAY)

    def off(self):
        """off
        """
        self.destroy()

    def _send(self, mode, bits):
        """_send
        """
        higher_bits = mode | (bits & 0xF0)
        self._write(bits=higher_bits)

        lower_bit = mode | ((bits << 4) & 0xF0)
        self._write(bits=lower_bit)

    def _write(self, bits):
        """_write
        """
        self.smbus.write_byte(self.I2C_ADDR, bits)
        time.sleep(self.CMD_WAIT)

        self.smbus.write_byte(self.I2C_ADDR, (bits | self.ENABLE_BIT))
        time.sleep(self.CMD_WAIT)

        self.smbus.write_byte(self.I2C_ADDR, (bits & ~self.ENABLE_BIT))
        time.sleep(self.CMD_WAIT)

    def loop(self):
        """loop
        """
        while True:
            self.message(message='1234567890123456', line=self.LINE_1)
            self.message(message='abcdefghijklmnop', line=self.LINE_2)
            time.sleep(2)

            self.message(message='ABCDEFGHIJKLMNOP', line=self.LINE_1)
            self.message(message='ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀ', line=self.LINE_2)
            time.sleep(2)


if __name__ == '__main__':
    lcd = LCD()
    try:
        print('start')
        lcd.loop()
    except KeyboardInterrupt:
        lcd.destroy()
        print('stop')
