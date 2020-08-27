"""app/addition.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/8/23
python version  : 3.7.3
"""

from random import randint

from story_board import StoryBoard


class Addition(StoryBoard):
    """Addition
    """
    MAXIMUM = 5

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.lcd = app.lcd

        self.question = 0
        self.num1 = 0
        self.num2 = 0

    def top(self):
        """top
        """
        self.question = 0
        self.num1 = 0
        self.num2 = 0
        self.lcd.message(message='ﾀｼｻﾞﾝ ｹﾞｰﾑ ^o^', line=self.lcd.LINE_1)
        self.lcd.message(message='ｷﾐ ﾊ ﾜｶﾙｶﾅ?', line=self.lcd.LINE_2)

    def button1_pressed(self):
        """button1_pressed
        """
        self.question = self.question + 1

        if self.question > 10:
            self.app.status = 'menu'
            self.app.display.get(self.app.status).top()
            return

        self.num1 = randint(1, self.MAXIMUM)
        self.num2 = randint(1, self.MAXIMUM)

        self.lcd.message(message='Q{}) {} + {} = ?'.format(str(self.question).zfill(2), self.num1,
                                                           self.num2), line=self.lcd.LINE_1)
        self.lcd.message(message='ｺﾀｴ)', line=self.lcd.LINE_2)

    def button1_released(self):
        """button1_released
        """
        print('>>> button1_released')

    def button2_pressed(self):
        """button2_pressed
        """
        if self.num1 == 0 or self.num2 == 0:
            return
        self.lcd.message(message='ｺﾀｴ) {}'.format(
            self.num1+self.num2), line=self.lcd.LINE_2)

    def button2_released(self):
        """button2_released
        """
        print('>>> button2_released')
