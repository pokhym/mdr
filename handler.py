from title_metadata import TitleMetadata

import logging
import time
from os.path import abspath, join as path_join, exists, isdir
from os import makedirs

from selenium import webdriver 
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys

class Handler:
  def __init__(self, source_name):
    """
    Member Variables
    -----------------
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
    self.source_name = source_name
    self.metadata = TitleMetadata()
    self.downloaded_blobs_set = set()
    self.download_title_abs_base_path = None
    self.download_chapter_rel_base_path = None
    self.current_title_base_url = None
    self.current_chapter_base_url = None
    self.current_download_image_number = 0

    # Initialize selenium
    # Define the Chrome webdriver options
    options = webdriver.FirefoxOptions()
    # options.binary_location = r'/usr/bin/firefox' 
    options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability
    options.add_argument("--enable-javascript")

    # By default, Selenium waits for all resources to download before taking actions.
    # However, we don't need it as the page is populated with dynamically generated JavaScript code.
    options.page_load_strategy = "none"

    geckodriver_path = "/snap/bin/geckodriver"  # specify the path to your geckodriver
    driver_service = Service(executable_path=geckodriver_path)

    # Pass the defined options objects to initialize the web driver 
    self.driver = Firefox(options=options, service=driver_service) 
    # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
    self.driver.implicitly_wait(5)

  def terminate_driver(self):
    """
    Terminates the Selenium driver
    """
    logging.info("Terminating " + self.source_name + " driver")
    self.driver.close()
  
  def reset_for_next_title(self):
    """
    Resets all member variables for handling the next title
    """
    self.downloaded_blobs_set.clear()
    self.download_title_abs_base_path = None
    self.download_chapter_rel_base_path = None
    self.current_title_base_url = None
    self.current_chapter_base_url = None
    self.current_download_image_number = 0

  def init_for_title(self, title_abs_base_path, title_base_url):
    """
    Initialize member variables for title and creates folders
    """
    self.download_title_abs_base_path = abspath(title_abs_base_path)
    
    if not exists(self.download_title_abs_base_path):
      logging.info("Creating base title folder at: " + self.download_title_abs_base_path)
      try:
        makedirs(self.download_title_abs_base_path)
      except Exception as e:
        raise Exception("Unable to create base title folder at: " + self.download_title_abs_base_path)
    else:
      assert(exists(self.download_title_abs_base_path))
      assert(isdir(self.download_title_abs_base_path))
      logging.info("Base title folder exists at: " + self.download_title_abs_base_path)
    
    logging.info("Loading title url: " + title_base_url)
    self.current_title_base_url = title_base_url
    self.driver.get(self.current_title_base_url)
    time.sleep(5)

  def reset_for_next_chapter(self):
    """
    Resets all member variables for handling the
    next chapter and creates folders
    """
    self.downloaded_blobs_set.clear()
    self.download_chapter_rel_base_path = None
    self.current_chapter_base_url = None
    self.current_download_image_number = 0

  def init_for_chapter(self, chapter_base_rel_path, chapter_url):
    """
    Initialize member variables for chapter
    """
    self.download_chapter_rel_base_path = chapter_base_rel_path
    self.current_chapter_base_url = chapter_url

    joined_path = path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path)
    if not exists(joined_path):
      logging.info("Creating chapter folder at: " + joined_path)
      try:
        makedirs(joined_path)
      except Exception as e:
        raise Exception("Unable to create chapter folder at: " + joined_path)
    else:
      assert(exists(joined_path))
      assert(isdir(joined_path))
      logging.info("Chapter folder exists at: " + joined_path)
      
    logging.info("Loading chapter url: " + chapter_url)
    self.current_chapter_base_url = chapter_url
    self.driver.get(self.current_chapter_base_url)
    time.sleep(5)

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

  def extract_title_name(self):
    """
    Obtain the title name

    Implemented for:
      - MangaDex
    """
    pass

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
    """
    pass

  def extract_chapter_numbers(self):
    """
    Returns the chapter numbers (and titles) of
    the current title
    """
    pass

  def get_update(self):
    """
    Checks for new chapters and if required
    downloads them
    """
    pass