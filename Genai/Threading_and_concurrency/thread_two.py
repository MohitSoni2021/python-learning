import threading
import time

def prepare_tea(type_, wait_time):
    print(f"Preparing {type_} tea...")
    time.sleep(wait_time)
    print(f"{type_} tea is ready.")
    
t1 = threading.Thread(target=prepare_tea, args=("Green", 2))
t2 = threading.Thread(target=prepare_tea, args=("Black", 3))

t1.start()
t2.start()

t1.join()
t2.join()