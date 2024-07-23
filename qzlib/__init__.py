import logging
import os
import sys

from . import zout, ztime


class _LogFormat(logging.Formatter):
    def format(self, record):
        message = record.getMessage()
        error_level = record.levelname
        data_time = ztime.time.asctime()
        color_head = ''
        if error_level == "ERROR":
            color_head = zout.get_color_head(255, 0, 0)
        if error_level == "WARNING":
            color_head = zout.get_color_head(255, 255, 0)
        if error_level == "INFO":
            color_head = zout.get_color_head(0, 255, 0)
        if error_level == "DEBUG":
            color_head = zout.get_color_head(0, 0, 255)
        if error_level == "CRITICAL":
            color_head = zout.get_color_head(255, 0, 255)
        if error_level == "NOTSET":
            color_head = zout.get_color_init()

        return color_head + f"Module {record.module} at '{data_time}' Logging: [{error_level}] - {message}" + zout.get_color_init()


_lib_logging_root = logging.getLogger()
Formatter = _LogFormat()
_lib_logging_root.setLevel(logging.DEBUG)

version = "0.0.1"

_lib_logging_root.debug("--Qzlib-------------------------")
_lib_logging_root.debug(f"| version:\t{version}")
_lib_logging_root.debug(f"| platform:\t{os.name}")
_lib_logging_root.debug(f"| python:\t{sys.version}")
_lib_logging_root.debug(f"--log--------------------------")


def management_logger():
    return _lib_logging_root


from . import (
    zdatabase,
    zdatabaseX,
    zencrypt,
    zfile,
    zfilex,
    zjson,
    zlibcon,
    znetwork,
    znamepipe,
    zother,
    zpath,
    zprocess,
    zprocessx,
    zreg,
    zsystem,
    zshell,
    zthread,
    typefunc,
    zwindow,
    zstruct,
    sample,
    zFileSystemMapper,
    zplugins_loader,  # TODO: This module is not finished
    zauth,
    zsimplepipe,
    zhash,
    zimport_func,
    zencryio
)

_lib_logging_root.debug("All modules are ready.")
