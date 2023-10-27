import time

class benchmark_test:
    def __init__(self, func):
        self.func = func
    
    def run(self, count:int = 1):
        for i in range(count):
            start = time.perf_counter()
            self.func()
            duration = (time.perf_counter() - start) * 1000
            print(f"run: {i}: {self.func.__name__} took {duration: 0.4f} ms")