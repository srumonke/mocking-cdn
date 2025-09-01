import requests
import threading

SERVER_URL = "http://localhost:5000"

def check_file_availability(file_name):
    response = requests.get(f"{SERVER_URL}/read")
    files = response.json()
    return file_name not in files

def request_file(file_name, file_content):
    payload = {'file_name': file_name, 'file_content': file_content}
    response = requests.post(f"{SERVER_URL}/write", json=payload)
    print(response.json())

def main():
    while True:
        file_name = input("Enter file name (press 'q' to quit): ")
        if file_name.lower() == 'q':
            break
        
        # Check if the file is available
        if not check_file_availability(file_name):
            print(f"File '{file_name}' is busy. Please try again later.")
            continue
        
        file_content = input("Enter file content: ")


        request_file(file_name, file_content)

if __name__ == "__main__":
    main()
