import logging
import time
from typing import Callable

zout_logger = logging.getLogger("SzQlib.zout")


def mapping(stream, in_min, in_max, out_min, out_max, rt_function: Callable = float):
    zout_logger.debug(f"Mapping data {stream} from {in_min} {in_max} to {out_min} {out_max}")
    return rt_function(out_min + (in_max - in_min) * (stream - in_min) / (out_max - out_min))


def get_foreground(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


def get_background(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"


def get_color_head(fr_r=0, fr_g=0, fr_b=0, bk_r=0, bk_g=0, bk_b=0):
    return get_foreground(fr_r, fr_g, fr_b) + get_background(bk_r, bk_g, bk_b)


def get_color_init():
    return "\033[0m"


def print_color(
        *values, sep=' ', end='\n',
        file=None, flush=False,
        foreground=None, background=None
):
    """
    :param values:
    :param sep:
    :param end:
    :param file:
    :param flush:
    :param foreground:这个参数的实参应为一个iterable，所有值为int或其子类
    :param background:这个参数的实参应为一个iterable，所有值为int或其子类
    :return: None
    """

    foreground = tuple(map(int, foreground))
    background = tuple(map(int, background))

    if not foreground:
        foreground = (0, 0, 0)
    foreground += (0, 0, 0)
    if not background:
        background = (0, 0, 0)
    background += (0, 0, 0)

    r, g, b = foreground[:3:]
    print(get_foreground(r, g, b), end='', file=file, flush=flush)
    r, g, b = background[:3:]
    print(get_background(r, g, b), end='', file=file, flush=flush)
    print(*values, sep=sep, end=end, file=file, flush=flush)
    print(get_color_init(), end='', file=file, flush=flush)


class progressbar:
    STATUS_INIT = 0
    STATUS_RUNNING = 1
    STATUS_FINISH = 2

    def __init__(self, title, precsion: int, additional, tasks: int = 100, lenght: int = 100):
        self._title = title  # 标题
        self._precsion = precsion  # 精度
        self._additional = additional  # 附加信息
        self._create_time = time.time()  # 创建时间
        self._status = self.STATUS_INIT  # 状态
        self._finishs = 0  # 完成数
        self._tasks = tasks  # 任务数
        self._lenght = lenght  # 长度
        zout_logger.debug(f"Create New Progress Bar: {title}")

    def start(self):
        zout_logger.debug("Start Progress Bar")
        self._finishs = 0
        self._status = self.STATUS_RUNNING

    def __iter__(self):
        import decimal
        decimal.getcontext().prec = self._precsion + 2
        if self._status != self.STATUS_RUNNING:
            raise RuntimeError('The progressbar is not running.')
        for i in range(self._tasks - 1):
            self._finishs += 1
            yield (
                '\r',
                self._title,
                self._additional,
                self._finishs,
                self._precsion,
                (decimal.Decimal(self._finishs) / decimal.Decimal(self._tasks) * 100),
            )

    def format(self, __iter_data):
        title = __iter_data[1]
        additional = __iter_data[2]
        finishs = __iter_data[3]
        precsion = __iter_data[4]
        percent = __iter_data[5]

        finishs_str = '#' * mapping(finishs, 0, self._tasks, 0, self._lenght, int)
        unfinishs_str = '-' * (self._lenght - len(finishs_str))

        res = f"\r{title}{additional}: {finishs_str}{unfinishs_str} | {finishs} / {self._tasks}  {percent}%"

        return res

    def print(self, __iter_data):
        print(self.format(__iter_data), end='')

    def stop(self):
        self._status = self.STATUS_FINISH
        title = self._title
        add = self._additional
        self._finishs += 1

        finishs_str = '#' * mapping(self._finishs, 0, self._tasks, 0, self._lenght, int)
        string = f"\r{title}{add}: {finishs_str} | {self._finishs} / {self._tasks}  100.00%"
        print(string, end='')


class Cursor:
    def move(self, row, col):
        print(f"\033[{row};{col}H", end='')

    def up(self, row):
        print(f"\033[{row}A", end='')

    def down(self, row):
        print(f"\033[{row}B", end='')

    def left(self, col):
        print(f"\033[{col}D", end='')

    def right(self, col):
        print(f"\033[{col}C", end='')
