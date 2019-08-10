
def checkElapsedTime(measuredFunction):
    """
        Decorator, timed function
        Work example:
        @timeChecker.checkElapsedTime
        def foo():
            print("foo")
    """
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        res = measuredFunction(*args, **kwargs)
        end = time.time()
        print('[*] elapsed time: {} second'.format(end - start))
        return res
    return wrapper
