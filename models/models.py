import operator
from datetime import datetime
from data import data_io


class ArtItem:
    def __init__(self, title, content, release_date, artist,
                 rating=None, image=None, link=None):

        self.title = title
        self.content = content
        self.release_date = release_date
        self.artist = artist
        self.rating = float(rating) if rating is not None else None
        self.image = image
        self.link = link

    def update(self, new_data: dict):
        for attr, value in new_data.items():
            if value is not None:   # FIX
                setattr(self, attr, value)

    def to_dict(self):
        """Serialize object -> dict"""
        return {
            "title": self.title,
            "content": self.content,
            "release_date": self.release_date,
            "artist": self.artist,
            "rating": self.rating,
            "image": self.image,
            "link": self.link
        }


class ArtDatabase:
    def __init__(self):
        self.art_items_list = []
        self.art_dict_data = data_io.load_json_data()

    def load_data(self):
        for art in self.art_dict_data:
            self.art_items_list.append(
                ArtItem(**art)
            )

    def save(self):
        """Save toàn bộ data"""
        self.art_dict_data = [item.to_dict() for item in self.art_items_list]
        data_io.write_json_data(self.art_dict_data)

    # ======================
    # CRUD
    # ======================
    def get_item_by_title(self, title):
        for item in self.art_items_list:
            if item.title == title:
                return item
        return None

    def add_item(self, data):
        # check duplicate
        if self.get_item_by_title(data["title"]):
            raise ValueError("Title already exists")

        self.art_items_list.append(ArtItem(**data))
        self.save()

    def edit_item(self, title, new_data):
        item = self.get_item_by_title(title)
        if item:
            item.update(new_data)
            self.save()

    def delete_item(self, title):
        item = self.get_item_by_title(title)
        if item:
            self.art_items_list.remove(item)
            self.save()

    # ======================
    # SEARCH / SORT
    # ======================
    def search_by_title(self, keyword):
        return [
            item for item in self.art_items_list
            if keyword.lower() in item.title.lower()
        ]

    def sort_by_rating(self):
        self.art_items_list.sort(
            key=lambda x: x.rating if x.rating is not None else -1,
            reverse=True
        )

    def sort_by_title(self):
        self.art_items_list.sort(key=lambda x: x.title.lower())

    def sort_by_date(self):
        self.art_items_list.sort(
            key=lambda x: parse_date(x.release_date),
            reverse=True
        )

    # ======================
    # UTIL
    # ======================
    def get_title_list(self):
        return [item.title for item in self.art_items_list]


def parse_date(date_text):
    return datetime.strptime(date_text, "%b %Y")
