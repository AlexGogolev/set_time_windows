from multiprocessing import Process
import os
import time
from datetime import datetime


def sleeper():
    time.sleep(10)
    print(f'Process {os.getpid()} has been finished!')


if __name__ == '__main__':
    st = datetime.now()
    p = Process(target=sleeper)
    p.start()
    print(f'p.pid: {p.pid}')

    print(f'Main process ({os.getpid()}) has been finished: {datetime.now() - st}')

