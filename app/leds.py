import threading
import time
import RPi.GPIO as GPIO
import yaml
from app.status import Status


class RgbLed(threading.Thread):
    rgb_off = [GPIO.LOW, GPIO.LOW, GPIO.LOW]

    def __init__(self, red_pin, green_pin, blue_pin):
        super(RgbLed, self).__init__()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)
        self.daemon = True
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.rgb = RgbLed.rgb_off
        self.blinking = False

    def __color_output(self, rgb):
      GPIO.output(self.red_pin, rgb[0])
      GPIO.output(self.green_pin, rgb[1])
      GPIO.output(self.blue_pin, rgb[2])

    def __pause(self):
      time.sleep(1)

    def run(self):
      while(True):
        self.__color_output(self.rgb)
        self.__pause()
        if self.blinking:
          self.__color_output(RgbLed.rgb_off)
          self.__pause()

    def color(self, rgb):
      self.rgb = rgb

    def blink(self, blinking):
      self.blinking = blinking


class StatusLed():
    red = [1, 0, 0]
    green = [0, 1, 0]
    yellow = [1, 1, 0]

    def __init__(self, pins):
        super(StatusLed, self).__init__()
        self.daemon = True
        self.rgb_led = RgbLed(pins[0], pins[1], pins[2])
        self.rgb_led.start()
    
    def update(self, status):
        self.rgb_led.color(StatusLed.green if 'success' in status.status else StatusLed.red if 'error' in status.status else StatusLed.yellow)
        self.rgb_led.blink(status.in_progress)


class StatusLeds():
    def __init__(self):
        self.leds = {}
        with open("config.yml", 'r') as f:
            cfg = yaml.load(f)
            for name, pins in cfg['leds'].items():
                self.leds[name] = StatusLed(pins)
                print('Started LED(%s) for %s' % (pins, name))

    def update(self, statuses):
        for status in statuses:
            if status.name in self.leds.keys():
                self.leds[status.name].update(status)
                print(status)
