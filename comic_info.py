from xml.dom import minidom

class ComicInfo():

  def __init__(self):
    """
    """
    self.root = minidom.Document()

if __name__ == "__main__":
  ci = ComicInfo()