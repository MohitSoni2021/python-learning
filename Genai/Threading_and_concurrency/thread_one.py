import threading
import time

def boil_milk():
    print("Boiling milk...")
    time.sleep(2)
    print("Milk is boiled.")
    
def make_coffee():
    print("Making coffee...")
    time.sleep(3)
    print("Coffee is ready.")
    
start = time.time()
t1 = threading.Thread(target=boil_milk)
t2 = threading.Thread(target=make_coffee)

t1.start()
t2.start()
t1.join()
t2.join()

end = time.time()

print(f"Total time taken: {end - start:.2f} seconds") 