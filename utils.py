import os
import time


class Timer:

    def __init__(self):
        self.val = 0

    def tick(self):
        self.val = time.time()

    def tock(self):
        return round(time.time() - self.val, 6)


def url_list():
    list_file = os.path.join("piclist/images.txt")
    url_list = []
    with open(list_file, 'r') as f:
        url_list = [line.strip() for line in f]
    return url_list[0:100]
