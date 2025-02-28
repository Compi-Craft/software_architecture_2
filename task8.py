import hazelcast
import threading

def producer(client):
    queue = client.get_queue("queue").blocking()
    for i in range(1, 101):
        while queue.size() >= 10:
            continue
        queue.put(i)
        print(f"Produced: {i}")


def consumer(client, consumer_id):
    queue = client.get_queue("queue").blocking()
    while True:
        value = queue.take()
        print(f"Consumer {consumer_id} consumed: {value}")

client1 = hazelcast.HazelcastClient()
client2 = hazelcast.HazelcastClient()
client3 = hazelcast.HazelcastClient()

producer_thread = threading.Thread(target=producer, args=(client1,))
# consumer_thread1 = threading.Thread(target=consumer, args=(client2, 1))
# consumer_thread2 = threading.Thread(target=consumer, args=(client3, 2))

producer_thread.start()
# consumer_thread1.start()
# consumer_thread2.start()

producer_thread.join()
# consumer_thread1.join()
# consumer_thread2.join()

client1.shutdown()
client2.shutdown()
client3.shutdown()
