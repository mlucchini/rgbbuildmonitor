import os


def is_pi():
    return 'arm' in os.uname()[4][:3]
