"""app/menu.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/8/23
python version  : 3.7.3
"""

from story_board import StoryBoard


class Menu(StoryBoard):
    """Menu
    """

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.lcd = app.lcd

        self.status = None

    def top(self):
        """top
        """
        self.lcd.message(message='ﾒﾆｭｰ', line=self.lcd.LINE_1)
        self.lcd.message(message='>ﾀｼｻﾞﾝ  ﾋｷｻﾞﾝ', line=self.lcd.LINE_2)
        self.status = 'addition'

    def button1_pressed(self):
        """button1_pressed
        """
        if self.status == 'addition':
            self.lcd.message(message=' ﾀｼｻﾞﾝ >ﾋｷｻﾞﾝ', line=self.lcd.LINE_2)
            self.status = 'subtraction'
        else:
            self.lcd.message(message='>ﾀｼｻﾞﾝ  ﾋｷｻﾞﾝ', line=self.lcd.LINE_2)
            self.status = 'addition'

    def button1_released(self):
        """button1_released
        """
        print('>>> button1_released')

    def button2_pressed(self):
        """button2_pressed
        """
        if self.status == 'addition':
            self.app.status = 'addition'
        else:
            self.app.status = 'subtraction'
        self.app.display.get(self.app.status).top()

    def button2_released(self):
        """button2_released
        """
        print('>>> button2_released')
