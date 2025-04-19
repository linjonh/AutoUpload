from logging import log
import time
import traceback


def timeCost(func):
    def wrapper(*args, **argss):
        try:
            start = time.time()
            result = func(*args, **argss)
            end = time.time()
            duration = end - start
            print(f"{func.__name__} cost:{duration:.3f}s")
        except Exception as e:
            traceback.print_exc()
            print(e)
            if hasattr(argss, "callback"):
                if argss["callback"] != None:
                    argss["callback"]("opso !")
            return "opso !"
        return result

    return wrapper