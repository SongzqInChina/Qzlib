# 操作Windows的os.pipe()返回的管道

import os
import queue

from . import json, network, qstruct, thread


class _PIPEWriter:
    """
    因为pipe是单向的，所以我们需要创建两个类
    """
    def __init__(self, writer: int, buffer_size: int = 1024):
        self._pipe = writer
        self._io = os.fdopen(self._pipe, 'w', buffer_size)

        self._msg_queue = queue.Queue(buffer_size)
        self._event = thread.threading.Event()

        self._write_thread = thread.start_demon_thread(self._write_thread_func)

        self.buffersize = buffer_size

    def set(self, pipe: int):
        self._event.set()
        self._io.close()
        self._pipe = pipe
        self._io = os.fdopen(self._pipe, 'w', self.buffersize)
        self._event.clear()

    def write(self, data):
        data_text = qstruct.simple_jsonpickle_pack(data)
        self._msg_queue.put(data_text)


