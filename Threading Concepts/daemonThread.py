import threading
import time

def task():
    while True:
        print("Running...")
        time.sleep(1)

# Daemon means that when the new function start, daemon function stops automatically;
t = threading.Thread(target=task, daemon=True)
t.start()

print("Main ends")