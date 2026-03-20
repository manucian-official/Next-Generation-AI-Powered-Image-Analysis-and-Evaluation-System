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
        uic.loadUi(self.UI_LOCATION, self)
        with open(self.STYLE_LOCATION, "r") as f:
            self.setStyleSheet(f.read())
            
        
        # Tạo đối tượng QDir để quản lý đường dẫn
        self.dir = QDir()

        # Nút tải ảnh từ máy tính
        self.ui.uploadImgButton.clicked.connect(self.browse_files)
        self.ui.releasedateInput.setDisplayFormat("dd/MM/yyyy") # Format ngày tháng năm
    
    def browse_files(self):
        """
        Phương thức mở file dialog để chọn ảnh
        """
        fname = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "./ui/images",
            "Image files (*.png *.jpg *.svg)"
        )
            
    if fname:
        self.uploadImgButton.setText(fname)

    def return_input_fields(self):
        """
        Thu thập dữ liệu của tất cả các trường và trả về một dict
        """
        # Xử lý trường ngày tháng năm
        date_input = self.releasedateInput.date().toPyDate()
        image_path_input = self.uploadImgButton.text()
        
        # Trả dữ liệu
        return {
            "title": self.ui.titleInput.text(),
            "release_date": date_input.strftime("%b %Y"), # => "Jan 2026"
            "image": self.dir.relativeFilePath(image_path) if image_path else ""
            "rating": float(self.ui.ratingInput.text()) if self.ratingInput.text() else None,
            "link": self.urlInput.text() or None
        }
