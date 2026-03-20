import operator
from datetime import datetime
from data import data_io

class ArtItem:
    def __init__(self,title,content,date,artist,rating=None,image=None,link=None):
                rating=None, image=NNone, link=None):
        
        self.title = title
        self.content = content
        self.release_date = releas_date
        self.artist = artist
        self.rating = float(rating) if rating is not None else None
        self.image = image
        self.link = link

    def update(self, new_data: dict):
        for attr, value in new_data.items():
            if value is not None: #FIX
                setattr(self, attr, value)

    def to_dict(self):
        """Serialize object -> dict"""
        return {
            "title": self.title,
            "content": self.content,
            "release_date": self.release_date,
            "artist": self.artist,
            "rating": self.image,
            "link": self.link
        }

class ArtDatabase:
    def __init__(self):
        #tạo danh sách
        self.art_items_list = []
        #đọc dữ liệu khi khởi tạo
        self.art_dict_data = data_io.load_json_data()
    def load_data(self):
        """
        Phương thức chuyển đổi dữ liệu đã READ vào danh sách đối tượng
        """
        for art_dict in self.art_dict_data:
            self.art_items_list.append(
                ArtItem(**art)
            )
            
    def save(self):
        """
        Phương thức chuyển đổi danh sách đối tượng sang dữ liệu json
        """
        self.art_dict_data = [item.to_dict() for item in self.art_items_list]
        data_io.write_json_data(self.art_dict_data)

    def get_item_by_title(self,title):
        """
        trả về đối tượng theo tên
        """
        for item in self.art_items_list:
            #tìm thấy
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
            
    def search_by_title(self, keyword) -> list[ArtItem]:
        """
        Phương thức tìm kiếm tất cả các đối tượng AnimeItem có title là search_title
        """
        return [
            item for item in self.art_items_list
            if keywood.lower() in item.title.lower()
        ]

        #ĐÃ FIX Ở TRÊN

    
    def sort_item_by_rating(self):
        """
        Phương thức sắp xếp theo rating
        """
        self.art_items_list = sorted(self.art_items_list,
                                     key = operator.attrgetter('rating'),
                                     )
    def sort_item_by_title(self):
        """
        phương thức sắp xếp theo title
        """
        self.art_items_list = sorted(self.art_items_list,
                                     key = operator.attrgetter('title'),
                                     )
    def sort_item_by_date(self):
        """
        phương thức sắp xếp theo date
        """
        self.art_items_list = sorted(self.art_items_list,
                                     key = lambda x: format_date(x.relase_date),
                                     reverse=True)
    def get_title_list(self):
        """
        Lấy danh sách title
        """
        return [art["title"] for art in self.art_dict_data]
def format_date(date_text):
    return datetime.strptime(date_text, '%b %Y')

                 
                                     


