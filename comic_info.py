from xml.dom import minidom

class ComicInfo():

  def __init__(self):
    """
    """
    self.first_genre = True
    self.root = minidom.Document()
    self.ci_element = self.root.createElement("ComicInfo")
    self.ci_element.setAttribute("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    self.ci_element.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    self.root.appendChild(self.ci_element)
    self.genre_element = None

  def add_title(self, title):
    title_element = self.root.createElement("Title")
    self.ci_element.appendChild(title_element)
    title_text = self.root.createTextNode(title)
    title_element.appendChild(title_text)
  
  def add_series(self, series):
    series_element = self.root.createElement("Series")
    self.ci_element.appendChild(series_element)
    series_text = self.root.createTextNode(series)
    series_element.appendChild(series_text)

  def add_web(self, url):
    web_element = self.root.createElement("Web")
    self.ci_element.appendChild(web_element)
    web_text = self.root.createTextNode(url)
    web_element.appendChild(web_text)
  
  def add_summary(self, summary):
    summary_element = self.root.createElement("Summary")
    self.ci_element.appendChild(summary_element)
    summary_text = self.root.createTextNode(summary)
    summary_element.appendChild(summary_text)
  
  def add_genre(self, genre):
    if self.first_genre:
      genre_element = self.root.createElement("Genre")
      self.ci_element.appendChild(genre_element)
      self.genre_text = self.root.createTextNode(genre)
      genre_element.appendChild(self.genre_text)
      self.first_genre = False
    else:
      assert(self.genre_text != None)
      self.genre_text.data = self.genre_text.data + "," + genre

  def add_page_count(self, page_count):
    page_count_element = self.root.createElement("PageCount")
    self.ci_element.appendChild(page_count_element)
    page_count_text = self.root.createTextNode(page_count)
    page_count_element.appendChild(page_count_text)

  def add_all_info(self, title, series, web, summary, genres, page_count):
    self.add_title(title)
    self.add_series(series)
    self.add_web(web)
    self.add_summary(summary)
    for g in genres:
      self.add_genre(g)
    self.add_page_count(page_count)

  def write_out(self, path):
    with open(path, "w") as fd:
      fd.write(self.root.toprettyxml(indent="\t"))

if __name__ == "__main__":
  ci = ComicInfo()
  ci.add_all_info("test title", "test series", "https://test.com", "test summary", ["genre1", "genre2"], "5")
  ci.write_out("test.xml")