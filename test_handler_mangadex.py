import logging

from handler_mangadex import *
from constants import *

def test_chapter_download():
  mh = HandlerMangaDex(SOURCE_MANGADEX)
  mh.reset_for_next_title()
  mh.init_for_title("test/test_title")
  mh.init_for_chapter("216", "https://mangadex.org/chapter/d1d38099-b7a4-459b-ad4c-729bd74c55f9")
  mh.extract_chapter_images()
  mh.terminate_driver()

if __name__ == "__main__":
  # Setup Logging
  logging.basicConfig(level=logging.INFO)
  
  test_chapter_download()
  