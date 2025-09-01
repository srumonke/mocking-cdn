import requests

SERVER_URL = "http://localhost:5000"

def request_file_version():
    file_name = input("Enter file name: ")
    version = int(input("Enter version number: "))
    response = requests.get(f"{SERVER_URL}/read_version?file_name={file_name}&version={version}")
    file_version = response.json()
    if 'message' in file_version:
        print(file_version['message'])
    else:
        print(f"File '{file_name}' version {version} content: {file_version['content']}")


def main():
    request_file_version()


if __name__ == "__main__":
    main()
