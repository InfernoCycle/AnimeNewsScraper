from PySide6.QtWidgets import QApplication
import sys
from widgets.central import Center
if "__main__" == __name__:
  app = QApplication([])
  
  window = Center()
  window.show()
  
  app.exec()