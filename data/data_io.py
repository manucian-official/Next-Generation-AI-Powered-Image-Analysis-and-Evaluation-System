import json
import os

DATA_PATH = os.path.join("data", "art_dict.json")


def load_json_data():
    """
    Đọc dữ liệu JSON an toàn
    """
    # nếu chưa có file → tạo file rỗng
    if not os.path.exists(DATA_PATH):
        return []

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # file bị lỗi → tránh crash
        print("⚠️ JSON corrupted, returning empty list")
        return []


def write_json_data(json_data):
    """
    Ghi dữ liệu JSON an toàn (atomic write)
    """
    temp_path = DATA_PATH + ".tmp"

    # ghi file tạm trước
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    # replace file chính
    os.replace(temp_path, DATA_PATH)
