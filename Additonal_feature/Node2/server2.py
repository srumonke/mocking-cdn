from flask import Flask, request, jsonify
import threading
import hashlib
import time

app = Flask(__name__)

# Shared data structures
file_locks = {}
file_queues = {}
files = {
    'file1.txt': [{'version': 1, 'content': 'This is the content of file1.txt', 'timestamp': time.time()}],
    'file2.txt': [{'version': 1, 'content': 'This is the content of file2.txt', 'timestamp': time.time()}]
}

def hash_file_content(content):
    """Generate a hash for file content."""
    return hashlib.sha256(content.encode()).hexdigest()

def detect_duplicates(file_content):
    """Detect duplicate files based on content hash."""
    file_hash = hash_file_content(file_content)
    return file_hash in [hash_file_content(version['content']) for versions in files.values() for version in versions]

def request_lock(file_name, user_id):
    """Request lock for a file."""
    if file_name not in file_locks:
        file_locks[file_name] = threading.Lock()
        file_queues[file_name] = []

    lock = file_locks[file_name]
    queue = file_queues[file_name]

    lock.acquire()
    if not queue:
        lock.release()
        return True
    else:
        queue.append(user_id)
        lock.release()
        return False

def release_lock(file_name):
    """Release lock for a file."""
    if file_name in file_queues:
        queue = file_queues[file_name]
        if queue:
            queue.pop(0)

def write_file(file_name, file_content):
    """Write file content."""
    if file_name in files:
        latest_version = files[file_name][-1]['version']
        new_version = latest_version + 1
        files[file_name].append({'version': new_version, 'content': file_content, 'timestamp': time.time()})
    else:
        files[file_name] = [{'version': 1, 'content': file_content, 'timestamp': time.time()}]

@app.route('/write', methods=['POST'])
def write_file_route():
    data = request.json
    file_name = data.get('file_name')
    file_content = data.get('file_content')
    user_id = data.get('user_id')

    if detect_duplicates(file_content):
        return jsonify({'message': 'Duplicate file detected. Not written.'}), 400

    if not request_lock(file_name, user_id):
        return jsonify({'message': 'File is locked by another user. Please wait.'}), 403

    write_file(file_name, file_content)
    release_lock(file_name)

    return jsonify({'message': 'File written successfully.'}), 200

@app.route('/read', methods=['GET'])
def read_files():
    return jsonify(files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
