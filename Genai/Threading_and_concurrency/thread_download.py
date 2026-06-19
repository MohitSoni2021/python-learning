import threading
import time 
import requests

def download_file(url, filename):
    print("Downloading the file from:", url)
    response = requests.get(url)
    print("Download size:", len(response.content), "bytes")
    
urls = [
    "https://httpbin.org/image/jpeg",
    "https://httpbin.org/image/png",
    "https://httpbin.org/image/svg", 
]


start = time.time()
threads = []

for url in urls:
    t = threading.Thread(target=download_file, args=(url, "file.jpg"))
    t.start()
    threads.append(t)
    
for thread in threads:
    thread.join() 
    
end = time.time()
print(f"Total time taken: {end - start:.2f} seconds")