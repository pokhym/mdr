import logging

from handler_mangadex import *
from constants import *

def test_chapter_download():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangadex.org/title/879af0bb-ce30-47e4-a74e-cd1ce874c6e3/isekai-nonbiri-nouka")
  
  mh.extract_metadata()
  
  mh.start_driver()
  mh.init_for_chapter("216", "https://mangadex.org/chapter/d1d38099-b7a4-459b-ad4c-729bd74c55f9")
  mh.extract_chapter_images()
  mh.reset_for_next_chapter()
  mh.terminate_driver()

def test_comicinfo_and_zip():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangadex.org/title/879af0bb-ce30-47e4-a74e-cd1ce874c6e3/isekai-nonbiri-nouka")

  mh.extract_metadata()
  
  mh.start_driver()
  mh.init_for_chapter("216", "https://mangadex.org/chapter/d1d38099-b7a4-459b-ad4c-729bd74c55f9")
  mh.extract_chapter_images()
  mh.create_comic_info()
  mh.create_cbz()
  mh.reset_for_next_chapter()
  mh.terminate_driver()

def test_title_metadata():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/879af0bb-ce30-47e4-a74e-cd1ce874c6e3/isekai-nonbiri-nouka")

  mh.extract_metadata()

  mh.metadata.dump()

def test_title_metadata2():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/ffe69cc2-3f9e-4eab-a7f7-c963cea9ec25/hitoribocchi-no-isekai-kouryaku")

  mh.extract_metadata()

  mh.metadata.dump()

def test_language_selection():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()
  mh.start_driver()
  mh.init_for_title("test/", "https://mangadex.org/title/879af0bb-ce30-47e4-a74e-cd1ce874c6e3/isekai-nonbiri-nouka")
  mh.select_chapter_language()
  mh.terminate_driver()

def test_full():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangadex.org/title/6af5379f-ace2-453f-a9dd-94f7c443937a/shinozaki-himeno-s-love-q-a")
  
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
  
  test_chapter_download()
