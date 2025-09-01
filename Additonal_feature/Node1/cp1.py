import requests

SERVER_URL = "http://localhost:5000"

def add_file():
    file_name = input("Enter file name: ")
    file_content = input("Enter file content: ")
    
    payload = {'file_name': file_name, 'file_content': file_content}
    response = requests.post(f"{SERVER_URL}/write", json=payload)
    print(response.json())


def main():
    add_file()


if __name__ == "__main__":
    main()
