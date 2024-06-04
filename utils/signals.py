class CopyPlate():
  def __init__(self, clipboard, page_obj):
    self.clipboard = clipboard
    self.page_obj = page_obj
    
  def copy_title(self, status):
    self.clipboard.setText(self.page_obj.title_holder.text())
  def copy_url(self):
    self.clipboard.setText(self.page_obj.webUrl_holder.text())
  def copy_ytUrl(self):
    self.clipboard.setText(self.page_obj.ytUrl_holder.text())
  def copy_date(self):
    self.clipboard.setText(self.page_obj.date_holder.text())
  def copy_note(self):
    self.clipboard.setText(self.page_obj.note_holder.text())
  def copy_paragraph(self):
    self.clipboard.setText(self.page_obj.paragraph_holder.text())