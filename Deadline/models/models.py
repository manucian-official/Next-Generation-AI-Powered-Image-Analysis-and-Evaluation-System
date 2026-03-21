import json
import os


class Art:
    def __init__(self, title, release_date, content="", image=None, rating=None, link=None):
        self.title = title
        self.release_date = release_date
        self.content = content
        self.image = image
        self.rating = rating
        self.link = link

    def to_dict(self):
        return {
            "title": self.title,
            "release_date": self.release_date,
            "content": self.content,
            "image": self.image,
            "rating": self.rating,
            "link": self.link
        }


class ArtDatabase:
    DATA_PATH = os.path.join("data", "art_dict.json")

    def __init__(self):
        self.data = []

    def load_data(self):
        if not os.path.exists(self.DATA_PATH):
            self.data = []
            return

        with open(self.DATA_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)

        self.data = []

        for item in raw:
            art = Art(
                title=item.get("title"),
                release_date=item.get("release_date") or "Jan 2000",  # 🔥 FIX
                content=item.get("content", ""),
                image=item.get("image"),
                rating=item.get("rating"),
                link=item.get("link"),
            )
            self.data.append(art)

    def save_data(self):
        with open(self.DATA_PATH, "w", encoding="utf-8") as f:
            json.dump([a.to_dict() for a in self.data], f, indent=4, ensure_ascii=False)

    def add_item(self, art_dict):
        art = Art(
            title=art_dict.get("title"),
            release_date=art_dict.get("release_date") or "Jan 2000",
            content=art_dict.get("content", ""),
            image=art_dict.get("image"),
            rating=art_dict.get("rating"),
            link=art_dict.get("link"),
        )
        self.data.append(art)
        self.save_data()

    def get_title_list(self):
        return [a.title for a in self.data]

    def get_item_by_title(self, title):
        for a in self.data:
            if a.title == title:
                return a
        return None

    def edit_item(self, old_title, new_data):
        for a in self.data:
            if a.title == old_title:
                a.title = new_data.get("title", a.title)
                a.release_date = new_data.get("release_date", a.release_date)
                a.content = new_data.get("content", a.content)
                a.image = new_data.get("image", a.image)
                a.rating = new_data.get("rating", a.rating)
                a.link = new_data.get("link", a.link)
                break
        self.save_data()

    def delete_item(self, title):
        self.data = [a for a in self.data if a.title != title]
        self.save_data()