"""app/story_board.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/8/23
python version  : 3.7.3
"""

import abc


class StoryBoard(metaclass=abc.ABCMeta):
    """StoryBoard
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def top(self):
        pass

    @abc.abstractmethod
    def button1_pressed(self):
        pass

    @abc.abstractmethod
    def button1_released(self):
        pass

    @abc.abstractmethod
    def button2_pressed(self):
        pass

    @abc.abstractmethod
    def button2_released(self):
        pass
