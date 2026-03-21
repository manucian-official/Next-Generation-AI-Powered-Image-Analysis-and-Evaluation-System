import os
from datetime import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt6.QtCore import QDate, QDir
from PyQt6.QtGui import QDoubleValidator


class BaseDialog(QDialog):
    STYLE_LOCATION = os.path.join("ui", "style_popup.qss")

    def setup_common(self):
        with open(self.STYLE_LOCATION, "r") as f:
            self.setStyleSheet(f.read())

        self.dir = QDir()

        # Validator rating
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.ui.ratingInput.setValidator(validator)

        self.ui.releasedateInput.setDisplayFormat("dd/MM/yyyy")
        self.ui.uploadImgButton.clicked.connect(self.browse_files)

    def browse_files(self):
        fname = QFileDialog.getOpenFileName(
            self,
            'Open file',
            './ui/images',
            filter='Image files (*.png *.jpg *.svg)'
        )

        if fname[0]:
            self.ui.uploadImgButton.setText(fname[0])

        return fname

    def parse_rating(self):
        text = self.ui.ratingInput.text().strip()
        if not text:
            return None
        try:
            return float(text)
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Rating phải là số!")
            return None

    def build_data(self):
        date_input = self.ui.releasedateInput.date().toPyDate()
        image_path = self.ui.uploadImgButton.text()

        rating = self.parse_rating()
        if rating is None and self.ui.ratingInput.text():
            return None

        image = self.dir.relativeFilePath(image_path) if os.path.exists(image_path) else None

        return {
            "title": self.ui.titleInput.text().strip(),
            "release_date": date_input.strftime("%b %Y"),
            "content": "",  # FIX luôn tránh lỗi models
            "image": image,
            "rating": rating,
            "link": self.ui.urlInput.text().strip() or None
        }


class AddDialog(BaseDialog):
    UI_LOCATION = os.path.join("ui", "ADD.ui")

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(self.UI_LOCATION, self)
        self.setup_common()

    def return_input_fields(self):
        return self.build_data()


class EditDialog(BaseDialog):
    UI_LOCATION = os.path.join("ui", "Edit.ui")

    def __init__(self, edit_item):
        super().__init__()
        self.ui = uic.loadUi(self.UI_LOCATION, self)
        self.setup_common()

        self.ui.titleInput.setText(edit_item.title or "")

        # 🔥 FIX CHÍNH Ở ĐÂY
        if edit_item.release_date:
            try:
                date = datetime.strptime(edit_item.release_date, '%b %Y')
                self.ui.releasedateInput.setDate(QDate(date.year, date.month, 1))
            except Exception:
                self.ui.releasedateInput.setDate(QDate.currentDate())
        else:
            self.ui.releasedateInput.setDate(QDate.currentDate())

        self.ui.uploadImgButton.setText(self.dir.relativeFilePath(edit_item.image or ""))

        self.ui.ratingInput.setText("" if edit_item.rating is None else str(edit_item.rating))
        self.ui.urlInput.setText("" if edit_item.link is None else edit_item.link)

    def return_input_fields(self):
        return self.build_data()