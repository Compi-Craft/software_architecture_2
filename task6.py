import hazelcast
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def run_client_with_optimistic_lock():
    client = hazelcast.HazelcastClient()
    distributed_map = client.get_map("map").blocking()
    def increment_map_with_optimistic_lock():
        for _ in range(10000):
            while True:
                old_value = distributed_map.get("key") or 0
                if distributed_map.replace_if_same("key", old_value, old_value + 1):
                    break

    increment_map_with_optimistic_lock()

    client.shutdown()

start_time = time.time()

threads = []
for i in range(3):
    t = threading.Thread(target=run_client_with_optimistic_lock)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

final_client = hazelcast.HazelcastClient()
final_map = final_client.get_map("map").blocking()
final_value = final_map.get("key")
print("Optimistic locking:", final_value)
end_time = time.time()
print(f"Time spent: {end_time - start_time:.2f} seconds")
final_client.shutdown()
