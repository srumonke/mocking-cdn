import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def file_notification_callback(message):
    data = json.loads(message['data'])
    if data["event"] == "file_added":
        print(f"New file added: {data['filename']}")

if __name__ == "__main__":
    pubsub = redis_client.pubsub()
    pubsub.subscribe('file_notifications')
    print("Listening for file notifications...")
    for message in pubsub.listen():
        if message['type'] == 'message':
            file_notification_callback(message)
