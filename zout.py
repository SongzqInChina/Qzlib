import logging
from decimal import Decimal
from typing import Callable

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


class ProcessBar:
    def __init__(self, _format):
        self.title = None
        self.fill_char = '-'
        self.decimal_places = 2
        self.format = _format
        self.current = 0
        self.total = 0
        self.start_time = None
        self.last_undate_time = None
        self.speed = None
        self.eta = None


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
