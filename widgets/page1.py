from PySide6.QtWidgets import QListWidget, QTabWidget, QTextEdit, QCalendarWidget, QMessageBox, QFileDialog, QStatusBar, QMenu, QMainWindow, QComboBox, QTabWidget, QAbstractItemView, QListWidgetItem, QListWidget, QSizePolicy, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout
from PySide6.QtCore import QUrl, QDate, Qt
from PySide6.QtGui import QIcon, QImage, QPixmap, QFont, QGuiApplication
from utils.scrape import Scrape
from utils.month_convert import DateUtil
from utils.signals import CopyPlate
from utils.fImage import FIL

class Home(QWidget):
  def __init__(self):
    super().__init__()
    self.scraper = Scrape()
    self.dateUtil = DateUtil()
    self.imageUtil = FIL()
    self.clipboard = QGuiApplication.clipboard()
    self.act = CopyPlate(self.clipboard, self)
    
    self.tabs = QTabWidget(self)
    information_layout = QGridLayout()
    
    self.day = 1
    self.year = 2000
    self.month = 1
    self.info_height = 70
    
    MainLayout = QGridLayout(self)

    Title = QLabel("Inferno Anime News Scraper")
    Title.setAlignment(Qt.AlignCenter)
    Title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    font = QFont("Times New Roman", 40, 3, True)
    Title.setFont(font)
    
    word_font = QFont("Arial", 12, 6, True)
  
    calendar = QCalendarWidget(self)
    calendar.setMaximumHeight(600)
    calendar.setMaximumWidth(800)
    
    calendar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    calendar.clicked.connect(self.get_date)

    vLayout = QVBoxLayout()
    choice_label = QLabel("Choose an Article: ", self)
    self.choices_box = QListWidget(self)
    self.choices_box.itemClicked.connect(self.chosen)
    
    vHLayout = QHBoxLayout()
    current_item_label = QLabel("Pick: ", self)
    current_item_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    self.current_item_holder = QLabel("", self)
    self.current_item_holder.setWordWrap(True)
    self.current_item_holder.setFont(word_font)
    vHLayout.addWidget(current_item_label)
    vHLayout.addWidget(self.current_item_holder)
    
    #Title
    tLayout = QHBoxLayout()
    self.title_label = QLabel("Title: ", self)
    self.title_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    self.title_holder = QLabel("N/A", self)
    self.title_holder.setWordWrap(True)
    self.title_holder.setFont(word_font)
    #self.title_holder.setMaximumHeight(50)
    self.title_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.cop_title = QPushButton("Copy", self)
    self.cop_title.clicked.connect(self.act.copy_title)
    tLayout.addWidget(self.title_label)
    tLayout.addWidget(self.title_holder)
    tLayout.addWidget(self.cop_title)
    
    #URL
    urlLayout = QHBoxLayout()
    self.webUrl_label = QLabel("URL: ", self)
    self.webUrl_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    self.webUrl_holder = QLabel("N/A", self)
    self.webUrl_holder.setWordWrap(True)
    self.webUrl_holder.setFont(word_font)
    #self.webUrl_holder.setMaximumHeight(50)
    self.webUrl_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.cop_url = QPushButton("Copy", self)
    self.cop_url.pressed.connect(self.act.copy_url)
    urlLayout.addWidget(self.webUrl_label)
    urlLayout.addWidget(self.webUrl_holder)
    urlLayout.addWidget(self.cop_url)
    
    #youtube_url
    ytLayout = QHBoxLayout()
    self.ytUrl_label = QLabel("YT URL: ", self)
    self.ytUrl_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    self.ytUrl_holder = QLabel("N/A", self)
    self.ytUrl_holder.setWordWrap(True)
    self.ytUrl_holder.setFont(word_font)
    #self.ytUrl_holder.setMaximumHeight(40)
    self.ytUrl_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.cop_yt = QPushButton("Copy", self)
    self.cop_yt.pressed.connect(self.act.copy_ytUrl)
    ytLayout.addWidget(self.ytUrl_label)
    ytLayout.addWidget(self.ytUrl_holder)
    ytLayout.addWidget(self.cop_yt)
    
    #Note 
    noteLayout = QHBoxLayout()
    self.note_label = QLabel("Note: ", self)
    self.note_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    self.note_holder = QLabel("N/A", self)
    self.note_holder.setWordWrap(True)
    self.note_holder.setFont(word_font)
    #self.note_holder.setMaximumHeight(50)
    self.note_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.cop_note = QPushButton("Copy", self)
    self.cop_note.pressed.connect(self.act.copy_note)
    noteLayout.addWidget(self.note_label)
    noteLayout.addWidget(self.note_holder)
    noteLayout.addWidget(self.cop_note)
    
    #Date
    dateLayout = QHBoxLayout()
    self.date_label = QLabel("Date: ", self)
    self.date_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    self.date_holder = QLabel("N/A", self)
    self.date_holder.setFont(word_font)
    #self.date_holder.setMaximumHeight(30)
    self.date_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.cop_date = QPushButton("Copy", self)
    self.cop_date.pressed.connect(self.act.copy_date)
    dateLayout.addWidget(self.date_label)
    dateLayout.addWidget(self.date_holder)
    dateLayout.addWidget(self.cop_date)
    
    #Image
    imgLayout = QHBoxLayout()
    self.img_label = QLabel(self)
    self.img_label.setFixedSize(300,600)
    imgLayout.addWidget(self.img_label)
    
    #Paragraph
    parLayout = QVBoxLayout()
    self.paragraph_holder = QTextEdit(self)
    #self.paragraph_holder.setMaximumHeight(300)
    self.paragraph_holder.setReadOnly(True)
    self.paragraph_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    parLayout.addWidget(self.paragraph_holder)
    
    MainLayout.addWidget(Title,0,0,1,2)
    vLayout.addWidget(choice_label)
    vLayout.addWidget(self.choices_box)
    vLayout.addLayout(vHLayout)
    
    #vLayout.addLayout(imgLayout)
    information_layout.addWidget(calendar, 1,0)
    information_layout.addLayout(vLayout, 1,1)
    
    information_widget = QWidget()
    information_widget.setLayout(information_layout)
    self.tabs.addTab(information_widget, "Pick")
    
    img_widget = QWidget()
    vImgLayout = QVBoxLayout()
    vImgLayout.addLayout(tLayout)
    vImgLayout.addLayout(dateLayout)
    vImgLayout.addLayout(urlLayout)
    vImgLayout.addLayout(ytLayout)
    vImgLayout.addLayout(noteLayout)
    imgLayout.addLayout(vImgLayout)
    img_widget.setLayout(imgLayout)
    self.tabs.addTab(img_widget, "Info")
    
    par_widget = QWidget()
    par_widget.setLayout(parLayout)
    self.tabs.addTab(par_widget, "Article")
    
    MainLayout.addWidget(self.tabs)
    self.setLayout(MainLayout)
    #MainLayout.addWidget(self.paragraph_holder, 2,0,1,2)
  
  #runs when a date is chosen on calendar
  def get_date(self, date:QDate):
    self.day = date.day()
    self.year = date.year()
    self.month = date.month()
    
    content = self.scraper.get_date_string(self.month, self.year)
    self.choices_box.clear()
    
    try:
      keys = self.scraper.urls_obj["main"][content][str(self.dateUtil.day_to_two(self.day))].keys()
      self.choices_box.addItems(keys)
      
    except KeyError:
      self.choices_box.clear()
  
  #runs when a choice is selected in the combobox
  def chosen(self, item):
    self.current_item_holder.setText(item.text())
    self.title_holder.setText(item.text())
    content = self.scraper.get_date_string(self.month, self.year)
    url = self.scraper.urls_obj["main"][content][str(self.dateUtil.day_to_two(self.day))][item.text()]
    self.webUrl_holder.setText(url)
    self.date_holder.setText("Loading...")
    self.ytUrl_holder.setText("Loading...")
    self.note_holder.setText("Loading...")
    #get paragraph, any yt vid link etc
    data = self.scraper.add_cache_data(self.dateUtil.num_to_monthStr(self.month, toLower=True), self.day, self.year, item.text(), url)

    date = data["Date"]
    yt_url = data["Video"]
    image = data["Image"]
    note = data["Note"]
    
    self.date_holder.setText(date)
    self.ytUrl_holder.setText(yt_url)
    self.note_holder.setText(note)
    
    picture = self.imageUtil.read_image_url(image)
    if(picture != None):
      pix = QPixmap()
      pix.loadFromData(picture)
      #pix.scaled(100, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
      self.img_label.setPixmap(pix)
    else:
      self.img_label.setPixmap(QPixmap())
      
    self.paragraph_holder.setReadOnly(False)
    self.paragraph_holder.setText(data["Paragraph"])
    self.paragraph_holder.setReadOnly(True)
    #print(self.imageUtil.read_image_url(image))
    #self.img_label.setStyleSheet(f"background-image:url({image});")
    
    #print(f"Date: {date}, YT_URL: {yt_url}, Image: {image}, Note: {note}")
    #self.choices_box.addItem()
  
  def copy_title(self, status):
    print("copy title")