from enum import IntEnum


class CalcType(IntEnum):
    SingleThread = 0
    MultiThread = 1
    MultiProcess = 2
    PyCoroutine = 3
