import ctypes
import threading
import time
import traceback

def ctype_async_raise(thread_obj, exception):
    found = False
    target_tid = 0
    for tid, tobj in threading._active.items():
        if tobj is thread_obj:
            found = True
            target_tid = tid
            break

    if not found:
        raise ValueError("Invalid thread object")

    ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(target_tid),
                                                     ctypes.py_object(exception))
    # ref: http://docs.python.org/c-api/init.html#PyThreadState_SetAsyncExc
    if ret == 0:
        raise ValueError("Invalid thread ID")
    elif ret > 1:
        # Huh? Why would we notify more than one threads?
        # Because we punch a hole into C level interpreter.
        # So it is better to clean up the mess.
        ctypes.pythonapi.PyThreadState_SetAsyncExc(target_tid, NULL)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    print "Successfully set asynchronized exception for", target_tid

# def parser_func(code):
    # print "parsing"
    # try:
        # exec(code)
    # except SystemExit:
        # print "exit from loop."
    # except:
        # traceback.print_exc()
    # finally:
        # pass

class Thread:

    def __init__(self):
        self.t = None

    def start(self, func, code):
        self.t = threading.Thread(target=func, args=(code,))
        self.t.start()

    def stop(self):
        try:
            if self.t.isAlive():
                ctype_async_raise(self.t, SystemExit)
            self.t.join()
        except:
            traceback.print_exc()

