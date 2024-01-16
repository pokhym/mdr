from title_metadata import TitleMetadata
from constants import *
from comic_info import ComicInfo
import utils, shutil

import logging
import time
from os.path import abspath, join as path_join, exists, isdir
from os import makedirs
import platform

from selenium import webdriver 
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys

class Handler:
  def __init__(self, tid, source_name):
    """
    Member Variables
    -----------------
    tid: int
      Thread id helps with identifying the Handler in the log
    source_name: str
      Name of the source defined as SOURCE_XX in constants.py
    metadata: TitleMetadata
      Store metadata about this title
    downloaded_blobs_set: Set[str]
      Set of downloaded blob links for the currently being handled chapter
    download_title_abs_base_path: Union[None, str]
      Absolute base path
    download_chapter_rel_base_path: Union[None, str]
      Relative base path to the current chapter download
    current_title_base_url: Union[None, str]
      Base URL of the title
    current_chapter_base_url: Union[None, str]
      Base URL of the chapter
    current_download_image_number: int
      A number representing the page number currently being downloaded
    driver:
      Firefox driver from Selenium
    """
    self.tid = tid
    self.source_name = source_name
    self.metadata = TitleMetadata()
    self.downloaded_blobs_set = set()
    self.download_title_abs_base_path = None
    self.download_chapter_rel_base_path = None
    self.current_title_base_url = None
    self.current_chapter_base_url = None
    self.current_download_image_number = 1

    self.driver = None

  def get_tid(self):
    """
    Returns the thread id as "tidX" as a str
    """
    return "tid" + str(self.tid)
  
  def save_screenshot(self):
    self.driver.get_screenshot_as_file(self.get_tid + ".png")

  def start_driver(self):
    """
    Creates a new driver
    """
    logging.info("[" + self.get_tid() + " start_driver]: Starting " + self.source_name + " driver")

    # Initialize selenium
    # Define the Chrome webdriver options
    options = webdriver.FirefoxOptions()
    # options.binary_location = r'/usr/bin/firefox' 
    options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability
    options.add_argument("--enable-javascript")

    if platform.system() == "Windows":
      options.binary_location = FIREFOX_BIN_PATH
    else:
      assert(platform.system() == "Linux")

    # By default, Selenium waits for all resources to download before taking actions.
    # However, we don't need it as the page is populated with dynamically generated JavaScript code.
    options.page_load_strategy = "none"

    geckodriver_path = GECKO_BIN_PATH  # specify the path to your geckodriver
    driver_service = Service(executable_path=geckodriver_path)

    # Pass the defined options objects to initialize the web driver 
    self.driver = Firefox(options=options, service=driver_service) 
    # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
    self.driver.implicitly_wait(SLEEP_SEC)
    
    self.driver.set_window_size(1920, 1080)

  def terminate_driver(self):
    """
    Terminates the Selenium driver
    """
    logging.info("[" + self.get_tid() + " terminate_driver]: Terminating " + self.source_name + " driver")
    self.driver.close()
    self.driver = None
  
  def reset_for_next_title(self):
    """
    Resets all member variables for handling the next title
    """
    self.downloaded_blobs_set.clear()
    self.download_title_abs_base_path = None
    self.download_chapter_rel_base_path = None
    self.current_title_base_url = None
    self.current_chapter_base_url = None
    self.current_download_image_number = 1

  def init_for_title(self, title_abs_base_path, title_base_url):
    """
    Initialize member variables for title and creates folders
    """
    assert(self.driver == None)
    self.start_driver()

    # Load the URL
    logging.info("[" + self.get_tid() + " init_for_title]: Loading title url: " + title_base_url)
    self.current_title_base_url = title_base_url
    self.driver.get(self.current_title_base_url)
    time.sleep(SLEEP_SEC)

    # Obtain the title
    self.extract_title_name()

    # Join the base path with the name of the manga
    self.download_title_abs_base_path = abspath(title_abs_base_path)
    self.download_title_abs_base_path = path_join(self.download_title_abs_base_path, self.metadata.get_title())
    
    if not exists(self.download_title_abs_base_path):
      logging.info("[" + self.get_tid() + " init_for_title]: Creating base title folder at: " + self.download_title_abs_base_path)
      try:
        makedirs(self.download_title_abs_base_path)
      except Exception as e:
        self.save_screenshot()
        raise Exception("Unable to create base title folder at: " + self.download_title_abs_base_path)
    else:
      assert(exists(self.download_title_abs_base_path))
      assert(isdir(self.download_title_abs_base_path))
      logging.info("[" + self.get_tid() + " init_for_title]: Base title folder exists at: " + self.download_title_abs_base_path)
    
    # logging.info("[" + self.get_tid() + " init_for_title]: Loading title url: " + title_base_url)
    self.current_title_base_url = title_base_url
    self.driver.get(self.current_title_base_url)
    time.sleep(SLEEP_SEC)

    self.terminate_driver()

  def reset_for_next_chapter(self):
    """
    Resets all member variables for handling the
    next chapter and creates folders
    """
    self.downloaded_blobs_set.clear()
    self.download_chapter_rel_base_path = None
    self.current_chapter_base_url = None
    self.current_download_image_number = 1

  def init_for_chapter(self, chapter_base_rel_path, chapter_url):
    """
    Initialize member variables for chapter
    """
    self.download_chapter_rel_base_path = chapter_base_rel_path
    self.current_chapter_base_url = chapter_url

    joined_path = path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path)
    if not exists(joined_path):
      logging.info("[" + self.get_tid() + " init_for_chapter]: Creating chapter folder at: " + joined_path)
      try:
        makedirs(joined_path)
      except Exception as e:
        self.save_screenshot()
        raise Exception("Unable to create chapter folder at: " + joined_path)
    else:
      assert(exists(joined_path))
      assert(isdir(joined_path))
      logging.info("[" + self.get_tid() + " init_for_chapter]: Chapter folder exists at: " + joined_path)
    
    self.current_chapter_base_url = chapter_url
    self.driver.get(self.current_chapter_base_url)
    time.sleep(SLEEP_SEC)

    logging.info("[" + self.get_tid() + " init_for_chapter]: (Title: " + self.metadata.get_title() + ", Chapter: " + self.download_chapter_rel_base_path + ") Loading chapter url: " + chapter_url)

  def extract_current_page(self):
    """
    Gets the current page number

    Implemented for:
      - MangaDex

    Returns
    -------------------
    current_chapter_page: int
    """
    pass

  def extract_total_pages(self):
    """
    Gets the total number of pages in a chapter

    Implemented for:
      - MangaDex

    Returns
    --------------------
    total_chapter_pages: int
    """

  def extract_single_page(self):
    """
    Downloads a single page's image

    Implemented for:
      - MangaDex
    """
    pass

  def extract_chapter_images(self):
    """
    Downloads a full chapter

    Implemented for:
      - MangaDex
    """
    pass

  def create_comic_info(self):
    """
    Creates and saves a ComicInfo.xml
    """
    logging.info("[" + self.get_tid() + " create_comic_info]: Creating ComicInfo.xml...")
    ci = ComicInfo()
    ci.add_all_info(
      title=self.download_chapter_rel_base_path,
      series=self.metadata.get_title(),
      web=self.current_chapter_base_url,
      summary=self.metadata.get_description(),
      genres=self.metadata.get_categories(),
      page_count=str(self.current_download_image_number)
    )
    ci.write_out(path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path, "ComicInfo.xml"))

  def create_cbz(self):
    """
    Zips the currently operating folder and creates
    a cbz in its place then deletes the chapter folder
    """
    logging.info("[" + self.get_tid() + " create_cbz]: Creating cbz for: " + path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path))
    utils.zip_folder_into_cbz(path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path))
    assert(exists(path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path + ".cbz")))
    logging.info("[" + self.get_tid() + " create_cbz]: Removing folder: " + path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path))
    shutil.rmtree(path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path))

  def extract_title_name(self):
    """
    Obtain the title name

    Implemented for:
      - MangaDex
    """
    pass

  def extract_title_url(self):
    """
    Set the title url
    """
    self.metadata.set_title_url(self.current_title_base_url)

  def extract_description(self):
    """
    Obtain the description

    Implemented for:
      - MangaDex
    """
    pass

  def extract_categories(self):
    """
    Returns the categories for the current title

    Implemented for:
      - MangaDex
    """
    pass

  def extract_chapter_numbers(self):
    """
    Returns the chapter numbers (and titles) of
    the current title

    Implemented for:
      - MangaDex
    """
    pass

  def extract_cover(self):
    """
    Get the cover image and save it to the
    base directory as cover.jpg

    Implemented for:
      - MangaDex
    """
    pass

  def save_metadata(self):
    """
    Saves metadata to file in the base directory
    """
    joined = path_join(self.download_title_abs_base_path, METADATA_FILE_NAME)
    with open(joined, "w") as fd:
      fd.write(self.metadata.dump())
      fd.close()
  
  def extract_metadata(self):
    """
    Obtains metadata for the title.
    Implementation should wrap other metadata extraction
    functions

    Implemented for:
      - MangaDex
    """
    self.extract_title_name()
    self.extract_title_url()
    self.extract_description()
    self.extract_categories()
    self.extract_chapter_numbers()
    self.extract_cover()
    self.save_metadata()

  def is_url_valid_source(self, url):
    """
    Checks if the URL is actually from the accepted list of
    links.  For instance if a url is from MangaDex the link
    should only go to a valid MangaDex chapter and not one for
    J-Novel.

    eg. Ignore https://j-novel.club/read/XXXX
    eg. Allow  https://mangadex.org/chapter/XXXX
    """
    if self.source_name == SOURCE_MANGADEX:
      if SOURCE_MANGADEX_BASE_URL in url or SOURCE_MANGADEX_BASE_WWW_URL in url:
        return True
      else:
        return False
    elif self.source_name == SOURCE_MANGAHERE:
      if SOURCE_MANGAHERE_BASE_URL in url or SOURCE_MANGAHERE_BASE_WWW_URL in url:
        return True
      else:
        return False
    else:
      assert(0)
    return False

  def get_update(self):
    """
    Checks for new chapters and if required
    downloads them
    """
    chs, urls = self.metadata.get_chapter_numbers()
    assert(len(chs) == len(urls))

    logging.info("[" + self.get_tid() + " get_update]: Updating title '" + self.metadata.get_title() + "' on source " + self.source_name)

    for idx in range(len(chs)):
      # Check if the folder exists
      joined_chapter_path = path_join(self.download_title_abs_base_path, chs[idx] + ".cbz")
      
      # If the folder doesn't exist or if the path does exist but is not a foler
      # Attempt to download it
      if not exists(joined_chapter_path) and self.is_url_valid_source(urls[idx]):
        self.reset_for_next_chapter()
        self.start_driver()
        self.init_for_chapter(chs[idx], urls[idx])
        self.extract_chapter_images()
        self.create_comic_info()
        self.create_cbz()
        self.terminate_driver()
      else:
        if not self.is_url_valid_source(urls[idx]):
          logging.info("[" + self.get_tid() + " get_update]: Skipping chapter " + str(chs[idx]) + " for title: " + self.metadata.get_title() + " as it is not from a vlid source: " + urls[idx])
        else:
          assert(exists(joined_chapter_path))
          logging.info("[" + self.get_tid() + " get_update]: Skipping chapter " + str(chs[idx]) + " for title: " + self.metadata.get_title() + " as it is already downloaded")