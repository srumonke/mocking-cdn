import requests

# SERVER_URL = "http://172.31.13.6:5000"
SERVER_URL = "http://localhost:5000"

def request_file():
    file_name = input("Enter file name: ")
    response = requests.get(f"{SERVER_URL}/read")
    files = response.json()
    if file_name in files:
        print(f"File '{file_name}' content: {files[file_name]}")
    else:
        print(f"File '{file_name}' does not exist.")


def main():
    request_file()


if __name__ == "__main__":
    main()
