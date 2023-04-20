import multiprocessing
import os
import time


def sing(num):
    time.sleep(2)
    for i in range(num):
        print(os.getid(), ':singing', i, '...')


def dance(num):
    time.sleep(2)
    for i in range(num):
        print(os.getid(), ':dancing', i, '...')


if __name__ == '__main__':
    start = time.time()
    proc1 = multiprocessing.Process(target=sing, args=(10,))
    proc2 = multiprocessing.Process(target=dance, args=(10,))

    proc1.start()
    proc2.start()

    proc1.join()
    proc2.join()
    end = time.time()

    print('total time', end - start, os.getpid(), '主进程...END!')
