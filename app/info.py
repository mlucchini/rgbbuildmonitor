from subprocess import check_output
import time
from .util import is_pi


def print_ip(lcd):
    out = check_output(['hostname', '-I'] if is_pi() else ['hostname']).decode('utf-8')
    lcd.update('   IP ADDRESS   ', ' ' + out)
    time.sleep(3)
