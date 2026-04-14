import requests
import os

SERVER = "http://3.26.50.235:5000"
STORAGE_DIR = "./storage"

# Tạo thư mục storage nếu chưa tồn tại
os.makedirs(STORAGE_DIR, exist_ok=True)

def upload(file_path):
    if not os.path.exists(file_path):
        print("File không tồn tại!")
        return

    filename = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        files = {"file": (filename, f)}
        r = requests.post(SERVER + "/upload", files=files)
        print("Upload response:", r.json())

def download(filename, save_path=None):
    r = requests.get(SERVER + "/download/" + filename)

    if r.status_code == 200:
        if save_path is None:
            save_path = os.path.join(STORAGE_DIR, filename)

        with open(save_path, "wb") as f:
            f.write(r.content)

        print(f"Downloaded file saved at: {save_path}")
    else:
        print("Error:", r.json())

# Upload file từ thư mục hiện tại
upload("test.txt")

# Download file về thư mục ./storage
download("test.txt")