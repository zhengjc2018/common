import os
import sys
import threading
from time import sleep
from queue import Queue, Empty
from threading import RLock, Thread
import unittest


MAX_THREAD_NUM = 2
MAX_QPS = 1000


class ActorExit(Exception):
    """
        let child-thread exit
    """
    pass


class ActorSleep(Exception):
    pass


class ThreadPoolManger():
    """
        usage :
            obj = ThreadPoolManger(4)
            obj.submit(func, *args)
            obj.submit(ActorExit)
    """

    def __init__(self, pool_size=MAX_THREAD_NUM):
        self.work_queue = Queue(100)
        self.__init_threading_pool(pool_size)
        self._qps = 0

    def __init_threading_pool(self, thread_num):
        for i in range(thread_num):
            thread = ThreadManger(self.work_queue)
            thread.start()

    def submit(self, func, *args):
        if self._qps >= MAX_QPS:
            self.work_queue.put((ActorSleep, None))
            self._qps = 0
        else:
            self.work_queue.put((func, args))


class ThreadManger(Thread):

    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self._lock = RLock()

    def run(self):
        while True:
            print(f"current threading: {threading.current_thread().name}")
            fn, args = self.work_queue.get()

            if fn is ActorSleep:
                sleep(1)
            if fn is ActorExit:
                self.work_queue.put((ActorExit, None))
                sys.exit(0)

            with self._lock:
                fn(*args)
            self.work_queue.task_done()


class TestCase(unittest.TestCase):

    def test_run(self):
        times = 3

        def inner(i):
            with open("%s.txt" % i, 'a+') as f:
                f.write("hhhh"*10)

        a = ThreadPoolManger()
        for i in range(times):
            a.submit(inner, *(i, ))
        a.submit(ActorExit)

        sleep(1)
        for i in range(times):
            self.assertTrue(os.path.exists(f"{i}.txt"))


if __name__ == '__main__':
    unittest.main()
