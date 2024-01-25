import logging

from handler_mangadex import *
from constants import *
from os.path import expanduser

import multiprocessing as mp

def download(tid):
  if tid == 0:
    mh = HandlerMangaDex(0, SOURCE_MANGADEX)
    mh.reset_for_next_title()
    
    mh.init_for_title("test/", "https://mangadex.org/title/879af0bb-ce30-47e4-a74e-cd1ce874c6e3/isekai-nonbiri-nouka")
    
    mh.extract_metadata()

    mh.start_driver()
    mh.init_for_chapter("216", "https://mangadex.org/chapter/d1d38099-b7a4-459b-ad4c-729bd74c55f9")
    mh.extract_chapter_images()
    mh.reset_for_next_chapter()
    mh.terminate_driver()
  elif tid == 1:
    mh = HandlerMangaDex(1, SOURCE_MANGADEX)
    mh.reset_for_next_title()
    
    mh.init_for_title("test/", "https://mangadex.org/title/ffe69cc2-3f9e-4eab-a7f7-c963cea9ec25/hitoribocchi-no-isekai-kouryaku")
    
    mh.extract_metadata()

    mh.start_driver()
    mh.init_for_chapter("216", "https://mangadex.org/chapter/207f85d5-06cd-4e01-ac3a-64c009bfad93")
    mh.extract_chapter_images()
    mh.reset_for_next_chapter()
    mh.terminate_driver()
  else:
    assert(0)

def test_mp():
  
  p = mp.Pool(2)
  p.map(download, [i for i in range(2)])

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

def test_title_metadata3():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/027df837-7a15-4893-9dc3-e2ae11b94717/2d5bcdb0-e2a3-4352-9043-2ab218bee11b")

  mh.extract_metadata()

  mh.metadata.dump()

def test_title_metadata4():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/076b3757-2050-4362-b0ad-52513ecefa3f")

  mh.extract_metadata()

  mh.metadata.dump(log=True)

def test_title_metadata5():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/0e009a58-6ebf-445b-8057-a1a69b8f8c7f/202cf5e2-44c9-4b4c-8c99-55f354f518fb")

  mh.extract_metadata()

  mh.metadata.dump(log=True)

def test_title_metadata6():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()

  mh.init_for_title(expanduser("test/"), "https://mangadex.org/title/12e28a8a-cbfe-4e12-bab8-b6fb0b9a59b4/09960d27-f0a4-42bc-9e2b-c77ac93eec2a")

  mh.extract_metadata()

  mh.metadata.dump(log=True)

def test_language_selection():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()
  mh.start_driver()
  mh.init_for_title("test/", "https://mangadex.org/title/879af0bb-ce30-47e4-a74e-cd1ce874c6e3/isekai-nonbiri-nouka")
  mh.select_chapter_language()
  mh.terminate_driver()

def test_language_selection1():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangadex.org/title/00b64b8f-cb7e-4322-9855-3669fe210ac7/766f76d8-316d-4174-aca1-971c00f830c3")
  
  mh.extract_metadata()

def test_full():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX, "test_missing.txt")
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangadex.org/title/6af5379f-ace2-453f-a9dd-94f7c443937a/shinozaki-himeno-s-love-q-a")
  
  mh.extract_metadata()

  mh.get_update()

def test_full1():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangadex.org/title/010abcb5-c705-4dcb-a51d-49b2c518b673/ea4a2fff-90fa-46f2-9d4e-ced50b02af52")
  
  mh.extract_metadata()

  mh.get_update()

def test_full2():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangadex.org/title/009c62ce-6064-4409-9949-4f00ba6d593c/cheat-skill-shisha-sosei-ga-kakusei-shite-inishie-no-maougun-wo-fukkatsu-sasete-shimaimashita")
  
  mh.extract_metadata()

  mh.get_update()

def test_full3():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()
  
  mh.init_for_title("test/", "https://mangadex.org/title/009c62ce-6064-4409-9949-4f00ba6d593c/daf63c4b-af64-47a3-8c0c-0363db7f0547")
  
  mh.extract_metadata()

  mh.get_update()

def test_full4():
  """
  webtoon test
  """
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/0b9dfda1-8255-46ff-90f5-f0980923a1b0/1e8f8b80-49a6-4ac4-84ee-20715aa49b45")

  mh.extract_metadata()

  mh.get_update()

def test_get_mangaupdates_link():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/0b9dfda1-8255-46ff-90f5-f0980923a1b0/1e8f8b80-49a6-4ac4-84ee-20715aa49b45")

  mh.extract_mangaupdates_url()

  logging.info("MangaUpdates URL: " + mh.current_title_manga_updates_base_url)

def test_get_mangaupdates_translated_chs():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX, "test_missing.txt")
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/0b9dfda1-8255-46ff-90f5-f0980923a1b0/1e8f8b80-49a6-4ac4-84ee-20715aa49b45")

  mh.extract_mangaupdates_url()

  logging.info("MangaUpdates URL: " + mh.current_title_manga_updates_base_url)

  mh.check_manga_updates_status()

def test_get_mangaupdates_translated_chs1():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX, "test_missing.txt")
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/6af5379f-ace2-453f-a9dd-94f7c443937a/shinozaki-himeno-s-love-q-a")

  mh.extract_mangaupdates_url()

  logging.info("MangaUpdates URL: " + mh.current_title_manga_updates_base_url)

  mh.check_manga_updates_status()

def test_get_mangaupdates_translated_chs2():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX)
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/10db587f-a232-485d-b4a8-68ee0cb15e3c/93ee0736-016a-42cf-bd09-7129280318f5")

  mh.extract_mangaupdates_url()

  logging.info("MangaUpdates URL: " + mh.current_title_manga_updates_base_url)

  mh.check_manga_updates_status()

  # mh.get_update()


def test_get_mangaupdates_translated_chs2():
  """
  Test 14c chapter
  """
  mh = HandlerMangaDex(0, SOURCE_MANGADEX, "test_missing.txt")
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/024af7a5-f8ad-4b67-b950-b1708f52b018/7875e964-5034-4fd9-aacd-0e65eb181db4")

  mh.extract_mangaupdates_url()

  logging.info("MangaUpdates URL: " + mh.current_title_manga_updates_base_url)

  mh.check_manga_updates_status()

def test_get_mangaupdates_translated_chs3():
  """
  MangaUpdates containts things like
    Extras
    20 (End)
  https://mangadex.org/title/051e6a66-7373-4583-98b6-b746153041e9/e9985bbe-ace2-4cc0-a56c-99cd25de0990

  TODO:
  """
  mh = HandlerMangaDex(0, SOURCE_MANGADEX, "test_missing.txt")
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/051e6a66-7373-4583-98b6-b746153041e9/e9985bbe-ace2-4cc0-a56c-99cd25de0990")

  mh.extract_mangaupdates_url()

  logging.info("MangaUpdates URL: " + mh.current_title_manga_updates_base_url)

  mh.check_manga_updates_status()

def test_get_mangaupdates_translated_chs4():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX, "test_missing.txt")
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/08ff391a-7991-4c43-8741-531d7d0b2165/e14c3d10-7cd3-481b-b602-e3b68b6084d2")

  mh.extract_mangaupdates_url()

  logging.info("MangaUpdates URL: " + mh.current_title_manga_updates_base_url)

  mh.check_manga_updates_status()

def test_mangaupdates_missing():
  mh = HandlerMangaDex(0, SOURCE_MANGADEX, "test_missing.txt")
  mh.reset_for_next_title()

  mh.init_for_title("test/", "https://mangadex.org/title/10227f74-9134-4262-b01d-8966bc149c4d/b7d1a6ea-fbb9-4fa5-a6a4-098320656f24")

  mh.extract_mangaupdates_url()

  logging.info("MangaUpdates URL: " + mh.current_title_manga_updates_base_url)

  mh.check_manga_updates_status()

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
  
  test_mangaupdates_missing()
