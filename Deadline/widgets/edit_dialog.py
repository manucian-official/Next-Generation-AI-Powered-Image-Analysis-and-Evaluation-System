import os
from datetime import datetime

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6.QtCore import QDate, QDir


class EditDialog(QDialog):
    UI_LOCATION = os.path.join("ui", "Edit.ui")
    STYLE_LOCATION = os.path.join("ui", "style_popup.qss")

    def __init__(self, edit_item):
        super().__init__()

        # Load UI
        uic.loadUi(self.UI_LOCATION, self)

        # Load style
        if os.path.exists(self.STYLE_LOCATION):
            with open(self.STYLE_LOCATION, "r") as f:
                self.setStyleSheet(f.read())

        self.dir = QDir()

        # ======================
        # CONNECT
        # ======================
        self.uploadImgButton.clicked.connect(self.browse_files)
        self.releasedateInput.setDisplayFormat("dd/MM/yyyy")

        # ======================
        # FILL DATA
        # ======================
        self.titleInput.setText(edit_item.title)

        # Date
        try:
            date = datetime.strptime(edit_item.release_date, "%b %Y")
            self.releasedateInput.setDate(QDate(date.year, date.month, 1))
        except:
            self.releasedateInput.setDate(QDate.currentDate())

        # Image
        if edit_item.image:
            self.uploadImgButton.setText(
                self.dir.relativeFilePath(edit_item.image)
            )

        # Rating (QLineEdit)
        self.ratingInput.setText(
            str(edit_item.rating) if edit_item.rating else ""
        )

        # Link
        self.urlInput.setText(edit_item.link or "")

    # ======================
    # BROWSE IMAGE
    # ======================
    def browse_files(self):
        fname, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "./asset",
            "Image files (*.png *.jpg *.jpeg *.svg)"
        )

        if fname:
            self.uploadImgButton.setText(fname)

    # ======================
    # RETURN DATA
    # ======================
    def return_input_fields(self):
        date_input = self.releasedateInput.date().toPyDate()
        image_path = self.uploadImgButton.text()

        return {
            "title": self.titleInput.text().strip(),
            "release_date": date_input.strftime("%b %Y"),
            "image": self.dir.relativeFilePath(image_path) if image_path else "",
            "rating": float(self.ratingInput.text()) if self.ratingInput.text() else None,
            "link": self.urlInput.text().strip() or None
        }