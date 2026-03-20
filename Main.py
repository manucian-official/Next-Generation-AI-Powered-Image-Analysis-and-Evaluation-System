import sys
import os
#import models
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from models.models import ArtDatabase, ArtDatabase
from widgets.dialog import EditDialog, AddDialog

# # tạo cơ sở dữ liệu
# art_list = models.ArtDatabase()
# #tạo dữ liệu
# art_list.add_item({"title":"Mona Lisa","content":"A portrait painting by Leonardo da Vinci.","date":"1503","artist":"Leonardo da Vinci","rating":4.8,"image":"monalisa.jpg","link":"https://en.wikipedia.org/wiki/Mona_Lisa"})
# art_list.add_item({"title":"Starry Night",
#                           "content":"A night sky painting by Vincent van Gogh.",
#                           "date":"1889",
#                           "artist":"Vincent van Gogh",
#                           "rating":5.0,
#                           "image":"starrynight.jpg",
#                           "link":"https://en.wikipedia.org/wiki/The_Starry_Night"})
#  
class MainWindow(QMainWindow):
    # Định nghĩa vị trí của các file ui
    UI_LOCATION = os.path.join("qt","Mainqt.ui") # ==> ui/main_window1.ui
    
    def __init__(self):
        super().__init__()
        

        # Load file giao diện .ui và .qss
        self.qt = uic.loadUi(self.UI_LOCATION, self)

        # Hiển thị trang CRUD
        self.qt.stackedWidget.setCurrentIndex(1)
        # Tạo database
        self.dtb = ArtDatabase()
        self.dtb.load_data()

        # leftMenu
        self.qt.homeButton.clicked.connect(self.show_home_page)
        self.qt.museumButton.clicked.connect(self.show_museum_page)
        self.qt.GalleryButton.clicked.connect(self.show_Gallery_page)
        self.qt.exitButton.clicked.connect(self.exit_app)
        #setup trang CRUD
        self.setup_CRUD_page()
    
    def setup_CRUD_page(self):
       # hiển thị trang danh sách
       art_titles = self.dtb.get_title_list()
       self.qt.animeList.addItems(art_titles)
       self.qt.animeList.setCurrentRow(0)
       #xử lý các button CRUD
       #CRUD_Button
       self.qt.addButton.clicked.connect(self.add)
       self.qt.editButton.clicked.connect(self.edit)
       self.qt  .removeButton.clicked.connect(self.delete)
    def show_home_page(self):
        self.qt.stackedWidget.setCurrentIndex(0)
    def show_museum_page(self):
        self.qt.stackedWidget.setCurrentIndex(1)
    def show_Gallery_page(self):
        self.qt.stackedWidget.setCurrentIndex(2)
    def exit_app(self):
       QApplication.quit()
    ### CUD methods
    def add(self):
        curr_index = self.qt.artList.currentRow()
        # tạo dialog
        add_dialog = AddDialog()
        #nếu nhấn nút OK trên dialog
        if add_dialog.exec():
            #lấy dữ liệu từ dialog
            inputs = add_dialog.return_input_fields()
            #thêm item vào list widget
            self.ui.artList.addItem(curr_index, inputs["title"])
            #thêm dữ liệu vào database
            self.dtb.add_item(inputs)
    
    def edit(self):
        #lấy item đang chọn
        curr_index = self.ui.artList.currentRow()
        item = self.ui.artList.item(curr_index)
        item_title = item.text()
        edit_item = self.dtb.get_item_by_title(item_title)
        #tạo dialog edit
        if item is not None:
            edit_dialog = EditDialog(edit_item)
            #nếu nhấn nút ok trên dialog
            if edit_dialog.exec():
                #lấy dữ liệu từ dialog
                inputs = edit_dialog.return_input_fields()
                #sửa lại tên item trên list widget
                item.setText(inputs["title"])
                #sửa dữ liệu trong database
                self.dtb.edit_item(item_title, inputs)
    
    def delete(self):
        #lấy item đang chọn
        curr_index = self.ui.artList.currentRow()
        item = self.ui.artList.item(curr_index)
        item_title = item.text()
        #tạo message box xác nhận xóa
        if item is not None:
            choice = QMessageBox.question(self, "Remove Anime",
                                            "Do you want to remove this anime?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            #nếu chọn nút "Yes"
            if choice == QMessageBox.StandardButton.Yes:
                #xóa item khỏi list Widget
                item = self.ui.artList.takeItem(curr_index)
                #xóa dữ liệu trong database
                self.dtb.delete_item(item_title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    #Hiển thị cửa sổ ra màn hình
    window.show()
    sys.exit(app.exec())


                                            
            
                






        
    
