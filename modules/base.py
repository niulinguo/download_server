from const import CalcType
from modules.executors import thread_pool_executor as tp, process_pool_executor as pp


class BaseModule:
    def __init__(self):
        self.calc_type = CalcType.SingleThread

    def set_calc_type(self, type_):
        self.calc_type = type_

    def _process(self, item):
        raise NotImplementedError()

    def _process_single_thread(self, list_):
        result_list = []
        for item in list_:
            result = self._process(item)
            result_list.append(result)
        return result_list

    def _process_executor(self, executor, list_):
        result_list = []
        task_list = []
        for item in list_:
            task = executor.submit(self._process, item)
            task_list.append(task)
        for task in task_list:
            result = task.result()
            result_list.append(result)
        return result_list

    def _process_multi_thread(self, list_):
        return self._process_executor(tp, list_)

    def _process_multi_process(self, list_):
        return self._process_executor(pp, list_)

    def process(self, list_):
        process_method_map = {
            CalcType.SingleThread: self._process_single_thread,
            CalcType.MultiThread: self._process_multi_thread,
            CalcType.MultiProcess: self._process_multi_process,
        }
        process_method = process_method_map.get(self.calc_type, self._process_single_thread)
        return process_method(list_)
