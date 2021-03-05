from modules.downloader import Downloader
from modules.hasher import Hasher
from modules.storager import Storager
import utils
import os
import prettytable
from const import CalcType


class Scheduler:

    def __init__(self):
        self.downloader = Downloader()
        self.hasher = Hasher()
        self.storager = Storager()
        self.md5_map = {}

    def set_calc_type(self, type_):
        self.downloader.set_calc_type(type_)
        self.hasher.set_calc_type(type_)
        self.storager.set_calc_type(type_)

    def _wrap_path(self, md5):
        if md5 in self.md5_map:
            self.md5_map[md5] += 1
        else:
            self.md5_map[md5] = 1

        number = self.md5_map[md5]
        filename = f'{md5}.jpg' if number == 1 else f'{md5}_{number}.jpg'
        storage_path = os.path.join(".", "images")
        path = os.path.join(storage_path, filename)
        return path

    def process(self):
        time_statictics = {
            "network_time": [],
            "cpu_time": [],
            "disk_time": [],
        }
        timer = utils.Timer()

        url_list = utils.url_list()

        timer.tick()
        content_list = self.downloader.process(url_list)
        time_cost = timer.tock()
        time_statictics["network_time"].append(time_cost)

        timer.tick()
        md5_list = self.hasher.process(content_list)
        time_cost = timer.tock()
        time_statictics["cpu_time"].append(time_cost)

        item_list = []
        for content, md5 in zip(content_list, md5_list):
            path = self._wrap_path(md5)
            item = (content, path)
            item_list.append(item)

        timer.tick()
        self.storager.process(item_list)
        time_cost = timer.tock()
        time_statictics["disk_time"].append(time_cost)

        return time_statictics

    def create_row(self, type_, times):
        return [
            type_,
            times[0],
            times[1],
            '%.4f%%' % ((times[0] - times[1]) / times[0] * 100),
            times[2],
            '%.4f%%' % ((times[0] - times[2]) / times[0] * 100),
        ]

    def statictics(self, single_log, multi_thread_log, multi_process_log):
        # table = prettytable.PrettyTable(["类型", "单线程耗时", "多线程耗时", "多线程提升率", "多进程耗时", "多进程提升率"])
        table = prettytable.PrettyTable(
            ["type", "single thread", "multi thread", "thread perform", "multi process", "process perform"])

        network_time = (
            single_log["network_time"][0],
            multi_thread_log["network_time"][0],
            multi_process_log["network_time"][0],
        )
        network_row = self.create_row('network', network_time)

        cpu_time = (
            single_log["cpu_time"][0],
            multi_thread_log["cpu_time"][0],
            multi_process_log["cpu_time"][0],
        )
        cpu_row = self.create_row('cpu', cpu_time)

        disk_time = (
            single_log["disk_time"][0],
            multi_thread_log["disk_time"][0],
            multi_process_log["disk_time"][0],
        )
        disk_row = self.create_row('disk', disk_time)

        table.add_row(network_row)
        table.add_row(cpu_row)
        table.add_row(disk_row)

        print(table)


if __name__ == '__main__':
    scheduler = Scheduler()

    scheduler.set_calc_type(CalcType.SingleThread)
    single_thread_time = scheduler.process()

    scheduler.set_calc_type(CalcType.MultiThread)
    multi_thread_time = scheduler.process()

    scheduler.set_calc_type(CalcType.MultiProcess)
    multi_process_time = scheduler.process()

    scheduler.statictics(single_thread_time, multi_thread_time, multi_process_time)
