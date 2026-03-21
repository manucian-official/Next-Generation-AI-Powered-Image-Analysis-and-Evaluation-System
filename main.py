import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox

from models.models import ArtDatabase
from widgets.dialog import EditDialog, AddDialog


class MainWindow(QMainWindow):
    UI_LOCATION = os.path.join("ui", "Mainqt.ui")

    def __init__(self):
        super().__init__()
        uic.loadUi(self.UI_LOCATION, self)

        self.stackedWidget.setCurrentIndex(1)

        self.dtb = ArtDatabase()
        self.dtb.load_data()

        self.homeButton.clicked.connect(self.show_home_page)
        self.museumButton.clicked.connect(self.show_museum_page)
        self.GalleryButton.clicked.connect(self.show_gallery_page)
        self.exitButton.clicked.connect(self.exit_app)

        self.setup_CRUD_page()

    def setup_CRUD_page(self):
        self.animeList.clear()

        titles = self.dtb.get_title_list()
        self.animeList.addItems(titles)

        if titles:
            self.animeList.setCurrentRow(0)

        self.addButton.clicked.connect(self.add)
        self.editButton.clicked.connect(self.edit)
        self.removeButton.clicked.connect(self.delete)

    def show_home_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_museum_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def show_gallery_page(self):
        self.stackedWidget.setCurrentIndex(2)

    def exit_app(self):
        QApplication.quit()

    def add(self):
        dialog = AddDialog()
        if dialog.exec():
            inputs = dialog.return_input_fields()
            if not inputs:
                return
            self.animeList.addItem(inputs["title"])
            self.dtb.add_item(inputs)

    def edit(self):
        idx = self.animeList.currentRow()
        item = self.animeList.item(idx)
        if item is None:
            return

        old_title = item.text()
        edit_item = self.dtb.get_item_by_title(old_title)

        dialog = EditDialog(edit_item)
        if dialog.exec():
            inputs = dialog.return_input_fields()
            if not inputs:
                return
            item.setText(inputs["title"])
            self.dtb.edit_item(old_title, inputs)

    def delete(self):
        idx = self.animeList.currentRow()
        item = self.animeList.item(idx)
        if item is None:
            return

        title = item.text()

        confirm = QMessageBox.question(
            self,
            "Remove",
            "Delete this item?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.animeList.takeItem(idx)
            self.dtb.delete_item(title)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())