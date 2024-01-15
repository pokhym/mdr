from handler import Handler
from constants import *
from comic_info import ComicInfo
import utils
import urllib
import shutil

import logging
from os.path import join as path_join, exists, isdir
import time

from selenium import webdriver 
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys

class HandlerMangaDex(Handler):

  def select_chapter_language(self):
    if TARGET_LANGUAGE != TargetLanguageEnum.ENGLISH:
      self.save_screenshot()
      raise Exception("Unhandled language type to select!")

    self.select_english_chapters_only()

  def select_english_chapters_only(self):
    # Click user icon
    self.driver.find_element(By.ID, MANGADEX_USER_ICON_ID).click()
    # Select chapter selection language
    self.driver.find_element(By.XPATH, MANGADEX_USER_ICON_CHAPTER_LANGUAGES_XPATH).click()
    # Select the checkmark for english
    self.driver.find_element(By.XPATH, MANGADEX_USER_ICON_CHAPTER_LANGUAES_ENGLISH_XPATH).click()

    # Ensure it is checked
    assert("true" == self.driver.find_element(By.XPATH, MANGADEX_USER_ICON_CHAPTER_LANGUAES_ENGLISH_XPATH).get_attribute(MANGADEX_USER_ICON_CHAPTER_LANGUAES_ENGLISH_CHECKED_ATTR))
    time.sleep(SLEEP_SEC)

    # Exit the menu
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    time.sleep(SLEEP_SEC)


  def extract_current_page(self):
    # Sometimes the page number cannot be seen if the image is too big scroll to the top of the page
    time.sleep(SLEEP_SEC)
    self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.PAGE_UP)
    self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.PAGE_UP)
    time.sleep(SLEEP_SEC)
    content = self.driver.find_element(By.XPATH, MANGADEX_PAGE_COUNT_XPATH).text
    # try:
    #   content = self.driver.find_element(By.XPATH, MANGADEX_PAGE_COUNT_XPATH).text
    # except:
    #   logging.warn("[" + self.get_tid() + " extract_current_page]: Failed to extract page count info!")
    #   assert(0)
    # Pg. 1 / 35
    if content.count(MANGADEX_PAGE_KEYWORD_START) != 1:
      logging.warn("[" + self.get_tid() + " extract_current_page]: Failed to find '" + MANGADEX_PAGE_KEYWORD_START + "': " + content)
    assert(content.count(MANGADEX_PAGE_KEYWORD_START) == 1)
    # ` 1 / 35'
    stripped = content[content.find(MANGADEX_PAGE_KEYWORD_START) + len(MANGADEX_PAGE_KEYWORD_START):]
    # ` 1 / 35`
    # stripped = stripped[:stripped.find(MANGADEX_PAGE_KEYWORD_END)]
    # ` 1`
    curr_page = stripped[:stripped.find(MANGADEX_PAGE_DELIM_CURR_TOTAL)]
    curr_page = curr_page.strip()
    curr_page_num = None
    try:
      curr_page_num = int(curr_page)
    except Exception as e:
      self.save_screenshot()
      raise Exception("Unable to convert current page number " + curr_page) from e
    logging.info("[" + self.get_tid() + " extract_current_page]: Start page: (str) " + str(curr_page) + " (int) " +  str(curr_page_num))
    return curr_page_num
  
  def extract_total_pages(self):
    # Sometimes the page number cannot be seen if the image is too big scroll to the top of the page
    time.sleep(SLEEP_SEC)
    self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.PAGE_UP)
    self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.PAGE_UP)
    content = self.driver.find_element(By.XPATH, MANGADEX_PAGE_COUNT_XPATH).text
    time.sleep(SLEEP_SEC)
    # try:
    #   content = self.driver.find_element(By.XPATH, MANGADEX_PAGE_COUNT_XPATH).text
    # except:
    #   logging.warn("[" + self.get_tid() + " extract_total_pages]: Failed to extract page count info!")
    #   assert(0)
    # 'Site Rules\nPrivacy Policy\nAnnouncements\nv2023.11.27\n© MangaDex 2024\nCtrl\nK\nImmigrants and Doosu (2)\nIsekai Nonbiri Nouka\nCh. 222\nPg. 1 / 11\nMenu\nLHTranslation\n1\n11'
    if content.count(MANGADEX_PAGE_KEYWORD_START) != 1:
      logging.warn("[" + self.get_tid() + " extract_total_pages]: Failed to find '" + MANGADEX_PAGE_KEYWORD_START + "': " + content)

    # 'Pg. 1 / 35'
    assert(content.count(MANGADEX_PAGE_KEYWORD_START) == 1)
    # ` 1 / 35``
    stripped = content[content.find(MANGADEX_PAGE_KEYWORD_START) + len(MANGADEX_PAGE_KEYWORD_START):]
    # ` 1 / 35`
    # stripped = stripped[:stripped.find(MANGADEX_PAGE_KEYWORD_END)]

    # ` 11`
    end_page = stripped[stripped.find(MANGADEX_PAGE_DELIM_CURR_TOTAL) + len(MANGADEX_PAGE_DELIM_CURR_TOTAL):]
    end_page = end_page.strip()
    end_page_num = None
    try:
      end_page_num = int(end_page)
    except Exception as e:
      self.save_screenshot()
      raise Exception("Unable to convert current page number " + end_page) from e
    logging.info("[" + self.get_tid() + " extract_total_pages]: End page: (str) " + str(end_page) + " (int) " +  str(end_page_num))

    return end_page_num
  
  def extract_single_image(self):
    downloaded = False
    while True:
      for x in self.driver.find_elements(By.XPATH, MANGADEX_IMAGE_XCLASS):
          blob_location = x.get_attribute(MANGADEX_IMAGE_BLOB_ATTR)
          visible = True if x.get_attribute(MANGADEX_IMAGE_VISIBILITY_ATTR).find(MANGADEX_IMAGE_VISIBILITY_ATTR_NOT_VISIBLE_VALUE) == -1 else False

          # Download if it doesn't exist yet
          if blob_location not in self.downloaded_blobs_set and visible:
            # Ensure we only download one image per page
            assert(downloaded == False)

            self.downloaded_blobs_set.add(blob_location)
            logging.info("[" + self.get_tid() + " extract_single_image]: Downloading image " + str(self.current_download_image_number) + " with uri " + blob_location)
            # self.extract_current_page()

            bytes = utils.get_blob_contents(self.driver, blob_location)
            joined_path = path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path, str(self.current_download_image_number) + ".png")
            with open(joined_path, "wb") as fd:
              fd.write(bytes)
              fd.close()
            
            # Flip flag so that we ensure next iteration doesn't download
            downloaded = True
            break
      if downloaded:
        break
    assert(exists(path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path, str(self.current_download_image_number) + ".png")))
        

  def extract_chapter_images(self):
    logging.info("[" + self.get_tid() + " extract_chapter_images]: Handling chapter: " + self.current_chapter_base_url)

    logging.info("[" + self.get_tid() + " extract_chapter_images]: Extracting page numbers")
    curr_page_num = self.extract_current_page()
    end_page_num = self.extract_total_pages()

    # Open the menu
    # This only should be done once as this remains open until you go back
    # To the original content page
    # logging.info("[" + self.get_tid() + " extract_chapter_images]: Opening menu")
    # self.driver.find_element(By.CSS_SELECTOR, "body").send_keys("m")
    # time.sleep(1)

    # Save the image
    while self.current_download_image_number <= end_page_num:
      # Grab the specific page
      self.driver.get(self.current_chapter_base_url + "/" + str(self.current_download_image_number))
      time.sleep(SLEEP_SEC)

      # Download the image
      self.extract_single_image()
      # time.sleep(SLEEP_SEC)

      # Use right arrow key to advance to new page
      self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.ARROW_RIGHT)
      # # Click the next button
      # self.driver.find_element(By.XPATH, MANGADEX_NEXT_IMAGE_BUTTON_XCLASS).click()
      time.sleep(SLEEP_SEC)

      self.current_download_image_number += 1

    # Ensure the correct number of files is downloaded
    assert(self.current_download_image_number - 1 == end_page_num)
    
    cover_path = None
    if exists(path_join(self.download_title_abs_base_path, "cover.png")):
      cover_path = path_join(self.download_title_abs_base_path, "cover.png")
      # Copy cover
      shutil.copy(cover_path, path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path, "0.png"))
    elif exists(path_join(self.download_title_abs_base_path, "cover.jpg")):
      cover_path = path_join(self.download_title_abs_base_path, "cover.jpg")
      # Copy cover
      shutil.copy(cover_path, path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path, "0.jpg"))
    else:
      self.save_screenshot()
      raise Exception("Cover is missing!")

    return
  
  def create_comic_info(self):
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
    logging.info("[" + self.get_tid() + " create_cbz]: Creating cbz for: " + path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path))
    utils.zip_folder_into_cbz(path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path))
    assert(exists(path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path + ".cbz")))
    logging.info("[" + self.get_tid() + " create_cbz]: Removing folder: " + path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path))
    shutil.rmtree(path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path))

  def extract_title_name(self):
    title = self.driver.find_element(By.XPATH, MANGADEX_TITLE_XCLASS).text
    self.metadata.set_title(title)

  def extract_description(self):
    description = self.driver.find_element(By.XPATH, MANGADEX_DESCRIPTION_XCLASS).text
    self.metadata.set_description(description)
  
  def extract_categories(self):
    genres = []
    try:
      genres_obj = self.driver.find_element(By.XPATH, MANGADEX_GENRES_XCLASS)
      for tag_obj in genres_obj.find_elements(By.CLASS_NAME, MANGADEX_GENRES_TAG_OBJ_CLASS):
        genres.append(tag_obj.find_element(By.TAG_NAME, MANGADEX_GENRES_TAG_OBJ_TAG).text)
    except:
      logging.info("[" + self.get_tid() + " extract_categories] : No genres!")
    
    themes = []
    try:
      themes_obj = self.driver.find_element(By.XPATH, MANGADEX_THEMES_XCLASS)
      for tag_obj in themes_obj.find_elements(By.CLASS_NAME, MANGADEX_THEMES_TAG_OBJ_CLASS):
        themes.append(tag_obj.find_element(By.TAG_NAME, MANGADEX_THEMES_TAG_OBJ_TAG).text)
    except:
      logging.info("[" + self.get_tid() + " extract_categories] : No themes!")
    
    demographic = []
    try:
      demographic_obj = self.driver.find_element(By.XPATH, MANGADEX_DEMOGRAPHIC_XCLASS)
      # logging.info("[" + self.get_tid() + " extract_categories] : 2.1")
      for tag_obj in demographic_obj.find_elements(By.CLASS_NAME, MANGADEX_DEMOGRAPHIC_TAG_OBJ_CLASS):
        demographic.append(tag_obj.find_element(By.TAG_NAME, MANGADEX_DEMOGRAPHIC_TAG_OBJ_TAG).text)
    except:
      logging.info("[" + self.get_tid() + " extract_categories] : No demographic!")

    format = []
    try:
      format_obj = self.driver.find_element(By.XPATH, MANGADEX_FORMAT_XCLASS)
      for tag_obj in format_obj.find_elements(By.CLASS_NAME, MANGADEX_FORMAT_TAG_OBJ_CLASS):
        format.append(tag_obj.find_element(By.TAG_NAME, MANGADEX_FORMAT_TAG_OBJ_TAG).text)
    except:
      logging.info("[" + self.get_tid() + " extract_categories] : No format!")

    for g in genres:
      self.metadata.add_category(g)
    for t in themes:
      self.metadata.add_category(t)
    for d in demographic:
      self.metadata.add_category(d)
    for f in format:
      self.metadata.add_category(f)

  def extract_chapter_numbers(self):
    """
    Currently only supports English
    """
    if TARGET_LANGUAGE != TargetLanguageEnum.ENGLISH:
      self.save_screenshot()
      raise Exception("Unhandled target language!")
    
    # /html/body/div[1]/div[1]/div[2]/div[2]/div/div[9]/div[2]/div[2]/div[2]/div[7]
    # x = self.driver.find_elements(By.XPATH, "//svg[contains(@class, 'feather feather-arrow-left icon')]")
    # print(x)

    page_num = 1
    while True:
      logging.info("[" + self.get_tid() + " extract_chapter_numbers]: Grabbing page " + str(page_num) + " of chapters")
      # Obtain the the first page  
      for ch_obj in self.driver.find_elements(By.XPATH, MANGADEX_CHAPTER_TOP_LEVEL_XCLASS):
        flag_obj = ch_obj.find_element(By.XPATH, MANGADEX_CHAPTER_TOP_LEVEL_INNER_LANGUAGE_CLASS)
        lang = flag_obj.get_attribute(MANGADEX_CHAPTER_TOP_LEVEL_INNER_LANGUAGE_ATTR)

        if TARGET_LANGUAGE == TargetLanguageEnum.ENGLISH and lang == MANGADEX_ENGLISH_TITLE:
          ch_title = ch_obj.text
          ch_url = ch_obj.get_attribute(MANGADEX_CHAPTER_TOP_LEVEL_INNER_URL_ATTR)
          try:
            extracted_ch_num = utils.extract_chapter_num_string(ch_title)
          except:
            logging.info("[" + self.get_tid() + " extract_chapter_numbers]: Unable to extract chapter number! Probably has multiple sources! Attempting to grab outter div with chapter num!")
            try:
              # 'Chapter 57\nSkeleton...?\n44\nDreamManga\nN/A\nferonimo1\n3 years ago\nSkeleton...?\n66\nMangasushi\nN/A\nkketoxsushi\n3 years ago'
              ch_title = ch_obj.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..").find_element(By.XPATH, "./..").find_element(By.XPATH, "./..").text.split("\n")
              # Chapter 57
              ch_title = ch_title[0]
              extracted_ch_num = utils.extract_chapter_num_string(ch_title)
            except Exception as e:
              self.save_screenshot()
              raise e


          logging.info("[" + self.get_tid() + " extract_chapter_numbers]: Ch Num Extracted '" + extracted_ch_num + "' from: " + ch_title)
          self.metadata.add_chapter_number(utils.extract_chapter_num_string(ch_title), ch_url)
        
      # Check if there are next pages
      # <button>  
      #   <span>
      #     <svg>
      # This is why it is ./.. and ./.. twice
      try:
        right_arrow_button = self.driver.find_element(By.XPATH, MANGADEX_TITLE_RIGHT_ARROW_XPATH).find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
      except:
        logging.info("[" + self.get_tid() + " extract_chapter_numbers]: Cannot find right button, only 1 page breaking")
        break

      # Check if the button is disabled
      if MANGADEX_TITLE_RIGHT_ARROW_BUTTON_CLASS_DISABLED in right_arrow_button.get_attribute(MANGADEX_TITLE_RIGHT_ARROW_BUTTON_CLASS_ATTR):
        break

      # Click to advance to next page
      right_arrow_button.click()
      time.sleep(SLEEP_SEC)
      
      page_num += 1

  def extract_cover(self):
    cover = self.driver.find_element(By.XPATH, MANGADEX_TITLE_COVER_IMAGE_XPATH)
    href = cover.get_attribute(MANGADEX_TITLE_COVER_IMAGE_URL_ATTR)

    joined_path = None
    if "jpg" in href or "jpeg" in href:
      joined_path = path_join(self.download_title_abs_base_path, "cover.jpg")
    elif "png" in href:
      joined_path = path_join(self.download_title_abs_base_path, "cover.png")
    else:
      self.save_screenshot()
      raise Exception("Unknown cover image type with href: " + href)
    urllib.request.urlretrieve(cover.get_attribute(MANGADEX_TITLE_COVER_IMAGE_URL_ATTR), joined_path)

    logging.info("[" + self.get_tid() + " extract_cover]: Saving cover at: " + joined_path)

  def extract_metadata(self):
    logging.info("[" + self.get_tid() + " extract_metadata]: Extracting metadata!")
    self.start_driver()
    self.driver.get(self.current_title_base_url)
    time.sleep(SLEEP_SEC)

    logging.info("[" + self.get_tid() + " extract_metadata]: Selecting language!")
    self.select_chapter_language()
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
    chs, urls = self.metadata.get_chapter_numbers()
    assert(len(chs) == len(urls))

    logging.info("[" + self.get_tid() + " get_update]: Updating title '" + self.metadata.get_title() + "' on source " + self.source_name)

    for idx in range(len(chs)):
      # Check if the folder exists
      joined_chapter_path = path_join(self.download_title_abs_base_path, chs[idx] + ".cbz")
      
      # If the folder doesn't exist or if the path does exist but is not a foler
      # Attempt to download it
      if not exists(joined_chapter_path):
        self.reset_for_next_chapter()
        self.start_driver()
        self.init_for_chapter(chs[idx], urls[idx])
        self.extract_chapter_images()
        self.create_comic_info()
        self.create_cbz()
        self.terminate_driver()
      else:
        logging.info("[" + self.get_tid() + " get_update]: Skipping chapter " + str(chs[idx]) + " for title: " + self.metadata.get_title())

    