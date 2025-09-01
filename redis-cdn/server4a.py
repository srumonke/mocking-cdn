import requests

SERVER1_URL = "http://localhost:5000"  # Change to your Server 1 URL

def add_file(filename):
    response = requests.post(f"{SERVER1_URL}/add_file", json={"filename": filename})
    if response.status_code == 200:
        print("File added successfully to Server 1's file system.")
    else:
        print("Error occurred while adding the file.")

if __name__ == "__main__":
    filename = "file8.txt"
    add_file(filename)
