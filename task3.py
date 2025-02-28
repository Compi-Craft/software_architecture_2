import hazelcast
import logging

logging.basicConfig(level=logging.DEBUG)
client = hazelcast.HazelcastClient()

distributed_map = client.get_map("map").blocking()

for i in range(1000):
    distributed_map.put(str(i), f"Value_{i}")
client.shutdown()