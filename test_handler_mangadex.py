import logging

from handler_mangadex import *
from constants import *

def test_chapter_download():
  mh = HandlerMangaDex(SOURCE_MANGADEX)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangadex.org/title/879af0bb-ce30-47e4-a74e-cd1ce874c6e3/isekai-nonbiri-nouka")
  
  mh.start_driver()
  mh.init_for_chapter("216", "https://mangadex.org/chapter/d1d38099-b7a4-459b-ad4c-729bd74c55f9")
  mh.extract_chapter_images()
  mh.reset_for_next_chapter()
  mh.terminate_driver()

def test_comicinfo():
  mh = HandlerMangaDex(SOURCE_MANGADEX)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangadex.org/title/879af0bb-ce30-47e4-a74e-cd1ce874c6e3/isekai-nonbiri-nouka")

  mh.extract_metadata()
  
  mh.start_driver()
  mh.init_for_chapter("216", "https://mangadex.org/chapter/d1d38099-b7a4-459b-ad4c-729bd74c55f9")
  mh.extract_chapter_images()
  mh.create_comic_info()
  mh.reset_for_next_chapter()
  mh.terminate_driver()

def test_title_metadata():
  mh = HandlerMangaDex(SOURCE_MANGADEX)
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/879af0bb-ce30-47e4-a74e-cd1ce874c6e3/isekai-nonbiri-nouka")

  mh.extract_metadata()

  mh.metadata.dump()

def test_language_selection():
  mh = HandlerMangaDex(SOURCE_MANGADEX)
  mh.reset_for_next_title()
  mh.start_driver()
  mh.init_for_title("test/", "https://mangadex.org/title/879af0bb-ce30-47e4-a74e-cd1ce874c6e3/isekai-nonbiri-nouka")
  mh.select_chapter_language()
  mh.terminate_driver()

def test_full():
  mh = HandlerMangaDex(SOURCE_MANGADEX)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangadex.org/title/6af5379f-ace2-453f-a9dd-94f7c443937a/shinozaki-himeno-s-love-q-a")
  
  mh.extract_metadata()

  mh.get_update()

if __name__ == "__main__":
  # Setup Logging
  logging.basicConfig(level=logging.INFO)
  
  test_comicinfo()
