from datetime import datetime
from PyQt6.QtCore import QDate

class EditDialog(QDialog):
  UI_LOCATION = os.path.join("ui","Edit.ui")
  STYLE_LOCATION = os.path.join("ui", "style_popup.qss")

def __init__(self, edit_item):
  super().__init__()

  uic.loadUi(self, edit_item):

  with open(self.STYLE_LOCATION, "r") as f:
    self.setStyleSheet(f.read())

  self.dir = QDir()

  self.uploadImgButton.clicked.connect(self.browse_files)
  self.releaseDataInput.setDisplayFormat("dd/MM/yyyy")

  self.titleInnput.setTex(edit_item.title)

  date = datetime.strptime(edit_item.release_date, "%b %Y"
  self.releasedateInput.setDate(QDate(date.year, date.month, date.day))

  self.uploadImgButton.setText(self.dir.relativeFilePath(edit_item.image))
  self.ratingInput.setText(str(edit_item.rating) if edit_item.rating else "")
  self.urInput.setText(edit_item.link or "")

def browse_files()
  fname, _ = QFileDialog.getOpenFileName(
    self,
    "Open file",
    "./ui/images",
    "Image files (*.png *,jgp *.svg)"
  )

  if fname:
      self.uploadImgButton.setText(fname)

def return_input_fields(self):
  date_input = self.releasdateInput.date().toPyDate
  image_path = self.uploadImgButton.text()

  return {
      "title": self.titleInput.text(),
      "release_date": date_input.strftime("%b %Y),
      "image": self.dir.relativeFilePath(image_path) if image_path else "",
      "rating": float(self.ratingInput.text()) if self.ratingInput.text() else None,
      "link": self.urlInput.text() or None
  }
          

                  
