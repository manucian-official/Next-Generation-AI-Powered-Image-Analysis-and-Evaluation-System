import sys
import os

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox

from models.models import ArtDatabase
from widgets.dialog import EditDialog, AddDialog


class MainWindow(QMainWindow):
    """
    Main application window handling:
    - Navigation (Home / Museum / Gallery)
    - CRUD operations
    """

    UI_LOCATION = os.path.join("qt", "Mainqt.ui")

    def __init__(self):
        super().__init__()

        # Load UI
        uic.loadUi(self.UI_LOCATION, self)

        # Init database
        self.dtb = ArtDatabase()
        self.dtb.load_data()

        # Setup UI
        self.init_navigation()
        self.setup_crud_page()

        # Default page
        self.stackedWidget.setCurrentIndex(1)

    # =======================
    # NAVIGATION
    # =======================
    def init_navigation(self):
        self.homeButton.clicked.connect(lambda: self.switch_page(0))
        self.museumButton.clicked.connect(lambda: self.switch_page(1))
        self.GalleryButton.clicked.connect(lambda: self.switch_page(2))
        self.exitButton.clicked.connect(QApplication.quit)

    def switch_page(self, index: int):
        self.stackedWidget.setCurrentIndex(index)

    # =======================
    # CRUD SETUP
    # =======================
    def setup_crud_page(self):
        """Load data into list and bind buttons"""

        self.refresh_list()

        # Bind buttons
        self.addButton.clicked.connect(self.add_item)
        self.editButton.clicked.connect(self.edit_item)
        self.removeButton.clicked.connect(self.delete_item)

    def refresh_list(self):
        """Reload UI list from database"""
        self.artList.clear()
        titles = self.dtb.get_title_list()
        self.artList.addItems(titles)

        if titles:
            self.artList.setCurrentRow(0)

    # =======================
    # CRUD OPERATIONS
    # =======================
    def add_item(self):
        dialog = AddDialog()

        if dialog.exec():
            data = dialog.return_input_fields()

            # Update DB
            self.dtb.add_item(data)

            # Update UI
            self.artList.addItem(data["title"])

    def edit_item(self):
        index = self.artList.currentRow()
        item = self.artList.item(index)

        if item is None:
            return

        old_title = item.text()
        data = self.dtb.get_item_by_title(old_title)

        dialog = EditDialog(data)

        if dialog.exec():
            new_data = dialog.return_input_fields()

            # Update UI
            item.setText(new_data["title"])

            # Update DB
            self.dtb.edit_item(old_title, new_data)

    def delete_item(self):
        index = self.artList.currentRow()
        item = self.artList.item(index)

        if item is None:
            return

        title = item.text()

        confirm = QMessageBox.question(
            self,
            "Delete",
            "Are you sure you want to delete this item?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.artList.takeItem(index)
            self.dtb.delete_item(title)


# =======================
# MAIN ENTRY
# =======================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
