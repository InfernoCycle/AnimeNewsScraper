from bs4 import BeautifulSoup
import time
import datetime
import json
import requests
import os
import re
import random
from utils.month_convert import DateUtil
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget

class CCreate():
  def exist_create(self, file, create=False, dir="v2", with_json=False):
    if(os.path.exists(dir+"/"+file)):
      return True
    else:
      if(create):
        with open(dir+"/"+file, "w+") as fs:
          if(not with_json):
            return True #if create is true then return is true
          else:
            fs.write('{"main":{}}')
            return True
      else:
        return False
  
  def write_json(self, file, data:dict):
    if(os.path.exists(file) and os.path.isfile(file)):
      with open(file, "w+", encoding="utf-8") as fs:
        fs.seek(0)
        json.dump(data, fs)

class CCheck():
  def in_json(self, is_file, file:str="", key:str="", iterate=False, add_json=False, data=None):
    if(not is_file):
      try:
        if key == "main":
          return True
          
        key_s = data.keys()
        
        for i in key_s:
          if i == key:
            return True
        else:
          data[key]
          return True
        
      except KeyError:
        return False
            
    if(is_file):
      if(os.path.exists(file) and os.path.isfile(file)):
        with open(file, "r+") as fs:
          if(add_json):
              try:
                original = json.load(fs)
                original[key] = data
                #fs.truncate(0)
                fs.seek(0)
                json.dump(original, fs)
                return True
              except Exception as e:
                return False
              
          try:
            obj = json.load(fs)
            
            if(iterate):
              if key == "main":
                return True
              
              key_s = obj["main"].keys()
              for i in key_s:
                if i == key:
                  return True
            else:
              obj[key]
              return True
          except KeyError as e:
            return False
          
          return False
  
  def read_json(self, file):
    f = open(file, "r")
    j = json.load(f)
    f.close()
    return j

class Cleaner():
  def __init__(self):
    super().__init__()
    self.BUrl = "https://www.animenewsnetwork.com"
  
  def rsplit(self,old, replace ,amount=1):
    reverse = old[::-1].replace(replace, "", amount)
    newReverse = reverse[::-1]
    
    return newReverse

  def getInfo(self, date="", url=None, save_to="", include_par=True, include_url=False):
    title = ""
    intro = ""
    video = ""
    image = ""
    paragraph = ""
    
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "lxml")
    
    #get title
    title = ""
    try:
        title = soup.select("#page_header")[0].get_text().replace("News", "").replace("\n", "").strip()
        #print(title)
    except IndexError:
        print("D"*50)
        title = ""
        #await queue.put(url)
        return
    
    repeat = 0
    
    #getDatePosted
    date = ""
    try:
        date = soup.select("small > time")[0]
        formatted = self.rsplit(str(date.attrs["datetime"]), ":", 1)
        
        fullFunctions = datetime.datetime.strptime(formatted, "%Y-%m-%dT%H:%M:%S%z")
        date = str(fullFunctions.date()).strip().replace("\n", "")
    except IndexError:
        date=""
        print("No Time")
    
    #get intro
    intro = ""
    try:
        intro = soup.find("div", attrs={"class":"intro"}).text
    except AttributeError:
        intro = "None"

    #get videos if any
    videoisNone = soup.select("iframe[title='YouTube video player']")
    video = ""
    if(len(videoisNone) > 0):
        video = soup.select("iframe[title='YouTube video player']")[0]["src"]

    #get images if any within the meat section
    imageisNone = soup.select(".meat > figure > img")
    image = ""
    if(len(imageisNone) > 0):
        image = "https://cdn.animenewsnetwork.com" + soup.select(".meat > figure > img")[0]["data-src"]
    
    #get paragraph if any within the meat section
    paragraph = ""
    if(include_par):
        paragraph = soup.find("div", attrs={"class":"meat"}).get_text().strip().replace("\n\n\n\n", "\n\n")
    
    if(not include_url):
      return {"Title":title, "Note": intro.replace("\n", ""), "Video":video, "Image":image, "Date":date, "Paragraph":paragraph}
    else:
      return {"Title":title, "Note": intro.replace("\n", ""), "Video":video, "Image":image, "Date":date, "Paragraph":paragraph, "Url":url}
    #print("Title: " + title + "\nNote: " + intro.replace("\n", "") + "\n" + video + "\n" + image + "\n" + f"URL: {url}\n" + "Date: " + date + "\n\n" + paragraph + "\n\n" + "-"*200 + "\n"*3)
  
  def export_by_article(self, url):
    time.sleep(3)
    print("this ran")
    return
    with open("", "r+") as file:
      pass
    
  def export_by_month(self, month:str, year, progress_bar):
    local_time = time.localtime(time.time())
    url = requests.get("https://www.animenewsnetwork.com/news/archive")
    soup = BeautifulSoup(url.text, "lxml")
    Months = soup.find_all(string=[re.compile("(March|April|May|February|January|June|July|August|September|October|November|December) "+ str(year))])
    
    urls = []
    date_util = DateUtil()
    for element in Months:
      try:
        full_url = str(self.BUrl + element.parent.parent["href"])
        searched = re.search("\/\d+#",full_url)
        if(searched != None):
          url_month = date_util.num_to_monthStr(searched.group().replace("/","").replace("#",""), True, True)
          if(month.lower() == url_month):
            with open(f"{month}_{year}_animeNews.txt", "ab") as file:
              article_urls = requests.get(full_url)
              soupAll = BeautifulSoup(article_urls.text, "lxml")
              articles = soupAll.select(".article-list>li>a")
              
              total_articles = len(articles)
              print(total_articles)
              #progress_bar.emit(SIGNAL("pMax"), total_articles)
              progress_bar.setMaximum(total_articles)
              count = 0
              for article_link in articles:
                virtual_obj = self.getInfo(url=self.BUrl + article_link.attrs["href"], include_url=True)
                print(virtual_obj["Title"])
                file.write(str("Title: " + virtual_obj["Title"] + "\nNote: " + virtual_obj["Note"] + 
                           "\n" + virtual_obj["Video"] + "\n" + virtual_obj["Image"] + "\n" + 
                           f"URL: {virtual_obj['Url']}\n" + "Date: " + virtual_obj["Date"] + 
                           "\n\n" + virtual_obj["Paragraph"] + 
                           "\n\n" + "-"*200 + "\n"*3).encode("utf-8"))
                count+=1
                #progress_bar.emit(SIGNAL("pUpdate"), count)
                progress_bar.setValue(count)
                time.sleep(5)
          #urls.append(self.BUrl + element.parent.parent["href"])
      except KeyError:
          continue
        
    return
    with open(f"{month}_{year}_animeNews", "r+") as file:
      for i in urls:
        first = re.search("\/\d+#", i)
        month_to_ = date_util.num_to_monthStr(first.group().replace("/", ""), True, True) + "_" + str(year)
        
        if(month == month_to_):
          stuff = requests.get(i)
          soupAll = BeautifulSoup(stuff.text, "lxml")
          articles = soupAll.select(".article-list>li>a")
          
          total_articles = len(articles)
          
          for article_link in articles:
            pass

class Threader(QThread):
  progress = Signal(int)
  max1 = Signal(int)
  
  def __init__(self, type1:str, month:str="", year=0, url="", title=""):
    super().__init__()
    self.month = month
    self.year = year
    self.url = url
    self.type1 = type1
    self.BUrl = "https://www.animenewsnetwork.com"
    self.cleaner = Cleaner()
    self.title = title
    
  def run(self):
    if(self.type1 == "Month"):
      self.export_by_month()
    else:
      self.export_by_article()
  
  def export_by_article(self):
    stringify = ""
    for i in range(5):
      stringify+=str(random.randint(0,9))
      
      self.max1.emit(1)
      
    with open(f"article_{self.year}_{self.month}_{stringify}.txt", "wb") as file:
      virtual_obj = self.cleaner.getInfo(url=self.url, include_url=True)
      file.write(str("Title: " + virtual_obj["Title"] + "\nNote: " + virtual_obj["Note"] + 
                           "\n" + virtual_obj["Video"] + "\n" + virtual_obj["Image"] + "\n" + 
                           f"URL: {virtual_obj['Url']}\n" + "Date: " + virtual_obj["Date"] + 
                           "\n\n" + virtual_obj["Paragraph"] + 
                           "\n\n" + "-"*200 + "\n"*3).encode("utf-8"))
    self.progress.emit(1)
    
  def export_by_month(self):
    local_time = time.localtime(time.time())
    url = requests.get("https://www.animenewsnetwork.com/news/archive")
    soup = BeautifulSoup(url.text, "lxml")
    Months = soup.find_all(string=[re.compile("(March|April|May|February|January|June|July|August|September|October|November|December) "+ str(self.year))])
    
    urls = []
    date_util = DateUtil()
    stringify = ""
    for i in range(5):
      stringify+=str(random.randint(0,9))
      
    for element in Months:
      try:
        full_url = str(self.BUrl + element.parent.parent["href"])
        searched = re.search("\/\d+#",full_url)
        if(searched != None):
          url_month = date_util.num_to_monthStr(searched.group().replace("/","").replace("#",""), True, True)
          if(self.month.lower() == url_month):
            with open(f"{self.month}_{self.year}_animeNews_{stringify}.txt", "ab") as file:
              article_urls = requests.get(full_url)
              soupAll = BeautifulSoup(article_urls.text, "lxml")
              articles = soupAll.select(".article-list>li>a")
              
              total_articles = len(articles)
              #print(total_articles)
              
              self.max1.emit(total_articles)
              #self.progress_bar.setMaximum(total_articles)
              count = 0
              for article_link in articles:
                virtual_obj = self.cleaner.getInfo(url=self.BUrl + article_link.attrs["href"], include_url=True)
                #print(virtual_obj["Title"])
                file.write(str("Title: " + virtual_obj["Title"] + "\nNote: " + virtual_obj["Note"] + 
                           "\n" + virtual_obj["Video"] + "\n" + virtual_obj["Image"] + "\n" + 
                           f"URL: {virtual_obj['Url']}\n" + "Date: " + virtual_obj["Date"] + 
                           "\n\n" + virtual_obj["Paragraph"] + 
                           "\n\n" + "-"*200 + "\n"*3).encode("utf-8"))
                count+=1
                self.progress.emit(count)
                #self.progress_bar.setValue(count)
                time.sleep(5)
          #urls.append(self.BUrl + element.parent.parent["href"])
      except KeyError:
          continue
        
    return