import sys
from queue import Queue
import asyncio

q = Queue(10)


class Actor(Exception):
    pass


class AsyncIoQueue:

    def __init__(self, queue, do_action=None):
        coro = self.consume_task()
        self._loop = asyncio.get_event_loop()
        self._task = self._loop.create_task(coro)

        self._queue = queue
        self._action = do_action

    @staticmethod
    def do_action(*args, **kw):
        """
            function to deal with the data from queue
        """
        print(*args)

    async def consume_task(self):
        while True:
            f = self._queue.get(1)
            if isinstance(f, Actor):
                sys.exit(0)

            if self._action:
                self._action(f)
            else:
                AsyncIoQueue.do_action(f)

    def done(self):
        self._queue.put(Actor())
        self._loop.run_until_complete(self._task)
        self._loop.close()


class TestFunc:
    @classmethod
    def print_(cls, i):
        print(i, 2, 3)


def test():
    a = AsyncIoQueue(q, TestFunc.print_)
    for i in range(3):
        q.put(i)
    a.done()


if __name__ == '__main__':
    test()
