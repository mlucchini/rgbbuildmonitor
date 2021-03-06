from app.bamboo import BambooMonitor
from app.bitrise import BitriseMonitor
from app.info import print_ip
from app.leds import StatusLeds
from app.lcd import StatusLcd
import RPi.GPIO as GPIO


if __name__ == '__main__':
    try:
        leds = StatusLeds()
        lcd = StatusLcd()
        print_ip(lcd.lcd)
        monitors = [BambooMonitor([leds.update, lcd.update]), BitriseMonitor([leds.update, lcd.update])]
        for monitor in monitors:
            monitor.start()
        for monitor in monitors:
            monitor.join()
    except KeyboardInterrupt:
        GPIO.cleanup()
