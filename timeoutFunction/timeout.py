import signal
import threading


#              __       __  .__   __.  __    __  ___   ___
#             |  |     |  | |  \ |  | |  |  |  | \  \ /  /
#             |  |     |  | |   \|  | |  |  |  |  \  V  /
#             |  |     |  | |  . `  | |  |  |  |   >   <
#             |  `----.|  | |  |\   | |  `--'  |  /  .  \
#             |_______||__| |__| \__|  \______/  /__/ \__\
#


def callback_func():
    raise ValueError()


def set_timeout_for_linux(seconds, callback=callback_func):
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(seconds)
                r = func(*args, **kwargs)
                signal.alarm(0)  # 关闭闹钟
                return r
            except RuntimeError:
                callback()

        return to_do

    return wrap


# ____    __    ____  __  .__   __.  _______   ______   ____    __    ____   _______.
# \   \  /  \  /   / |  | |  \ |  | |       \ /  __  \  \   \  /  \  /   /  /       |
#  \   \/    \/   /  |  | |   \|  | |  .--.  |  |  |  |  \   \/    \/   /  |   (----`
#   \            /   |  | |  . `  | |  |  |  |  |  |  |   \            /    \   \
#    \    /\    /    |  | |  |\   | |  '--'  |  `--'  |    \    /\    / .----)   |
#     \__/  \__/     |__| |__| \__| |_______/ \______/      \__/  \__/  |_______/

def set_timeout_for_windows(time, callback=callback_func):
    def decorator(f):
        def inner(*args, **kw):
            try:
                t = threading.Thread(target=f, args=[*args, *kw])
                t.setDaemon(True)
                t.start()
                t.join(time)

                # 判断线程是否还存活
                assert not t.isAlive()
            except Exception:
                callable()
        return inner
    return decorator
