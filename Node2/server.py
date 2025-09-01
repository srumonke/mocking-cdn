from flask import Flask, request, jsonify
import threading
import hashlib

app = Flask(__name__)

# Shared data structures
file_lock = threading.Lock()
files = {
    'file1.txt': 'This is the content of file1.txt',
    'file2.txt': 'This is the content of file2.txt'
}


def hash_file_content(content):
    """Generate a hash for file content."""
    return hashlib.sha256(content.encode()).hexdigest()


def detect_duplicates(file_content):
    """Detect duplicate files based on content hash."""
    file_hash = hash_file_content(file_content)
    return file_hash in [hash_file_content(content) for content in files.values()]


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
        files[file_name] = file_content

    return jsonify({'message': 'File written successfully.'}), 200


@app.route('/read', methods=['GET'])
def read_files():
    return jsonify(files)


if __name__ == '__main__':
    # app.run(host='172.31.13.6', port=5000, debug=True)
    app.run(host='localhost', port=5000, debug=True)
    
