import benchmarking
import sys
sys.path.append(f"C://Users//nsmel//Documents//Programming//python//brachify")
from Application.BRep.Channel import *
import testing.data.channels as data

def test():
    benchmark = benchmarking.benchmark_test(lambda: rounded_channel(data.points()[3]))

    print("Testing Application.BBrep.Channel.rounded_channel:")
    benchmark.run(4)

if __name__ == "__main__":
    test()