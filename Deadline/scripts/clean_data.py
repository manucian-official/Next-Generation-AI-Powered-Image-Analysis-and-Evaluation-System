import json
import os
import shutil
from datetime import datetime

# ======================
# CONFIG
# ======================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "art_dict.json")
TEMP_PATH = DATA_PATH + ".tmp"
BACKUP_PATH = DATA_PATH + ".bak"


# ======================
# HELPERS
# ======================
def parse_date(old_date: str) -> str:
    """
    Convert date cũ -> format "%b %Y"
    Ví dụ:
    "1503" -> "Jan 1503"
    "1889-06" -> "Jun 1889"
    """
    if not old_date:
        return "Jan 2000"

    try:
        # nếu chỉ có năm
        if old_date.isdigit():
            return f"Jan {old_date}"

        # nếu dạng YYYY-MM
        dt = datetime.strptime(old_date, "%Y-%m")
        return dt.strftime("%b %Y")

    except Exception:
        return "Jan 2000"


def validate_item(item: dict) -> bool:
    """
    Validate dữ liệu cơ bản
    """
    required_fields = ["title", "artist"]

    for field in required_fields:
        if not item.get(field):
            return False

    return True


# ======================
# MAIN CLEAN FUNCTION
# ======================
def clean_data():
    print("🚀 Start cleaning data...")

    # check file tồn tại
    if not os.path.exists(DATA_PATH):
        print("❌ Data file not found!")
        return

    # backup trước khi sửa
    shutil.copy(DATA_PATH, BACKUP_PATH)
    print(f"📦 Backup created: {BACKUP_PATH}")

    # load data
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("❌ Failed to read JSON:", e)
        return

    seen = set()
    cleaned = []

    for item in data:
        if not validate_item(item):
            print("⚠️ Skip invalid item:", item)
            continue

        title = item.get("title")
        artist = item.get("artist")

        # tránh duplicate
        key = (title.lower(), artist.lower())
        if key in seen:
            print(f"⚠️ Duplicate removed: {title}")
            continue

        seen.add(key)

        new_item = item.copy()

        # ======================
        # FIX DATE
        # ======================
        if "date" in new_item:
            new_item["release_date"] = parse_date(new_item["date"])
            del new_item["date"]

        elif "release_date" in new_item:
            new_item["release_date"] = parse_date(new_item["release_date"])

        else:
            new_item["release_date"] = "Jan 2000"

        # ======================
        # FIX RATING
        # ======================
        try:
            new_item["rating"] = float(new_item.get("rating", 0))
        except:
            new_item["rating"] = None

        # ======================
        # CLEAN STRING
        # ======================
        new_item["title"] = new_item["title"].strip()
        new_item["artist"] = new_item["artist"].strip()

        # ======================
        # DEFAULT FIELDS
        # ======================
        new_item["content"] = new_item.get("content", "")
        new_item["image"] = new_item.get("image", "")
        new_item["link"] = new_item.get("link", None)

        cleaned.append(new_item)

    # ======================
    # SAVE (ATOMIC WRITE)
    # ======================
    try:
        with open(TEMP_PATH, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, indent=4, ensure_ascii=False)

        os.replace(TEMP_PATH, DATA_PATH)

    except Exception as e:
        print("❌ Write failed:", e)
        return

    print("✅ Done!")
    print(f"📊 {len(data)} → {len(cleaned)} items")


# ======================
# RUN
# ======================
if __name__ == "__main__":
    clean_data()