import json
import os

DATA_PATH = os.path.join("data", "art_dict.json")
TEMP_PATH = DATA_PATH + ".tmp"


def clean_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    seen = set()
    cleaned = []

    for item in data:
        title = item.get("title")
        artist = item.get("artist")

        if not title:
            continue

        key = (title, artist)

        if key in seen:
            continue

        seen.add(key)

        new_item = item.copy()

        # convert date -> release_date
        if "date" in new_item:
            year = new_item["date"]
            new_item["release_date"] = f"Jan {year}"
            del new_item["date"]

        cleaned.append(new_item)

    # ghi file an toàn
    with open(TEMP_PATH, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)

    os.replace(TEMP_PATH, DATA_PATH)

    print(f"✅ Cleaned {len(data)} -> {len(cleaned)} items")


if __name__ == "__main__":
    clean_data()
