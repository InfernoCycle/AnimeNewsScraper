from bs4 import BeautifulSoup
import requests
import os
import getpass
import re
import time
from utils.formatting import Cleaner, CCheck, CCreate
from utils.month_convert import DateUtil
import json
from multiprocessing import Process, Queue

cleaner = Cleaner()
check = CCheck()
create = CCreate()
date_util = DateUtil()

program = "InfernoNews"
username = getpass.getuser()
BUrl = "https://www.animenewsnetwork.com"
urls = list()
Month = list()
Articles = list()

data = {}

local_time = time.localtime(time.time())

program_dir = f"C:/Users/{username}/AppData/Local/{program}"
news_file = "5428_cache_1.json"
url_file = "url_cache1.json"
full_file_path = program_dir + "/" + news_file
full_url_path = program_dir + "/" + url_file

class Scrape():
  def __init__(self):
    self.urls_obj = None
    self.cache_obj = None
    self.creation()
    self.add_url_data()
  
  def get_date_string(self, month, year):
    return date_util.num_to_monthStr(month, False, True) + "_" + str(year)
  
  def creation(self):
    #create directory if don't exist
    if(not os.path.exists(program_dir)):
      os.makedirs(program_dir)
      
    #create url files if don't exist
    create.exist_create(url_file, True, dir=program_dir, with_json=True)

    #get url object
    self.urls_obj = check.read_json(full_url_path)

    #create cache file if don't exist
    create.exist_create(news_file, True, dir=program_dir, with_json=True)

    #get cache object
    self.cache_obj = check.read_json(full_file_path)

    if(os.path.exists(program_dir) and (os.path.isdir(program_dir))):
      print("Exists")
    else:
      os.makedirs(program_dir)
      print(f"Created Directory: C:/Users/{username}/AppData/Local/{program}")

  def add_url_data(self):
    url = requests.get("https://www.animenewsnetwork.com/news/archive")
    soup = BeautifulSoup(url.text, "lxml")
    Months = soup.find_all(string=[re.compile("(March|April|May|February|January|June|July|August|September|October|November|December) "+ str(local_time.tm_year))])

    for element in Months:
      split_month = element.split(" ")
      try:
        self.urls_obj["main"][split_month[0].lower()+"_"+split_month[1]]
      except KeyError:
        self.urls_obj["main"][split_month[0].lower()+"_"+split_month[1]] = {}
      try:
          urls.append(BUrl + element.parent.parent["href"])
      except KeyError:
          continue
    
    current_month = date_util.num_to_monthStr(local_time.tm_mon, toLower=True) + "_" + str(local_time.tm_year)
    month_1 = local_time.tm_mon
    
    #print(current_month)
    #assignment = figure out how to check for months for each month in the 'urls' variable
    
    for i in urls:
      first = re.search("\/\d+#", i)
      month_to_ = date_util.num_to_monthStr(first.group().replace("/", ""), True, True) + "_" + str(local_time.tm_year)
      
      if(month_to_ == current_month):
        stuff = requests.get(i)

        soupAll = BeautifulSoup(stuff.text, "lxml")
        articles = soupAll.select(".article-list>li>a")
        #tempStr = sess.url.__str__()
        #print(articles)
        #UNCOMMENTtime.sleep(5)
        
        #Month.append(re.sub(f"https://www.animenewsnetwork.com/news/{local_time.tm_year}/", "", tempStr))
        tempArticleName = []
        tempArticleUrls = []

        for i in articles:
            tempArticleName.append(i.get_text())
            tempArticleUrls.append(BUrl + i.attrs["href"])

        Articles.append((tempArticleName, tempArticleUrls))

    for i in range(len(Articles)):
      for k in range(len(Articles[i][0])):
        link = Articles[i][1][k]
        title = Articles[i][0][k]
        #url = Articles[0][1][0]

        date = re.search("\d+-\d+-\d+", link)
        if(date != None):
          date = date.group().replace("-", "_")

        split_date = date.split("_")

        year = split_date[0]
        month = split_date[1]
        day = split_date[2]

        key = date_util.num_to_monthStr(month, True, True)+"_"+year
        
        if(check.in_json(False, key=day, iterate=True, data=self.urls_obj["main"][key])):
          self.urls_obj["main"][key][day][title] = link
        else:
          self.urls_obj["main"][key][day] = {}
          self.urls_obj["main"][key][day][title] = link

    create.write_json(full_url_path, self.urls_obj)
    #insert the urls and title in date_obj

    #check if file exist, if not then create it

    #key has to be "main" when setting "use_json" as true
    #note this function only appends to "main" use "append_json" to append to further data
    """
    obj["main"]["january"] = False

    create.append_json(full_file_path, obj)

    print(check.read_json(full_file_path))

    print(check.in_json(full_file_path, "february", True))
    """
    #cleaner.getInfo(date, url, include_par=True)
    #UNCOMMENTkey = date_util.num_to_monthStr(month, True, True)+"_"+year

  
  
  #this only runs when a user chooses a date
  def add_cache_data(self, month:str, day, year:str, title, url:str):
    #figure out first and foremost if a record of this date exist in the cache
    month_key = month+"_"+str(year)
    try:
      self.cache_obj["main"][month_key][title]
    except KeyError: #if key doesn't exist then create and load up
      if(month_key in self.cache_obj["main"]):
        self.cache_obj["main"][month_key] = {title:cleaner.getInfo(url=url)}
        #print("added title")
      else:
        self.cache_obj["main"] = {month_key:{title:cleaner.getInfo(url=url)}}
        #print("added month_key and title")
    
    return self.cache_obj["main"][month_key][title]
    #return cleaner.getInfo(url=url)
    #cleaner.getInfo()