import threading
import time

counter = 0
lock = threading.Lock()

def increment_counter():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1
            
            
threads = [threading.Thread(target=increment_counter) for _ in range(10)]
[t.start() for t in threads]
[t.join() for t in threads]

print("Final counter value:", counter)