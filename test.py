import logging

import qzlib

liblib = qzlib

from qzlib.ztest import *


@test_function(1)
def qzlib_zout__process_bar__test():
    bar = qzlib.zout.ProcessBar(total=100, line=1)
    for i in range(100):
        sys.stdout.flush()
        bar.update(i)
        time.sleep(0.1)
    bar.finish()
    return "End"


@test_function(1)
def qzlib_zout__multi_process_bar__test():
    bar_pool = qzlib.zout.MultiProcessBar()
    cursor = qzlib.zout.get_cursor().to_local()
    print(cursor)

    bar_pool.add_processbar(qzlib.zout.ProcessBar(name="ProcessBar1", total=10000, line=1, cursor=cursor))
    bar_pool.add_processbar(qzlib.zout.ProcessBar(name="ProcessBar2", total=10000, line=1, cursor=cursor))
    bar_pool.add_processbar(qzlib.zout.ProcessBar(name="ProcessBar3", total=10000, line=1, cursor=cursor))

    for i in range(10000):
        sys.stdout.flush()
        bar_pool.records[0].update(i)
        bar_pool.records[1].update(i)
        bar_pool.records[2].update(i)
        time.sleep(0.005)
    bar_pool.finish_all()


@test_function(1)
def qzlib_zout__get_cursor__function_test():
    # 发送请求光标位置的 ANSI 转义序列
    sys.stdout.write("\033[6n")
    sys.stdout.flush()

    timeout = 3

    start_time = time.time()
    response = ""
    while time.time() - start_time < timeout:
        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8')
            if char == 'R':
                break
            response += char
        time.sleep(0.01)  # 减少CPU占用
    # 解析响应以获取光标位置
    # \x1b[27;1
    if response.startswith("\033["):
        response = response.split('\033[')[1]
        response = response.split(';')
        response = list(map(int, response))
        if len(response) == 2:
            print(f"Cursor position: {response[0]}, {response[1]}")
            return 'End'
    print(f"Cannot get cursor position(String is '{response}').")
    return 'End'


@test_function(1)
def qzlib_zshell__get_cmd_name__function_test():
    name = qzlib.zshell.command_shell()
    print(f"程序可能在{name}中运行")


if __name__ == "__main__":
    logger = qzlib.management_logger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(qzlib.Formatter)
    logger.addHandler(handler)

    functions = []
    for name, var in globals().copy().items():
        if name.startswith("qzlib") and name.endswith('test') and isinstance(var, TestFunction):
            functions.append(var)

    activate(qzlib_zout__get_cursor__function_test)
    activate(qzlib_zout__process_bar__test)
    activate(qzlib_zshell__get_cmd_name__function_test)

    test_main(functions)
    time.sleep(4)
