import threading
import time
from multiprocessing import Process

def worker():
    print("Worker thread is starting.")
    total = 0
    for i in range(10**8 ):
        total += i
    print("Worker thread is done. Total:", total)

if __name__ == "__main__":
    start = time.time()
    processes = [Process(target=worker) for _ in range(2)]
    [p.start() for p in processes]
    [p.join() for p in processes]
    end = time.time()
    print(f"Total time taken: {end - start:.2f} seconds")