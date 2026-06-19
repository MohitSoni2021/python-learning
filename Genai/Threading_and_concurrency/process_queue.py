from multiprocessing import Process, Queue

def prepare_coffee(queue):
    print("Preparing coffee...")
    queue.put("Coffee is ready!")
    
if __name__ == "__main__":
    queue = Queue()
    process = Process(target=prepare_coffee, args=(queue,))
    process.start()
    process.join()
    
    message = queue.get()
    print(message)