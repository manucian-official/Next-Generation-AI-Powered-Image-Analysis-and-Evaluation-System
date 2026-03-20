import os
from datetime import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6.QtCore import QDate, QDir



class AddDialog(QDialog):
    """
    Hộp thoại Add
    """
    UI_LOCATION = os.path.join("ui", "ADD.ui") # => ui/add_dialog.ui
    STYLE_LOCATION = os.path.join("ui", "style_popup.qss")

    def __init__(self):
        super().__init__()

        # Load giao diện
        self.ui = uic.loadUi(self.UI_LOCATION, self)
        with open(self.STYLE_LOCATION, "r") as style_file:
            style_config = style_file.read()
        self.setStyleSheet(style_config)
        
        # Tạo đối tượng QDir để quản lý đường dẫn
        self.dir = QDir()

        # Nút tải ảnh từ máy tính
        self.ui.uploadImgButton.clicked.connect(self.browse_files)
        self.ui.releasedateInput.setDisplayFormat("dd/MM/yyyy") # Format ngày tháng năm
    
    def browse_files(self):
        """
        Phương thức mở file dialog để chọn ảnh
        """
        fname = QFileDialog.getOpenFileName(self,
                                            'Open file', 
                                            './ui/images',
                                            filter='Image files (*.png *.jpg *.svg)'
                                            )
        self.ui.uploadImgButton.setText(fname[0])
        return fname

    def return_input_fields(self) -> dict:
        """
        Thu thập dữ liệu của tất cả các trường và trả về một dict
        """
        # Xử lý trường ngày tháng năm
        date_input = self.ui.releasedateInput.date().toPyDate() # formatted dd/MM/yyyy
        image_path_input = self.ui.uploadImgButton.text()
        
        # Trả dữ liệu
        return {
            "title": self.ui.titleInput.text(),
            "release_date": date_input.strftime("%b %Y"), # => "Jan 2026"
            "image": self.dir.relativeFilePath(image_path_input),
            "rating": float(self.ui.ratingInput.text()) if self.ui.ratingInput.text() else None,
            "link": self.ui.urlInput.text() if self.ui.urlInput.text() else "None"
        }


class EditDialog(QDialog):
    """
    Hộp thoại Edit 
    """
    UI_LOCATION = os.path.join("ui", "Edit.ui")
    STYLE_LOCATION = os.path.join("ui", "style_popup.qss")

    def __init__(self, edit_item): # Nhận vào đối tượng
        super().__init__()

        # Load giao diện
        self.ui = uic.loadUi(self.UI_LOCATION, self)
        with open(self.STYLE_LOCATION, "r") as style_file:
            style_config = style_file.read()
        self.setStyleSheet(style_config)

        self.ui.releasedateInput.setDisplayFormat("dd/MM/yyyy")
        self.ui.uploadImgButton.clicked.connect(self.browse_files)
        
        self.dir = QDir()

        # Hiển thị dữ liệu hiện tại của item
        self.ui.titleInput.setText(edit_item.title)
        date = datetime.strptime(edit_item.release_date, '%b %Y')
        self.ui.releasedateInput.setDate(QDate(date.year, date.month, date.day))
        self.ui.uploadImgButton.setText(self.dir.relativeFilePath(edit_item.image))
        self.ui.ratingInput.setText(str(edit_item.rating))
        self.ui.urlInput.setText(edit_item.link)
    
    def browse_files(self):
        """
        Phương thức mở file dialog để chọn ảnh
        """
        fname = QFileDialog.getOpenFileName(self,
                                            'Open file', 
                                            './ui/images',
                                            filter='Image files (*.png *.jpg *.svg)'
                                            )
        self.ui.uploadImgButton.setText(fname[0])
        return fname
    
    def return_input_fields(self) -> dict:
        """
        Thu thập dữ liệu của tất cả các trường và trả về một dict
        """
        date_input = self.ui.releasedateInput.date().toPyDate() # formatted YYYY-mm-dd
        image_path_input = self.ui.uploadImgButton.text()

        return {
            "title": self.ui.titleInput.text(),
            "release_date": date_input.strftime("%b %Y"),
            "image": self.dir.relativeFilePath(image_path_input),
            "rating": float(self.ui.ratingInput.text()) if self.ui.ratingInput.text() else None,
            "link": self.ui.urlInput.text() if self.ui.urlInput.text() else "None"
        }
