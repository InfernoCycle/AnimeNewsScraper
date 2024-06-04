class DateUtil():
  def __init__(self):
    self.month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    self.num = [1,2,3,4,5,6,7,8,9,10,11,12]
    self.days = [i for i in range(32)]
  
  def day_to_two(self, num, isString=False):
    if(isString):
      if(len(num) > 1):
        return num
      else:
        return "0"+num
    
    else:
      if(len(str(num)) > 1):
        return str(num)
      else:
        return "0"+str(num)
  
  def num_to_monthStr(self, num, isString=False, toLower=False):
    if(isString):
      if(len(num) > 1):
        if(str(num[0]) == "0"):
          if(toLower):
            return self.month[int(num[1])-1].lower()
          else:
            return self.month[int(num[1])-1]
        else:
          if(toLower):
            return self.month[int(num)-1].lower()
          else:
            return self.month[int(num)-1]
      else:
        if(toLower):
          return self.month[int(num)-1].lower()
        else:
          return self.month[int(num)-1]
    else:
      if(toLower):
        return self.month[num-1].lower()
      else:
        return self.month[num-1]
  
  #setting 'two_digits' to True returns string
  def monthStr_to_num(self, month:str, two_digits = False):
    index = 0
    for i in self.month:
      index+=1
      if(i == month.lower()):
        if(two_digits):
          if(index-1 < 10):
            return "0" + str(index)
          else:
            return index
          
        return index