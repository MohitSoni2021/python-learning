import threading
import time

def worker():
    print("Worker thread is starting.")
    total = 0
    for i in range(10**8 ):
        total += i
    print("Worker thread is done. Total:", total)

start = time.time()
threads = [threading.Thread(target=worker) for _ in range(2)]
[t.start() for t in threads]
[t.join() for t in threads]
end = time.time()
print(f"Total time taken: {end - start:.2f} seconds")