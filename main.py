from app.bamboo import BambooMonitor
from app.bitrise import BitriseMonitor
from app.leds import StatusLeds
import RPi.GPIO as GPIO


if __name__ == '__main__':
  try:
    leds = StatusLeds()
    monitors = [BambooMonitor(leds.update), BitriseMonitor(leds.update)]
    for monitor in monitors:
      monitor.start()
    for monitor in monitors:
      monitor.join()
  except KeyboardInterrupt:
    GPIO.cleanup()
