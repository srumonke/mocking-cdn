import requests

SERVER1_URL = "http://localhost:5000"  # Change to your Server 1 URL

def request_file(filename):
    response = requests.get(f"{SERVER1_URL}/get_file?filename={filename}")
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            print("File Path:", data["path"])
        else:
            print("Error:", data["message"])
    else:
        print("File not found in any servers.")

if __name__ == "__main__":
    filename = input("Enter the name of the file to request: ")
    request_file(filename)
