import threading
import time


class SimpleThreadPool:

    def process(self):
        while True:
            if len(self.queue) == 0:
                time.sleep(1)
                continue
            task = self.queue.pop()
            task()

    def __init__(self, size):
        self.pool = []
        self.queue = []
        for i in range(size):
            self.pool.append(threading.Thread(target=self.process))

    def submit(self, task):
        self.queue.append(task)

    def start(self):
        for thread in self.pool:
            thread.start()


def _task_creator(name):
    def task():
        for process in range(1, 101, 10):
            print(f'{name} running. process = {process}%. threadId = {threading.get_native_id()}')
            time.sleep(1)

    return task


if __name__ == '__main__':
    pool = SimpleThreadPool(10)
    pool.start()
    for i in range(100):
        pool.submit(_task_creator(f'task_{i}'))
