from flask import Flask, request, jsonify
import threading
import hashlib
import time

app = Flask(__name__)

# Shared data structures
file_lock = threading.Lock()
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


@app.route('/write', methods=['POST'])
def write_file():
    data = request.json
    file_name = data.get('file_name')
    file_content = data.get('file_content')

    # Check for duplicate files
    if detect_duplicates(file_content):
        return jsonify({'message': 'Duplicate file detected. Not written.'}), 400

    # Apply distributed mutual exclusion
    with file_lock:
        if file_name in files:
            latest_version = files[file_name][-1]['version']
            new_version = latest_version + 1
            files[file_name].append({'version': new_version, 'content': file_content, 'timestamp': time.time()})
        else:
            files[file_name] = [{'version': 1, 'content': file_content, 'timestamp': time.time()}]

    return jsonify({'message': 'File written successfully.'}), 200


@app.route('/read', methods=['GET'])
def read_files():
    return jsonify(files)


@app.route('/read_version', methods=['GET'])
def read_file_version():
    file_name = request.args.get('file_name')
    version = int(request.args.get('version'))

    if file_name in files:
        for file_version in files[file_name]:
            if file_version['version'] == version:
                return jsonify(file_version)

    return jsonify({'message': 'File version not found.'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
