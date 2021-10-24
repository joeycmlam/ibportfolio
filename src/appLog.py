import logging
from threading import Lock, Thread

class appLog(type):

    _instance = {}

    _lock: Lock = Lock()


def __call__(cls, *args, **kwargs):

    with cls._lock:

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
    return cls._instances[cls]



class appLog(metaclass=appLog):
    value: str = None

    def __init__(self, value: str) -> None:
        self.value = value

    def log(self, value):
        print (self.value)


if __name__ == "__main__":
        print('test')


