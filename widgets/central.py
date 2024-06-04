from PySide6.QtWidgets import QMessageBox, QFileDialog, QStatusBar, QMenu, QMainWindow, QComboBox, QTabWidget, QAbstractItemView, QListWidgetItem, QListWidget, QSizePolicy, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout
from PySide6.QtCore import QUrl
from widgets.page1 import Home
from widgets.exports import Exports
from threading import Thread

class Center(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Inferno Anime News Scraper")
    self.Home = Home()
    self.setCentralWidget(self.Home)
    self.setMinimumSize(1080, 720)
    
    self.export_win = None
    
    self.owner_msg = QMessageBox()
    self.version_msg = QMessageBox()
    self.source_msg = QMessageBox()
    
    menu = self.menuBar()
    file = menu.addMenu("File")
    exports = file.addAction("Export")
    exports.triggered.connect(self.open_wizard)
    
    about = menu.addMenu("About")
    version = about.addAction("Version")
    version.triggered.connect(self.show_version)
    
    source = about.addAction("Source")
    source.triggered.connect(self.show_source)
    
    owner = about.addAction("Owner")
    owner.triggered.connect(self.show_true_owner)
    
    options = menu.addMenu("Options")
    #Version 2 Font = file.addAction("Font")
    
    self.setMenuBar(menu)
    #self.showMaximized()
  
  def show_source(self):
    self.source_msg.information(self, "Source", "Anime News Network\nURL: https://www.animenewsnetwork.com/", QMessageBox.Ok)
  def show_version(self):
    self.version_msg.information(self, "Version", "Version 1.0", QMessageBox.Ok)
  def show_true_owner(self):
      message = """
      This is the property of InfernoCycle.
      For more projects from me please visit my github at
      https://github.com/InfernoCycle"""
      self.owner_msg.information(self, "Owner", message, QMessageBox.Ok)
  def open_wizard(self):
    #if(self.export_win is None):
     # self.export_win = Exports(self.Home)
    self.export_win = Exports(self.Home)
    self.export_win.show()