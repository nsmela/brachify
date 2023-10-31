import time

class benchmark_test:
    def __init__(self, func):
        self.func = func
    
    def run(self, count:int = 1):
        min = None
        max = None
        values = []
        for i in range(count):
            start = time.perf_counter()
            self.func()
            duration = (time.perf_counter() - start) * 1000
            if min is None or min > duration: min = duration
            if max is None or max < duration: max = duration
            values.append(duration)
            print(f"run: {i}: {self.func.__name__} took {duration: 0.4f} ms")
        for value in values:
            total += value
        avg = total / len(values)
        print(f" | min | avg | max |")
        print(f"{self.func.__name__}:   | {min} | {avg} | {max} |")
