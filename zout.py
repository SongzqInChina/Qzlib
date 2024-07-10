import logging
from decimal import Decimal
from queue import Queue
from typing import Callable

import simpleeval

zout_logger = logging.getLogger("SzQlib.zout")


def double(num, context=...):
    return Decimal(str(num), context=context)


def mapping(stream, in_min, in_max, out_min, out_max, rt_function: Callable = float):
    stream = double(stream)
    in_min, in_max, out_min, out_max = map(double, (in_min, in_max, out_min, out_max))
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
    :param foreground: 这个参数的实参应为一个iterable，所有值为int或其子类
    :param background: 这个参数的实参应为一个iterable，所有值为int或其子类
    :return: None
    """
    if not background:
        background = (0, 0, 0)
    if not foreground:
        foreground = (0, 0, 0)

    foreground = tuple(map(int, foreground))
    background = tuple(map(int, background))

    foreground += (0, 0, 0)

    background += (0, 0, 0)

    r, g, b = foreground[:3:]
    print(get_foreground(r, g, b), end='', file=file, flush=flush)
    r, g, b = background[:3:]
    print(get_background(r, g, b), end='', file=file, flush=flush)
    print(*values, sep=sep, end=end, file=file, flush=flush)
    print(get_color_init(), end='', file=file, flush=flush)


class Cursor:
    def __init__(self, row=1, col=1):
        self.row = row
        self.col = col

    @property
    def line(self):
        return self.row

    @property
    def column(self):
        return self.col

    def move(self, row, col):
        self.row, self.col = row, col
        print(f"\033[{row};{col}H", end='')

    def up(self, row):
        self.row += row
        print(f"\033[{row}A", end='')

    def down(self, row):
        self.row -= row
        print(f"\033[{row}B", end='')

    def left(self, col):
        self.col -= col
        print(f"\033[{col}D", end='')

    def right(self, col):
        self.col += col
        print(f"\033[{col}C", end='')

    def clear_now_line(self):
        self.col = 1
        print("\033[2K", end='')

    def print(self, *values, sep=' ', end='\n', file=None, flush=False):
        line_count = 0
        for value in values:
            str_val = str(value)
            line_count += str_val.count('\n')
            if '\r' in str_val:
                r_list = str_val.split('\r')
                value_str = list("")
                for x in r_list:
                    if not value_str:
                        value_str.extend(list(x))
                    else:
                        if len(value_str) >= len(x):
                            value_str[: len(x)] = list(x)
                        else:
                            value_str.clear()
                            value_str.extend(list(x))
                self.col = len(value_str)
        self.row += line_count
        print(*values, sep=sep, end=end, file=file, flush=flush)


class LocalCursor(Cursor):
    def __init__(self, base_class: Cursor, row, col):
        super().__init__(row, col)
        self.local_row = 0
        self.local_col = 0
        self.base = base_class

    def move(self, row, col):
        self.local_row = row
        self.local_col = col

        row = self.base.row + row
        col = self.base.col + col

        super(LocalCursor, self).move(row, col)

    def up(self, row):
        self.local_row -= row
        super(LocalCursor, self).up(row)

    def down(self, row):
        self.local_row += row
        super(LocalCursor, self).down(row)

    def left(self, col):
        self.local_col -= col
        super(LocalCursor, self).left(col)

    def right(self, col):
        self.local_col += col
        super(LocalCursor, self).right(col)

    @property
    def line(self):
        return self.local_row

    @property
    def column(self):
        return self.local_col


class Record:
    title = None
    fill_char = None
    start_time = None
    end_time = None
    current = None
    total = None
    speed = None
    eta = None
    unit = None
    bar = None
    elapsed_time = None
    line = None
    formatter = None
    running = None
    stop_because = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class _ProcessBarRequest:
    """
    内部类，用于向管理器发送操作请求


    形参 operate:
        - 请求的操作，包括 ['update', 'delete', 'done', 'stop']
        - update表示更新进度条，对应的operate_obj即为`current`，operate_for_obj应为`+`，value应是新完成的量；
        - delete表示删除进度条，不检查后三个参数（
        注：
            删除后，其余的进度条会自动补足空位，如果想“强制停止”，需要使用`stop`操作
        )
        - done 表示结束进度条，并标识为正常完成，与`stop`对立，完成后的进度条，进度条部分会被设置成标题（如果没有更改format）
        - stop 表示结束进度条，并标识为异常退出，与`done`对立，终止后的进度条，进度条部分会设置为红色“Error”（如果没有更改format）

    形参 orign_object:
        - 请求的进度条对象，应是管理器add_process_bar返回的整数id，通过这个id，管理器可以确定进度条位置并进行操作

    形参 operate_obj:
        - 指定对进度条的哪个对象进行操作

    形参 operate_for_obj:
        - 指定对进度条对象需要执行的操作，应为运算符

    形参 value:
        - 指定对进度条对象执行操作的操作值

    比如：
        对id为12345678进度条的current进行加操作，那么初始化应是这样的
        ```python
        ProcessBarRecord('update', 12345678, 'current', '+', 1)
        ```
    """

    def __init__(self, operate, orign_object, operate_obj, operate_for_obj, value):
        self.operate = operate
        self.orign_object = orign_object
        self.operate_obj = operate_obj
        self.operate_for_obj = operate_for_obj
        self.value = value

    def __str__(self):
        return f"{
        dict
            (
            operate=self.operate,
            orign_object=self.orign_object,
            operate_obj=self.operate_obj,
            operate_for_obj=self.operate_for_obj,
            value=self.value
        )
        }"


class BarFormatter:
    def __init__(self, format_run, format_stop):
        self.format_run_string = format_run
        self.format_stop_string = format_stop

    def format_run(self, record: Record):
        return self.format_run_string.format(
            title=record.title,
            bar=record.bar,
            current=record.current,
            total=record.total,
            speed=record.speed,
            unit=record.unit,
            eta=record.eta,
            elapsed_time=record.elapsed_time
        )

    def format_stop(self, record: Record):
        return self.format_stop_string.format(
            title=record.title,
            bar=record.bar,
            current=record.current,
            total=record.total,
            speed=record.speed,
            unit=record.unit,
            eta=record.eta,
            elapsed_time=record.elapsed_time
        )


class MultilineProcessBar:
    def __init__(self, cursor: Cursor):
        self.process_bars = {}
        self.cursor = cursor
        self.operates = Queue()

    def update_main(self):
        while True:
            operate = self.operates.get()  # type: _ProcessBarRequest
            if operate.operate == 'update':
                process_bar_record = self.process_bars[operate.orign_object]
                if hasattr(process_bar_record, operate.operate_obj):
                    orign_value = getattr(process_bar_record, operate.operate_obj)
                    target_value = simpleeval.simple_eval(f"{orign_value} {operate.operate_for_obj} {operate.value}")
                    setattr(process_bar_record, operate.operate_obj, target_value)
                else:
                    zout_logger.debug("Bad Request:", operate)

            if operate.operate == 'delete':
                self.process_bars.pop(operate.orign_object)

    def rewrite(self):
        local = LocalCursor(self.cursor, 0, 0)
        for record in self.process_bars.values():
            if record.running:
                local.print(record.formatter.format_run(record))

    def add_process_bar(self, line: int):
        process_bar_record = Record(line=line)
        id_bar = id(process_bar_record)

        self.process_bars[id_bar] = process_bar_record

        return id_bar
