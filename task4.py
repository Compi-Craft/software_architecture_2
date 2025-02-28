import hazelcast
import threading
import logging

logging.basicConfig(level=logging.DEBUG)

def run_client():
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
    )
    distributed_map = client.get_map("map").blocking()
    def increment_map():
        for _ in range(10000):
            value = distributed_map.get("counter") or 0
            distributed_map.put("counter", value + 1)

    increment_map()
    client.shutdown()

threads = []
for i in range(3):
    t = threading.Thread(target=run_client)
    t.start()
    threads.append(t)
for t in threads:
    t.join()
final_client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
)
final_map = final_client.get_map("map").blocking()
print("Final value of 'counter':", final_map.get("counter"))

final_client.shutdown()
