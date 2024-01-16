import logging
import time
from constants import *
from handler import Handler
import utils
from os.path import join as path_join, exists
import urllib

from selenium import webdriver 
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys

class HandlerMangaHere(Handler):
  
  def extract_current_page(self):
    pages_outer_element = self.driver.find_element(By.XPATH, MANGAHERE_PAGE_BUTTONS_OUTER_XPATH)
    
    # Iterate from left -> right
    # This allows us to get the first page number
    curr_page_num = None
    for a in pages_outer_element.find_elements(By.TAG_NAME, MANGAHERE_PAGE_BUTTONS_INNER_TAG):
      try:
        curr_page_num = int(a.text)
        logging.info("[" + self.get_tid() + " extract_current_page]: Start page: (str) " + str(a.text) + " (int) " +  str(curr_page_num))
        return curr_page_num
      except:
        # Unable to convert to a number (possibly due to < or > representing back/forward)
        pass
    raise Exception("Unable to extract current page number!")
    
  
  def extract_total_pages(self):
    pages_outer_element = self.driver.find_element(By.XPATH, MANGAHERE_PAGE_BUTTONS_OUTER_XPATH)
    
    # Iterate from left -> right
    # This allows us to get the first page number
    curr_page_num = None
    for a in reversed(pages_outer_element.find_elements(By.TAG_NAME, MANGAHERE_PAGE_BUTTONS_INNER_TAG)):
      try:
        curr_page_num = int(a.text)
        logging.info("[" + self.get_tid() + " extract_total_pages]: End page: (str) " + str(a.text) + " (int) " +  str(curr_page_num))
        return curr_page_num
      except:
        # Unable to convert to a number (possibly due to < or > representing back/forward)
        pass
    raise Exception("Unable to extract current page number!")
  
  def extract_single_page(self):
    downloaded = False
    attempts = 0
    while True:
      if attempts > 5:
        self.driver.get(self.current_chapter_base_url + "#ipg" + str(self.current_download_image_number))
        time.sleep(SLEEP_SEC)
        logging.info("[" + self.get_tid() + " extract_single_page]: Reloading because no images!")
        attempts = 0

      # Hide the overlay
      self.driver.execute_script(MANGAHERE_HIDE_OVERLAY_SCRIPT)
      # Hide Danmaku if they exist
      try:
        self.driver.find_element(By.XPATH, MANGAHERE_HIDE_DANMAKU_XPATH).click()
      except:
        try:
          self.driver.find_element(By.XPATH, MANGAHERE_SHOW_DANMAKU_XPATH).click()
          self.driver.find_element(By.XPATH, MANGAHERE_HIDE_DANMAKU_XPATH).click()
        except:
          raise Exception("Neither hide/show danmaku exist")
        
      try:
        joined_path = path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path, str(self.current_download_image_number) + ".png")
        self.driver.find_element(By.XPATH, MANGAHERE_CHAPTER_IMAGE_XPATH).screenshot(joined_path)
        
        logging.info("[" + self.get_tid() + " extract_single_page]: Downloading image " + str(self.current_download_image_number))
        downloaded = True
      except:
        pass
      attempts += 1

      if downloaded:
        break
    
    assert(exists(path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path, str(self.current_download_image_number) + ".png")))
  
  def extract_chapter_images(self):
    logging.info("[" + self.get_tid() + " extract_chapter_images]: Handling chapter: " + self.current_chapter_base_url)

    logging.info("[" + self.get_tid() + " extract_chapter_images]: Extracting page numbers")
    curr_page_num = self.extract_current_page()
    end_page_num = self.extract_total_pages()

    # Save the image
    while self.current_download_image_number <= end_page_num:
      # Grab the specific page
      self.driver.get(self.current_chapter_base_url + "#ipg" + str(self.current_download_image_number))
      time.sleep(SLEEP_SEC)

      # Download the image
      self.extract_single_page()
      # time.sleep(SLEEP_SEC)

      # Use right arrow key to advance to new page
      self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.ARROW_RIGHT)
      # # Click the next button
      # self.driver.find_element(By.XPATH, MANGADEX_NEXT_IMAGE_BUTTON_XCLASS).click()
      time.sleep(SLEEP_SEC)

      self.current_download_image_number += 1

    # Ensure the correct number of files is downloaded
    assert(self.current_download_image_number - 1 == end_page_num)
  
  def create_comic_info(self):
    # TODO: Move into parent (also handler_mangadex.py)
    return super().create_comic_info()
  
  def create_cbz(self):
    # TODO: Move into parent (also handler_mangadex.py)
    return super().create_cbz()
  
  def extract_title_name(self):
    title = self.driver.find_element(By.XPATH, MANGAHERE_TITLE_XPATH).text
    self.metadata.set_title(title)
  
  def extract_description(self):
    # If the description has "more" click it first to expand
    try:
      self.driver.find_element(By.XPATH, MANGAHERE_DESCRIPTION_MORE_XPATH)
      self.driver.find_element(By.XPATH, MANGAHERE_DESCRIPTION_MORE_XPATH).click()
      # time.sleep(SLEEP_SEC)
    except:
      pass
    # Then get the content
    title = self.driver.find_element(By.XPATH, MANGAHERE_DESCRIPTION_XPATH).text
    self.metadata.set_description(title)
  
  def extract_categories(self):
    outer_categories_element = self.driver.find_element(By.XPATH, MANGAHERE_CATEGORIES_OUTER_XPATH)
    # 'Action Adventure Comedy Romance Shounen' -> ['Action', 'Adventure', 'Co  medy', 'Romance', 'Shounen']
    categories = outer_categories_element.text.split()
    for c in categories:
      self.metadata.add_category(c)
  
  def extract_chapter_numbers(self):
    try:
      self.driver.find_element(By.XPATH, MANGAHERE_CHAPTERS_EXPAND_BUTTON_XPATH)
      self.driver.find_element(By.XPATH, MANGAHERE_CHAPTERS_EXPAND_BUTTON_XPATH).click()
      logging.info("[" + self.get_tid() + " extract_chapter_numbers]: Expanding chapters!")
    except:
      pass
    
    chapters_outer_element = self.driver.find_element(By.XPATH, MANGAHERE_CHAPTERS_OUTER_XPATH)

    # Loop through to obtain all chapters
    for c in chapters_outer_element.find_elements(By.TAG_NAME, MANGAHERE_CHAPTERS_OUTER_INNER_TAG):
      ch_title = c.text
      a = c.find_element(By.TAG_NAME, MANGAHERE_CHAPTERS_OUTER_INNER_LINK_TAG)
      ch_url = a.get_attribute(MANGAHERE_CHAPTERS_OUTER_INNER_LINK_ATTR)

      # Replace http with https
      if "http://" in ch_url:
        assert(ch_url.count("http://") == 1)
        ch_url = ch_url.replace("http://", "https://")

      try:
        extracted_ch_num = utils.extract_chapter_num_string(ch_title)
      except Exception as e:
        self.save_screenshot()
        raise e

      logging.info("[" + self.get_tid() + " extract_chapter_numbers]: Ch Num Extracted '" + extracted_ch_num + "' from: " + ch_title)
      self.metadata.add_chapter_number(utils.extract_chapter_num_string(ch_title), ch_url)
  
  def extract_cover(self):
    cover = self.driver.find_element(By.XPATH, MANGAHERE_COVER_IMAGE_XPATH)
    joined_path = path_join(self.download_title_abs_base_path, "cover.png")
    cover.screenshot(joined_path)
  
  def extract_metadata(self):
    logging.info("[" + self.get_tid() + " extract_metadata]: Extracting metadata!")
    self.start_driver()
    self.driver.get(self.current_title_base_url)
    time.sleep(SLEEP_SEC)

    logging.info("[" + self.get_tid() + " extract_metadata]: Getting titlename!")
    self.extract_title_name()
    logging.info("[" + self.get_tid() + " extract_metadata]: Getting title base url!")
    self.extract_title_url()
    logging.info("[" + self.get_tid() + " extract_metadata]: Getting description!")
    self.extract_description()
    logging.info("[" + self.get_tid() + " extract_metadata]: Getting categories!")
    self.extract_categories()
    logging.info("[" + self.get_tid() + " extract_metadata]: Getting chapter numbers!")
    self.extract_chapter_numbers()
    logging.info("[" + self.get_tid() + " extract_metadata]: Getting chapter cover!")
    self.extract_cover()
    logging.info("[" + self.get_tid() + " extract_metadata]: Saving metadata!")
    self.save_metadata()

    self.terminate_driver()

  
  def get_update(self):
    return super().get_update()
  