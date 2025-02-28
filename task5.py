import hazelcast
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def run_client_with_lock():
    client = hazelcast.HazelcastClient()
    distributed_map = client.get_map("map").blocking()
    def increment_map_with_lock():
        for _ in range(10000):
            distributed_map.lock("key")
            try:
                value = distributed_map.get("key") or 0
                distributed_map.put("key", value + 1)
            finally:
                distributed_map.unlock("key")

    increment_map_with_lock()

    client.shutdown()
start_time = time.time()
threads = []
for i in range(3):
    t = threading.Thread(target=run_client_with_lock)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

final_client = hazelcast.HazelcastClient()
final_map = final_client.get_map("map").blocking()
print("Pessimistic locking:", final_map.get("key"))
time_taken = time.time() - start_time
print(f"Time spent: {time_taken:.2f} seconds")
final_client.shutdown()
