# Raspberry PiとPythonでLCD(16x2)ゲームを作成する

## はじめに

`Mac環境の記事ですが、Windows環境も同じ手順になります。環境依存の部分は読み替えてお試しください。`

### 目的

LCD1602A 16x2 I2Cを使用して、算数ゲームを作成します。

この記事を最後まで読むと、次のことができるようになります。

| No.  | 概要       | キーワード |
| :--- | :--------- | :--------- |
| 1    | 電子回路   |            |
| 2    | LCD制御    | SMBus      |
| 3    | ボタン制御 | gpiozero   |

### 仕様

| 画面     | ボタン1                                    | ボタン2    |
| :------- | :----------------------------------------- | :--------- |
| メニュー | 足し算、引き算の選択                       | 決定       |
| 足し算   | 次問題の表示、11問目の表示でメニューへ戻る | 答えの表示 |
| 引き算   | 次問題の表示、11問目の表示でメニューへ戻る | 答えの表示 |

### 完成イメージ

|                                                                        メニュー                                                                         |                                                                         足し算                                                                          |                                                                         引き算                                                                          |
| :-----------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------: |
| <img width="300" alt="IMG_4772.PNG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/a07fbe4f-5498-307d-4832-453d972784d2.jpeg"> | <img width="300" alt="IMG_4781.JPG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/94cc9e7a-7adf-c49f-e832-ccb3fc2634d3.jpeg"> | <img width="300" alt="IMG_4778.JPG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/4e0edf67-079f-e877-76c3-04499451e4da.jpeg"> |
| <img width="300" alt="IMG_4782.PNG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/31962c5f-d8fd-7442-4f6e-81f56d7f990e.jpeg"> | <img width="300" alt="IMG_4774.JPG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/22abced7-4ebc-e29f-dfdd-d5ba010881b2.jpeg"> | <img width="300" alt="IMG_4776.JPG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/92dc5d09-770d-ab4d-718a-67a6f58c49dd.jpeg"> |
| <img width="300" alt="IMG_4779.PNG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/a1b60a9a-5de6-5421-759b-231838d8a850.jpeg"> | <img width="300" alt="IMG_4775.JPG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/dd501854-4421-c8b2-3781-79249ff5dca8.jpeg"> | <img width="300" alt="IMG_4777.JPG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/0d40d6d7-216a-4478-062c-51a12c67f870.jpeg"> |

### 実行環境

| 環境                           | Ver.    |
| :----------------------------- | :------ |
| macOS Catalina                 | 10.15.6 |
| Raspberry Pi 4 Model B 4GB RAM | -       |
| Raspberry Pi OS (Raspbian)     | 10      |
| Python                         | 3.7.3   |
| gpiozero                       | 1.5.1   |
| RPi.GPIO                       | 0.7.0   |
| smbus2                         | 0.3.0   |

### ソースコード

実際に実装内容やソースコードを追いながら読むとより理解が深まるかと思います。是非ご活用ください。

[GitHub](https://github.com/nsuhara/raspi-lcdgame.git)

### 関連する記事

- [Raspberry PiのセットアップからPython環境のインストールまで](https://qiita.com/nsuhara/items/05a2b41d94ced1f54316)
- [Raspberry PiとPythonでリモコンカーを作成する](https://qiita.com/nsuhara/items/7970b5dfe95ea76c93d6)

## 電子回路

### LCD電子回路

<img width="700" alt="lcd.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/a4b8022a-b3f5-d093-7bbc-d58fb5321aee.png">

### ボタン電子回路

<img width="700" alt="button.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/1207c6d1-292c-96c4-bac1-71befdd536db.png">

## I2C設定

### Raspberry Pi Software Configuration Tool起動

```command.sh
~$ sudo raspi-config
```

### I2C有効化

1. `5 Interfacing Options`を選択
2. `P5 I2C`を選択

### 再起動

```command.sh
~$ sudo reboot
```

### I2C通信アドレス確認

```command.sh
~$ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

I2C通信アドレスは`0x27`となる

## ハンズオン

```command.sh
~$ git clone https://github.com/nsuhara/raspi-lcdgame.git -b master
~$ cd raspi-lcdgame

~$ python -m venv .venv
~$ source .venv/bin/activate
~$ pip install -r requirements.txt
~$ source config

~$ python app/main.py

~$ Control Key + C
```

## アプリ構成

```target.sh
/app
├─ addition.py
├─ i2clcd1602a
│      ├─ __init__.py
│      ├─ katakana.py
│      └─ pcf8574t.py
├─ main.py
├─ menu.py
├─ story_board.py
└─ subtraction.py
```

## LCD

```target.sh
/app
└─ i2clcd1602a
       ├─ __init__.py
       ├─ katakana.py
       └─ pcf8574t.py
```

### LCD制御

```pcf8574t.py
"""i2clcd1602a/pcf8574t.py
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
```

### カタカナ制御

```katakana.sh
"""i2clcd1602a/katakana.py
"""

SP_CODE = 0xfec0


def convert(message):
    """convert
    """
    converted = []
    for char in message:
        if ord(char) > SP_CODE:
            converted.append(chr(ord(char)-SP_CODE))
        else:
            converted.append(char)
    return ''.join(converted)
```

## メイン

```target.sh
/app
└─ main.py
```

### メイン制御

```main.py
"""app/main.py
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
```

## 共通

```target.sh
/app
└─ story_board.py
```

### 抽象クラス

```story_board.py
"""app/story_board.py
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
```

## メニュー

```target.sh
/app
├─ menu.py
└─ story_board.py
```

### メニュー制御

```menu.py
"""app/menu.py
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
```

## 足し算

```target.sh
/app
├─ addition.py
└─ story_board.py
```

### 足し算制御

```addition.py
"""app/addition.py
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
```

## 引き算

```target.sh
/app
├─ story_board.py
└─ subtraction.py
```

### 引き算制御

```subtraction.py
"""app/subtraction.py
"""

from random import randint

from story_board import StoryBoard


class Subtraction(StoryBoard):
    """Subtraction
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
        self.lcd.message(message='ﾋｷｻﾞﾝ ｹﾞｰﾑ ^o^', line=self.lcd.LINE_1)
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
        if self.num1 < self.num2:
            temp = self.num1
            self.num1 = self.num2
            self.num2 = temp

        self.lcd.message(message='Q{}) {} - {} = ?'.format(str(self.question).zfill(2), self.num1,
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
            self.num1-self.num2), line=self.lcd.LINE_2)

    def button2_released(self):
        """button2_released
        """
        print('>>> button2_released')
```
