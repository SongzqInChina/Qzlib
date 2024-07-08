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


class ProcessBar:
    def __init__(self):
        self.title = None
        self.


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
