import os

from win32com import client


def wmi():
    return client.GetObject("winmgmts:")


def wmi_process():
    return wmi().InstancesOf("win32_process")


def wmi_service():
    return wmi().InstancesOf("win32_service")


def wmi_disk():
    return wmi().InstancesOf("win32_logicaldisk")


def wmi_network():
    return wmi().InstancesOf("win32_networkadapterconfiguration")


def wmi_bios():
    return wmi().InstancesOf("win32_bios")


def wmi_cpu():
    return wmi().InstancesOf("win32_processor")


def wmi_os():
    return wmi().InstancesOf("win32_operatingsystem")


def wmi_user():
    return wmi().InstancesOf("win32_useraccount")


def wmi_group():
    return wmi().InstancesOf("win32_group")


def wmi_group_user():
    return wmi().InstancesOf("win32_groupuser")


def wmi_share():
    return wmi().InstancesOf("win32_share")


def shutdown(mode: str, _time: int = 1):
    if _time < 1:
        _time = 1
    return os.system(f'shutdown -{mode} -t {_time}')
