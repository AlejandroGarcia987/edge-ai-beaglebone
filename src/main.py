import platform
import time 

print("Edge AI project running on:", platform.node())

while True:
    print("Heartbeat OK")
    time.sleep(2)
