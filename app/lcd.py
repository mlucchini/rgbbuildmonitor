import os
import yaml
from .util import is_pi


class DesktopLcdScreen():
    def clear(self):
        pass

    def message(self, text):
        print('----------------')
        print(text)
        print('----------------')


class LcdScreen():
    def __init__(self):
        super(LcdScreen, self).__init__()
        with open('config.yml', 'r') as f:
            cfg = yaml.load(f)
            self.rs = cfg['lcd']['rs']
            self.en = cfg['lcd']['en']
            self.d4 = cfg['lcd']['d4']
            self.d5 = cfg['lcd']['d5']
            self.d6 = cfg['lcd']['d6']
            self.d7 = cfg['lcd']['d7']
        if is_pi():
            from Adafruit_CharLCD import Adafruit_CharLCD
            self.lcd = Adafruit_CharLCD(rs=self.rs, en=self.en, d4=self.d4, d5=self.d5, d6=self.d6, d7=self.d7, cols=16, lines=2)
            self.lcd.clear()
        else:
            self.lcd = DesktopLcdScreen()

    def update(self, title, text):
        self.lcd.clear()
        self.lcd.message(title + '\n' + text)

class StatusLcd():
    def __init__(self):
        self.lcd = LcdScreen()
        self.builds = {}

    def update(self, statuses):
        for status in statuses:
            self.builds[status.name] = status
        error_statuses = [status for _, status in self.builds.items() if status.status in 'error']
        if not error_statuses:
            self.lcd.update('     UNDER', '    CONTROL')
        else:
            error_status = error_statuses[0]
            self.lcd.update('    FAILURE', error_status.name.replace('ConnectionBox', 'CxBox'))
