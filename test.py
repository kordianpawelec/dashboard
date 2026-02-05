import requests
import threading

url = "http://173.212.226.46:8000/upcoming"


def req():
    for _ in range(100):
        try:
            res = requests.get(url="http://173.212.226.46:8000/upcoming", timeout=3)
            print(res.raise_for_status(), res.text)
        except Exception as e:
            print(e)


threads = []


for _ in range(20):
    thread = threading.Thread(target=req)
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()
