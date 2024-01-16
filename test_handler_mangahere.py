import logging
from constants import *
from handler_mangahere import HandlerMangaHere

def test_extract_metadata():
  mh = HandlerMangaHere(0, SOURCE_MANGAHERE)
  mh.init_for_title("test/", "https://mangahere.cc/manga/spy_x_family/")
  mh.extract_metadata()

  mh.metadata.dump(log=True)

def test_page_count():
  mh = HandlerMangaHere(0, SOURCE_MANGAHERE)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangahere.cc/manga/spy_x_family/")
  
  mh.extract_metadata()

  mh.start_driver()
  mh.init_for_chapter("001", "https://mangahere.cc/manga/spy_x_family/c001/1.html")
  curr_page = mh.extract_current_page()
  assert(curr_page == 1)
  num_pages = mh.extract_total_pages()
  assert(num_pages == 72)
  mh.terminate_driver()

def test_chapter_download():
  mh = HandlerMangaHere(0, SOURCE_MANGAHERE)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangahere.cc/manga/spy_x_family/")
  
  mh.extract_metadata()

  mh.start_driver()
  mh.init_for_chapter("001", "https://mangahere.cc/manga/spy_x_family/c001/1.html")
  mh.extract_chapter_images()
  mh.reset_for_next_chapter()
  mh.terminate_driver()

def test_full_download():
  """
  TODO:

  https://mangahere.cc/manga/furoufushi_shoujo_no_naedoko_ryokouki/

  Requires additional clicking to get through age filter
  """

def test_full_download1():
  mh = HandlerMangaHere(0, SOURCE_MANGAHERE)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangahere.cc/manga/uchida_san_wa_zettai_ni_gyaru_janai/")
  
  mh.extract_metadata()

  mh.get_update()

if __name__ == "__main__":
  # Setup Logging
  logging.basicConfig(level=logging.INFO
                      , format="%(asctime)s;%(levelname)s;%(message)s"
                      , datefmt="%Y-%m-%d %H:%M:%S"
                      , filename="test_log.txt"
                      , filemode="w")
  # define a Handler which writes INFO messages or higher to the sys.stderr
  console = logging.StreamHandler()
  console.setLevel(logging.INFO)
  # set a format which is simpler for console use
  formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
  # tell the handler to use this format
  console.setFormatter(formatter)
  # add the handler to the root logger
  logging.getLogger().addHandler(console)

  test_full_download1()