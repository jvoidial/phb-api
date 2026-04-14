import threading
import time
from kernel_worker import kernel_loop

def run_kernel():
    kernel_loop()

t = threading.Thread(target=run_kernel, daemon=True)
t.start()

print("🧠 PHB v20 KERNEL ACTIVE")
while True:
    time.sleep(999999)
