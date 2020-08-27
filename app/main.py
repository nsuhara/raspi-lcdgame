"""app/main.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/8/23
python version  : 3.7.3
"""

from signal import pause
from time import sleep

from gpiozero import Button

from addition import Addition
from i2clcd1602a.pcf8574t import LCD
from menu import Menu
from subtraction import Subtraction


class Raspi():
    """Raspi
    """
    GPIO_BCM_BUTTON1 = 15
    GPIO_BCM_BUTTON2 = 25

    def __init__(self):
        self.lcd = LCD()

        self.button1 = Button(self.GPIO_BCM_BUTTON1)
        self.button1.when_pressed = self.button1_pressed
        self.button1.when_released = self.button1_released

        self.button2 = Button(self.GPIO_BCM_BUTTON2)
        self.button2.when_pressed = self.button2_pressed
        self.button2.when_released = self.button2_released

        self.status = 'menu'

        self.display = {
            'menu': Menu(self),
            'addition': Addition(self),
            'subtraction': Subtraction(self)
        }

        self.display.get(self.status).top()

    def destroy(self):
        """destroy
        """
        self.lcd.off()

    def button1_pressed(self):
        """button1_pressed
        """
        self.display.get(self.status).button1_pressed()

    def button1_released(self):
        """button1_released
        """
        self.display.get(self.status).button1_released()

    def button2_pressed(self):
        """button2_pressed
        """
        self.display.get(self.status).button2_pressed()

    def button2_released(self):
        """button2_released
        """
        self.display.get(self.status).button2_released()

    def pause(self):
        """pause
        """
        pause()


if __name__ == '__main__':
    app = Raspi()
    try:
        print('start')
        app.pause()
    except KeyboardInterrupt:
        app.lcd.clear()
        app.lcd.message(message='Good by...', line=app.lcd.LINE_1)
        sleep(1)
        app.destroy()
        print('stop')
