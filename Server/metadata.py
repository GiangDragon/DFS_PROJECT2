import os
import json

def save_metadata(filename, metadata):
    os.makedirs(METADATA_DIR, exist_ok=True)

    path = os.path.join(METADATA_DIR, f"{filename}.json")
    with open(path, "w") as f:
    json.dump(metadata, f)

def get_metadata(filename):
    path = os.path.join(METADATA_DIR, f"{filename}.json")

    if not os.path.exists(path):
    raise FileNotFoundError(f"Metadata not found: {path}")

    with open(path, "r") as f:
    return json.load(f)

def delete_metadata(filename):
    path = os.path.join(METADATA_DIR, f"{filename}.json")
    if not os.path.exists(path):
        return False  # File không tồn tại
    try:
        os.remove(path)
        return True  # Xóa thành công
    except OSError as e:
        raise OSError(f"Không thể xóa file metadata {path}: {e}")