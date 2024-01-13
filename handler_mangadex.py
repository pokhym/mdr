from handler import Handler
from constants import *
import utils

import logging
from os.path import join as path_join
import time

from selenium import webdriver 
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys

class HandlerMangaDex(Handler):

  def extract_current_page(self):
    content = self.driver.find_element(By.XPATH, MANGADEX_PAGE_COUNT_CLASS).text
    # 'Site Rules\nPrivacy Policy\nAnnouncements\nv2023.11.27\n© MangaDex 2024\nCtrl\nK\nImmigrants and Doosu (2)\nIsekai Nonbiri Nouka\nCh. 222\nPg. 1 / 11\nMenu\nLHTranslation\n1\n11'
    assert(content.count(MANGADEX_PAGE_KEYWORD_START) == 1)
    # ` 1 / 11\nMenu\nLHTranslation\n1\n11'
    stripped = content[content.find(MANGADEX_PAGE_KEYWORD_START) + len(MANGADEX_PAGE_KEYWORD_START):]
    # ` 1/ 11`
    stripped = stripped[:stripped.find(MANGADEX_PAGE_KEYWORD_END)]
    # ` 1`
    curr_page = stripped[:stripped.find(MANGADEX_PAGE_DELIM_CURR_TOTAL)]
    curr_page = curr_page.strip()
    curr_page_num = None
    try:
      curr_page_num = int(curr_page)
    except Exception as e:
      raise Exception("Unable to convert current page number " + curr_page) from e
    logging.info("Start page: (str) " + str(curr_page) + " (int) " +  str(curr_page_num))
    return curr_page_num
  
  def extract_total_pages(self):
    content = self.driver.find_element(By.XPATH, MANGADEX_PAGE_COUNT_CLASS).text
    # 'Site Rules\nPrivacy Policy\nAnnouncements\nv2023.11.27\n© MangaDex 2024\nCtrl\nK\nImmigrants and Doosu (2)\nIsekai Nonbiri Nouka\nCh. 222\nPg. 1 / 11\nMenu\nLHTranslation\n1\n11'
    assert(content.count(MANGADEX_PAGE_KEYWORD_START) == 1)
    # ` 1 / 11\nMenu\nLHTranslation\n1\n11'
    stripped = content[content.find(MANGADEX_PAGE_KEYWORD_START) + len(MANGADEX_PAGE_KEYWORD_START):]
    # ` 1/ 11`
    stripped = stripped[:stripped.find(MANGADEX_PAGE_KEYWORD_END)]

    # ` 11`
    end_page = stripped[stripped.find(MANGADEX_PAGE_DELIM_CURR_TOTAL) + len(MANGADEX_PAGE_DELIM_CURR_TOTAL):]
    end_page = end_page.strip()
    end_page_num = None
    try:
      end_page_num = int(end_page)
    except Exception as e:
      raise Exception("Unable to convert current page number " + end_page) from e
    logging.info("End page: (str) " + str(end_page) + " (int) " +  str(end_page_num))

    return end_page_num
  
  def extract_single_image(self):
    downloaded = False
    for x in self.driver.find_elements(By.XPATH, MANGADEX_IMAGE_XCLASS):
      blob_location = x.get_attribute(MANGADEX_IMAGE_BLOB_ATTR)
      visible = True if x.get_attribute(MANGADEX_IMAGE_VISIBILITY_ATTR).find(MANGADEX_IMAGE_VISIBILITY_ATTR_NOT_VISIBLE_VALUE) == -1 else False
      # logging.info("Image: " + blob_location + " " + str(x.get_attribute(MANGADEX_IMAGE_VISIBILITY_ATTR)))

      # Download if it doesn't exist yet
      if blob_location not in self.downloaded_blobs_set and visible:
        # Ensure we only download one image per page
        assert(downloaded == False)

        self.downloaded_blobs_set.add(blob_location)
        logging.info("Downloading image " + str(self.current_download_image_number) + " with uri " + blob_location)
        self.extract_current_page()

        bytes = utils.get_blob_contents(self.driver, blob_location)
        joined_path = path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path, str(self.current_download_image_number) + ".png")
        with open(joined_path, "wb") as fd:
          fd.write(bytes)
          fd.close()
        
        # Flip flag so that we ensure next iteration doesn't download
        downloaded = True
        

  def extract_chapter_images(self):
    curr_page_num = self.extract_current_page()
    end_page_num = self.extract_total_pages()

    # Open the menu
    # This only should be done once as this remains open until you go back
    # To the original content page
    self.driver.find_element(By.CSS_SELECTOR, "body").send_keys("m")
    time.sleep(1)

    # Save the image
    while self.current_download_image_number < end_page_num:
      # Grab the specific page
      logging.info("Attempting to parse: " + self.current_chapter_base_url + "/" + str(self.current_download_image_number + 1))
      self.driver.get(self.current_chapter_base_url + "/" + str(self.current_download_image_number + 1))
      time.sleep(5)

      # Download the image
      self.extract_single_image()
      time.sleep(5)

      # Click the next button
      self.driver.find_element(By.XPATH, MANGADEX_NEXT_IMAGE_BUTTON_XCLASS).click()
      time.sleep(5)

      self.current_download_image_number += 1

    return
  