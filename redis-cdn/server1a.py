from flask import Flask, request, jsonify
import requests
import redis
import json

app = Flask(__name__)
SERVER2_URL = "http://localhost:5001"  # Change to your Server 2 URL
file_system = ["file1.txt", "file2.txt"]
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def publish_file_added_event(filename):
    event_data = {"event": "file_added", "filename": filename}
    redis_client.publish('file_notifications', json.dumps(event_data))

@app.route("/get_file", methods=["GET"])
def get_file():
    filename = request.args.get("filename")
    if filename in file_system:
        return jsonify({"status": "success", "path": f"/server1/{filename}"})
    else:
        response = requests.get(f"{SERVER2_URL}/get_file?filename={filename}")
        if response.status_code == 200:
            file_system.append(filename)
            return jsonify({"status": "success", "path": f"/server1/{filename}"})
        else:
            return jsonify({"status": "error", "message": "File not found in Server 1 or Server 2"}), 404

@app.route("/add_file", methods=["POST"])
def add_file():
    data = request.json
    filename = data["filename"]
    file_system.append(filename)
    publish_file_added_event(filename)  # Notify file addition
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
