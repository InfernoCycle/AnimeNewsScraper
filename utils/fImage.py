import requests
from PIL import Image
from io import BytesIO
class FIL():
  def __init__(self):
    pass
  
  def read_image_url(self, url):
    if(url != ''):
      img_data = requests.get(url)
      #image = Image.open()
      #image.close()
      #print(img_data.content)
      
      return img_data.content
      #return BytesIO(img_data.content)