import logging

class TitleMetadata():
  def __init__(self):
    """
    title: str
      Title
    description: str
      Description
    categories: Set[str]
      Categories
    chapter_numbers: List[str]
      Chapter numbers, uses a list because
      we care about the order they appear on the site
      rather than simple sorting
    """
    self.title = None
    self.description = None
    self.categories = set()
    self.chapter_numbers = []
  
  def set_title(self, title):
    self.title = title
  
  def set_description(self, description):
    self.description = description
  
  def add_category(self, category):
    self.categories.add(category.lower())
  
  def add_chapter_number(self, chapter_number):
    self.chapter_numbers.append(chapter_number)
  
  def dump(self):
    logging.info("Title: " + str(self.title))
    logging.info("==========")
    
    logging.info("Description: " + str(self.description))
    logging.info("==========")

    categories_str = ""
    for c in sorted(list(self.categories)):
      categories_str += "\t" + c + "\n"
    logging.info("Categories:\n" + categories_str)
    logging.info("==========")

    chapters_str = ""
    for c in self.chapter_numbers:
      chapters_str += "\t" + c + "\n"
    logging.info("Chapter Numbers:\n" + chapters_str)
    
