import operator
from datetime import datetime

from data import data_io

class ArtItem:
    def __init__(self,title,content,date,artist,rating=None,image=None,link=None):
        self.title = title
        self.content = content
        self.date = date
        self.artist = artist
        # không có thì = 0 (ko bắt buộc)
        self.rating = float(rating) if rating else 0
        self.image = image
        self.link = link

    def update(Self, new_data:dict):
        for attribute, value in new_data.items():
            #chỉ khi thuộc tính có giá trị mới cập nhật
            if value:
                setattr(Self, attribute, value)

class ArtDatabase:
    def __init__(self):
        #tạo danh sách
        self.art_items_list = list()
        #đọc dữ liệu khi khởi tạo
        self.art_dict_data = data_io.load_json_data()
    def load_data(self):
        """
        Phương thức chuyển đổi dữ liệu đã READ vào danh sách đối tượng
        """
        for art_dict in self.art_dict_data:
            art = ArtItem(title=art_dict["title"],
                          content=art_dict["content"],
                          date=art_dict["date"],
                          artist=art_dict["artist"],
                          rating=art_dict["rating"],
                          image=art_dict["image"],
                          link=art_dict["link"])
            self.art_items_list.append(art)

    def items_to_data(self):
        """
        Phương thức chuyển đổi danh sách đối tượng sang dữ liệu json
        """               
        json_data = list()
        for art in self.art_items_list:
            json_data.append(art.__dict__)
        return json_data
    def get_item_by_title(self,title):
        """
        trả về đối tượng theo tên
        """
        for art_items in self.art_items_list:
            #tìm thấy
            if art_items.title == title:
                return art_items
        #không thấy
        return False
    def add_item(self,art_dict):
        """
        Thêm đối tượng mới vào danh sách
        """

        new_item = ArtItem(title=art_dict["title"],
                      content=art_dict["content"],
                      date=art_dict["date"],
                      artist=art_dict["artist"],
                      rating=art_dict["rating"],
                      image=art_dict["image"],
                      link=art_dict["link"])
        
        #thêm vào danh sách phần tử
        self.art_items_list.append(new_item)
        # Thực hiện WRITE mỗi khi thay đổi danh sách đối tượng
        self.art_dict_data.append(art_dict)
        data_io.write_json_data(self.art_dict_data)

    def edit_item(self, edit_title, new_data):
        """
        Chỉnh sửa thông tin của một đối tượng trong danh sách
        """
        item = self.get_item_by_title(edit_title)
        if item:
            item.update(new_data)
            # Cập nhật lại dữ liệu JSON
            self.art_dict_data = self.items_to_data()
            data_io.write_json_data(self.art_dict_data)

    def delete_item(self,delete_title):
        """
        Phương thức xoá đối tượng AnimeItem có title là delete_title
        """
        matched = self.get_item_by_title(delete_title)
        if matched:
            self.art_items_list.remove(matched)
            #thực hiện Write mỗi khi thay đổi danh sách đối tượng
            self.art_dict_data = self.items_to_data()
            data_io.write_json_data(self.art_dict_data)
    def search_by_title(self,search_title) -> list[ArtItem]:
        """
        Phương thức tìm kiếm tất cả các đối tượng AnimeItem có title là search_title
        """
        matched_items = []
        for art_item in self.art_items_list:
            if search_title.lower() in art_item.title.lower():
                matched_items.append(art_item)
        return matched_items
    
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

                 
                                     


