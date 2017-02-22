import time
import os.path


def file_magic(file_name):
    os.remove(file_name)
    print(os.path.isfile(file_name))
    for i in range(50):
        out = open(file_name, 'a')
        read = open(file_name, 'r')
        print(i, file=out, end=' ', flush=True)
        print('%s: ' % ('File context:'), read.read())
        time.sleep(2)
        out.close()
        read.close()

file_name = 'file'
file_magic(file_name)


