from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QMessageBox, QProgressBar, QComboBox, QButtonGroup, QGroupBox, QRadioButton,QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout, QGridLayout
from PySide6.QtCore import Qt, SIGNAL, QThread, QObject
from utils.formatting import Cleaner, Threader
import time
from utils.month_convert import DateUtil
from threading import Thread

class Exports(QWidget):
  def __init__(self, home_obj):
    super().__init__()
    self.cleaner = Cleaner()
    self.dateUtil = DateUtil()
    self.type = "Article"
    self.home_obj = home_obj
    MainLayout = QGridLayout()
    self.subtract_from_year = 2
    self.setWindowTitle("Export Wizard")
    self.setFixedWidth(400)
    self.threader = None
    
    #radio buttons area
    button_layout = QHBoxLayout()
    type_box = QGroupBox("Choose Export Type: ", self)
    button_group = QButtonGroup(self)
    button_group.setExclusive(True)
    
    byArticle = QRadioButton("By Article", self)
    byArticle.setChecked(True)
    byArticle.clicked.connect(self.article_choice)
    
    byMonth = QRadioButton("By Month", self)
    byMonth.clicked.connect(self.month_choice1)
    
    button_group.addButton(byArticle)
    button_group.addButton(byMonth)
    button_layout.addWidget(byArticle)
    button_layout.addWidget(byMonth)
    type_box.setLayout(button_layout)
    
    #textbox to show article
    self.article_title = QTextEdit(self)
    self.article_title.setFixedHeight(25)
    self.article_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    #set current article
    if(self.home_obj.choices_box.currentItem() != None):
      self.article_title.setText(self.home_obj.choices_box.currentItem().text())
    self.article_title.setReadOnly(True)
    
    #combobox for months (if enabled) and years
    combo_area = QHBoxLayout()
    self.combo_month = QComboBox(self)
    self.combo_month.activated.connect(self.month_choice)
    self.combo_month.setDisabled(True)
    
    self.combo_year = QComboBox(self)
    self.combo_year.activated.connect(self.year_choice)
    self.combo_year.setDisabled(True)
    
    combo_area.addWidget(self.combo_month)
    combo_area.addWidget(self.combo_year)
    
    #progress bar area
    self.progress_bar = QProgressBar(self)
    self.progress_bar.setMaximum(100)
    self.progress_bar.setMinimum(0)
    self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    self.progress_bar.setAlignment(Qt.AlignCenter)
    self.progress_bar.setFormat("%p")

    #status area
    statH = QHBoxLayout()
    self.statusLabel = QLabel("Status: ", self)
    self.statusLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    self.status_holder = QLabel("", self)
    self.status_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    statH.addWidget(self.statusLabel)
    statH.addWidget(self.status_holder)
    
    self.export_btn = QPushButton("Export", self)
    self.export_btn.clicked.connect(self.export)
    
    MainLayout.addWidget(type_box, 0,0)
    MainLayout.addWidget(self.article_title,1,0)
    MainLayout.addLayout(combo_area, 2,0)
    MainLayout.addWidget(self.progress_bar, 3,0)
    MainLayout.addLayout(statH, 4,0)
    MainLayout.addWidget(self.export_btn, 5,0)
    
    self.setLayout(MainLayout)
  
  def closeEvent(self, event):
    #print("Stuff was destroyed")
    if(self.threader != None):
      self.threader.quit()
      self.threader = None
      self.status_holder.setText("")
    event.accept()
  
  def article_choice(self):
    self.type = "Article"
    self.combo_month.setDisabled(True)
    self.combo_year.setDisabled(True)
    self.combo_year.clear()
    self.combo_month.clear()
    self.threader = None
    self.status_holder.setText("")
  
  def month_choice1(self):
    self.type = "Month"
    self.combo_month.setDisabled(False)
    self.combo_year.setDisabled(False)
    
    self.export_btn.setDisabled(False)
    
    current_year = time.localtime().tm_year
    for i in range(1,13):
      self.combo_month.addItem(self.dateUtil.num_to_monthStr(i))
    
    for b in range(self.subtract_from_year+1):
      self.combo_year.addItem(str(current_year-b))
    
    self.status_holder.setText("")
    
  def month_choice(self, index):
    pass
  
  def year_choice(self, index):
    pass
  
  def progress_update(self, val):
    self.progress_bar.setValue(val)
  
  def progress_max(self, val):
    self.progress_bar.setMaximum(val)
  
  def clear_thread(self):
    self.threader = None
    self.status_holder.setText("Completed Download")
    
  def export(self):
    if(self.threader == None):
      if(self.type == "Month"):
        self.progress_bar.setValue(0)
        self.status_holder.setText("Downloading...")
        
        #self.cleaner.export_by_month(month, year, page_obj)
        year = int(self.combo_year.currentText())
        month = self.combo_month.currentText()
        
        self.threader = Threader(self.type, month, year, self.home_obj.webUrl_holder.text())
        self.threader.start()
        
        self.threader.max1.connect(self.progress_max)
        self.threader.progress.connect(self.progress_update)
        
        self.threader.finished.connect(self.clear_thread)
        #thread = Thread(target=self.cleaner.export_by_month, args=(month, year, self.progress_bar,))
        #thread.start()
        #self.cleaner.export_by_month(month, year, self)
      else:
        item = self.home_obj.current_item_holder.text()
        if(item != "" and item != None):
          self.progress_bar.setValue(0)
          self.status_holder.setText("Downloading...")
          
          full_date = self.home_obj.date_holder.text().split("-")
          
          year = int(full_date[0])
          month = full_date[1]
          
          self.threader = Threader(self.type, url=self.home_obj.webUrl_holder.text(), title=item, month=month, year=year)
          self.threader.start()
          
          self.threader.max1.connect(self.progress_max)
          self.threader.progress.connect(self.progress_update)
          
          self.threader.finished.connect(self.clear_thread)
        else:
          self.status_holder.setText("Please choose an article first")