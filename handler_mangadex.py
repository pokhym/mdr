from handler import Handler
from constants import *
from comic_info import ComicInfo
import utils
import requests
import shutil

import logging
from os.path import join as path_join, exists, isdir
import time

from selenium import webdriver 
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class HandlerMangaDex(Handler):

  def select_chapter_language(self):
    if TARGET_LANGUAGE != TargetLanguageEnum.ENGLISH:
      self.save_screenshot()
      raise Exception("Unhandled language type to select!")

    self.select_english_chapters_only()

  def select_english_chapters_only(self):
    wait = WebDriverWait(self.driver, SLEEP_SEC * 2)
    # Click user icon
    userid_obj = wait.until(EC.presence_of_element_located((By.ID, MANGADEX_USER_ICON_ID)))
    userid_obj.click()
    # Select chapter selection language
    userid_ch_lang_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_USER_ICON_CHAPTER_LANGUAGES_XPATH)))
    # Wait until the user menu is available
    wait.until(EC.visibility_of(userid_ch_lang_obj))
    userid_ch_lang_obj.click()
    # Select the checkmark for english
    userid_ch_lang_eng_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_USER_ICON_CHAPTER_LANGUAES_ENGLISH_XPATH)))
    # Wait until language choice menu is visible
    wait.until(EC.visibility_of(userid_ch_lang_eng_obj))
    userid_ch_lang_eng_obj.click()

    # Ensure it is checked
    assert("true" == userid_ch_lang_eng_obj.get_attribute(MANGADEX_USER_ICON_CHAPTER_LANGUAES_ENGLISH_CHECKED_ATTR))

    # As we are expecting the page to refresh now wait until the main body of the body to show up
    body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    wait.until(EC.visibility_of(body_obj))
    
    # Exit the menu
    body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    body_obj.click()

  def extract_mangaupdates_url(self):
    """
    Extracts the MangaHere link from the title page
    """
    started_driver_locally = False
    if self.driver == None:
      self.start_driver()
      started_driver_locally = True
      self.driver.get(self.current_title_base_url)
      wait = WebDriverWait(self.driver, SLEEP_SEC * 2)
      body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
      wait.until(EC.visibility_of(body_obj))
    else:
      self.driver.get(self.current_title_base_url)
      wait = WebDriverWait(self.driver, SLEEP_SEC * 2)
      body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
      wait.until(EC.visibility_of(body_obj))
    logging.info("[" + self.get_tid() + " extract_mangaupdates_url]: Extracting MangaUpdates link!")
    try:
      wait = WebDriverWait(self.driver, SLEEP_SEC * 2)
      mangaupdates_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_MANGAUPDATES_XCLASS)))
      url = mangaupdates_obj.get_attribute(MANGADEX_MANGAUPDATES_ATTRIBUTE)
      self.current_title_manga_updates_base_url = url
      assert(self.current_title_manga_updates_base_url != "" and self.current_title_manga_updates_base_url != None)
    except:
      logging.error("[" + self.get_tid() + " extract_mangaupdates_url]: Unable to obtain MangaUpdates link!")

    if started_driver_locally:
      self.terminate_driver()

  def extract_current_page(self):
    # Sometimes the page number cannot be seen if the image is too big scroll to the top of the page
    wait = WebDriverWait(self.driver, SLEEP_SEC)
    body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    body_obj.send_keys(Keys.PAGE_UP)
    wait = WebDriverWait(self.driver, SLEEP_SEC)
    body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    body_obj.send_keys(Keys.PAGE_UP)
    
    content_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_PAGE_COUNT_XPATH)))
    content = content_obj.text
    # try:
    #   content = self.driver.find_element(By.XPATH, MANGADEX_PAGE_COUNT_XPATH).text
    # except:
    #   logging.warn("[" + self.get_tid() + " extract_current_page]: Failed to extract page count info!")
    #   assert(0)
    
    # Web toon does not show page count
    if content.count(MANGADEX_PAGE_KEYWORD_START) != 1:
      logging.warn("[" + self.get_tid() + " extract_current_page]: Assuming webtoon failed to find '" + MANGADEX_PAGE_KEYWORD_START + "': " + content)

      return self.current_download_image_number
    # Pg. 1 / 35
    else:
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
    """
    Returns None if webtoon
    """
    # Sometimes the page number cannot be seen if the image is too big scroll to the top of the page
    wait = WebDriverWait(self.driver, SLEEP_SEC)
    body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    wait.until(EC.visibility_of(body_obj))
    body_obj.send_keys(Keys.PAGE_UP)
    body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    wait.until(EC.visibility_of(body_obj))
    body_obj.send_keys(Keys.PAGE_UP)

    content_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_PAGE_COUNT_XPATH)))
    content = content_obj.text
    # try:
    #   content = self.driver.find_element(By.XPATH, MANGADEX_PAGE_COUNT_XPATH).text
    # except:
    #   logging.warn("[" + self.get_tid() + " extract_total_pages]: Failed to extract page count info!")
    #   assert(0)
    
    # Web toon does not have 
    if content.count(MANGADEX_PAGE_KEYWORD_START) != 1:
      logging.warn("[" + self.get_tid() + " extract_total_pages]: Assuming webtoon failed to find '" + MANGADEX_PAGE_KEYWORD_START + "': " + content)
      
      # end_page_num = 0
      # images_outer_wrapper_object = self.driver.find_element(By.XPATH, MANGADEX_WEBTOON_OUTER_XCLASS)
      # blobs = [i.get_attribute(MANGADEX_IMAGE_BLOB_ATTR) for i in images_outer_wrapper_object.find_elements(By.XPATH, MANGADEX_WEBTOON_OUTER_OVERFLOW_XCLASS) if i.tag_name == "img"]
      # logging.info("[" + self.get_tid() + " extract_total_pages]: End page: (str) " + str(len(blobs)) + " (int) " +  str(len(blobs)))
      # Mark as webtoon
      self.is_webtoon = True
      return None
    # 'Pg. 1 / 35'
    else:
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
  
  def extract_single_page(self):
    downloaded = False
    attempts = 0
    while True:
      if attempts > 5:
        self.driver.get(self.current_chapter_base_url + "/" + str(self.current_download_image_number))
        wait = WebDriverWait(self.driver, SLEEP_SEC * 2)
        body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        wait.until(EC.visibility_of(body_obj))
        logging.info("[" + self.get_tid() + " extract_single_page]: Reloading because no images!")
        attempts = 0
      attempts += 1
      for x in self.driver.find_elements(By.XPATH, MANGADEX_IMAGE_XCLASS):
          blob_location = x.get_attribute(MANGADEX_IMAGE_BLOB_ATTR)
          visible = True if x.get_attribute(MANGADEX_IMAGE_VISIBILITY_ATTR).find(MANGADEX_IMAGE_VISIBILITY_ATTR_NOT_VISIBLE_VALUE) == -1 else False

          # Download if it doesn't exist yet
          if blob_location not in self.downloaded_blobs_set and visible:
            # Ensure we only download one image per page
            assert(downloaded == False)

            self.downloaded_blobs_set.add(blob_location)
            logging.info("[" + self.get_tid() + " extract_single_page]: Downloading image " + str(self.current_download_image_number) + " with uri " + blob_location)
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

  def extract_webtoon_chapter(self):
    """
    As MangaDex seems to treat webtoons differently by loading all the images "at once"
    this function is required to iterate over all of them. Requires the chapter to be loaded
    by the driver before calling this

    Returns
    ------------------
    Number of pages in the chapter
    """ 
    self.driver.get(self.current_chapter_base_url)
    # Required to ensure that the first image is the top of the page
    # Otherwise MANGADEX_IMAGE_XCLASS may return not the first image
    wait = WebDriverWait(self.driver, SLEEP_SEC)
    body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    wait.until(EC.visibility_of(body_obj))
    end_page_num = 0
    # This is used to ensure that we do not get stale references to images
    time.sleep(SLEEP_SEC)

    while True:
      # wait = WebDriverWait(self.driver, SLEEP_SEC * 2)
      try:
        image_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_IMAGE_XCLASS)))
        wait.until(EC.element_to_be_clickable(image_obj))
      except:
        logging.info("[" + self.get_tid() + " extract_webtoon_chapter]: Finished downloading chapter")
        assert(len(self.driver.find_elements(By.XPATH, MANGADEX_IMAGE_XCLASS)) == 0)
        break
      image_blob = image_obj.get_attribute(MANGADEX_IMAGE_BLOB_ATTR)

      if(image_blob in self.downloaded_blobs_set):
        break
      self.downloaded_blobs_set.add(image_blob)

      logging.info("[" + self.get_tid() + " extract_webtoon_chapter]: Downloading image " + str(self.current_download_image_number) + " with uri " + image_blob)
      # self.extract_current_page()

      bytes = utils.get_blob_contents(self.driver, image_blob)
      joined_path = path_join(self.download_title_abs_base_path, self.download_chapter_rel_base_path, str(self.current_download_image_number) + ".png")
      with open(joined_path, "wb") as fd:
        fd.write(bytes)
        fd.close()

      # Delete image
      self.driver.execute_script(MANGADEX_IMAGE_DELETE_SCRIPT(image_obj.get_attribute("class")))

      wait.until(EC.invisibility_of_element(image_obj))
      
      end_page_num += 1
      self.current_download_image_number += 1

    assert(self.current_download_image_number -1 == end_page_num)
    return end_page_num

  def extract_chapter_images(self):
    logging.info("[" + self.get_tid() + " extract_chapter_images]: Handling chapter: " + self.current_chapter_base_url)

    logging.info("[" + self.get_tid() + " extract_chapter_images]: Extracting page numbers")
    # curr_page_num = self.extract_current_page()
    # Determine if webtoon or not
    end_page_num = self.extract_total_pages()

    if self.is_webtoon:
      end_page_num = self.extract_webtoon_chapter()
    else:
      wait = WebDriverWait(self.driver, SLEEP_SEC * 2)
      # Open the menu
      # This only should be done once as this remains open until you go back
      # To the original content page
      logging.info("[" + self.get_tid() + " extract_chapter_images]: Opening menu")

      # Wait until body loads
      body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
      wait.until(EC.visibility_of(body_obj))
      # body_obj.send_keys("m")

      # Obtain the first image that is of the correct type
      image_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_IMAGE_XCLASS)))
      body_obj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
      wait.until(EC.visibility_of(body_obj))
      body_obj.send_keys("m")

      logging.info("[" + self.get_tid() + " extract_chapter_images]: Selecting long strip")
      # Convert to long strip to obtain blobs all at once and use extract_webtoon as normal
      change_reader_type_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_CHANGE_READER_TYPE)))
      wait.until(EC.visibility_of(change_reader_type_obj))
      change_reader_type_obj.click()
      change_reader_type_obj.click()
      
      end_page_num = self.extract_webtoon_chapter()

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
  
  def extract_title_name(self):
    wait = WebDriverWait(self.driver, SLEEP_SEC * 2)
    title_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_TITLE_XCLASS)))
    wait.until(EC.visibility_of(title_obj))
    title = title_obj.text
    # title = self.driver.find_element(By.XPATH, MANGADEX_TITLE_XCLASS).text
    self.metadata.set_title(title)

  def extract_description(self):
    try:
      wait = WebDriverWait(self.driver, SLEEP_SEC)
      description_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_DESCRIPTION_XCLASS)))
      description = description_obj.text
      self.metadata.set_description(description)
    except:
      logging.info("[" + self.get_tid() + " extract_description] : No description!")
      self.metadata.set_description("")
  
  def extract_categories(self):
    wait = WebDriverWait(self.driver, SLEEP_SEC)
    genres = []
    try:
      genres_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_GENRES_XCLASS)))
      for tag_obj in genres_obj.find_elements(By.CLASS_NAME, MANGADEX_GENRES_TAG_OBJ_CLASS):
        genres.append(tag_obj.find_element(By.TAG_NAME, MANGADEX_GENRES_TAG_OBJ_TAG).text)
    except:
      logging.info("[" + self.get_tid() + " extract_categories] : No genres!")
    
    themes = []
    try:
      themes_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_THEMES_XCLASS)))
      for tag_obj in themes_obj.find_elements(By.CLASS_NAME, MANGADEX_THEMES_TAG_OBJ_CLASS):
        themes.append(tag_obj.find_element(By.TAG_NAME, MANGADEX_THEMES_TAG_OBJ_TAG).text)
    except:
      logging.info("[" + self.get_tid() + " extract_categories] : No themes!")
    
    demographic = []
    try:
      demographic_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_DEMOGRAPHIC_XCLASS)))
      # logging.info("[" + self.get_tid() + " extract_categories] : 2.1")
      for tag_obj in demographic_obj.find_elements(By.CLASS_NAME, MANGADEX_DEMOGRAPHIC_TAG_OBJ_CLASS):
        demographic.append(tag_obj.find_element(By.TAG_NAME, MANGADEX_DEMOGRAPHIC_TAG_OBJ_TAG).text)
    except:
      logging.info("[" + self.get_tid() + " extract_categories] : No demographic!")

    format = []
    try:
      format_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_FORMAT_XCLASS)))
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
      wait = WebDriverWait(self.driver, SLEEP_SEC)
      chs_obj = wait.until(EC.presence_of_all_elements_located((By.XPATH, MANGADEX_CHAPTER_TOP_LEVEL_XCLASS)))
      chs_obj = wait.until(EC.visibility_of_all_elements_located((By.XPATH, MANGADEX_CHAPTER_TOP_LEVEL_XCLASS)))
      # Obtain the the first page  
      for ch_obj in chs_obj: # self.driver.find_elements(By.XPATH, MANGADEX_CHAPTER_TOP_LEVEL_XCLASS):
        wait = WebDriverWait(ch_obj, SLEEP_SEC)
        flag_obj = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_CHAPTER_TOP_LEVEL_INNER_LANGUAGE_CLASS)))
        lang = flag_obj.get_attribute(MANGADEX_CHAPTER_TOP_LEVEL_INNER_LANGUAGE_ATTR)

        if TARGET_LANGUAGE == TargetLanguageEnum.ENGLISH and lang == MANGADEX_ENGLISH_TITLE:
          ch_title = ch_obj.text
          ch_url = ch_obj.get_attribute(MANGADEX_CHAPTER_TOP_LEVEL_INNER_URL_ATTR)
          try:
            # When filtering by English, all chapters must begin with "Ch." unless there are multiple
            # uploaders after which we nee dto go up two levels like in the try block below
            assert(ch_title.startswith("Ch."))
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
      
      page_num += 1

  def extract_cover(self):
    wait = WebDriverWait(self.driver, SLEEP_SEC)
    cover = wait.until(EC.presence_of_element_located((By.XPATH, MANGADEX_TITLE_COVER_IMAGE_XPATH)))
    href = cover.get_attribute(MANGADEX_TITLE_COVER_IMAGE_URL_ATTR)

    joined_path = None
    if "jpg" in href or "jpeg" in href:
      joined_path = path_join(self.download_title_abs_base_path, "cover.jpg")
    elif "png" in href:
      joined_path = path_join(self.download_title_abs_base_path, "cover.png")
    else:
      self.save_screenshot()
      raise Exception("Unknown cover image type with href: " + href)
    
    # https://stackoverflow.com/questions/32763720/timeout-a-file-download-with-python-urllib
    # Make the actual request, set the timeout for no data to 10 seconds and enable streaming responses so we don't have to keep the large files in memory
    request = requests.get(href, timeout=SLEEP_SEC, stream=True)

    # Open the output file and make sure we write in binary mode
    with open(joined_path, 'wb') as fh:
        # Walk through the request response in chunks of 1024 * 1024 bytes, so 1MiB
        for chunk in request.iter_content(1024 * 1024):
            # Write the chunk to the file
            fh.write(chunk)
            # Optionally we can check here if the download is taking too long

    logging.info("[" + self.get_tid() + " extract_cover]: Saving cover at: " + joined_path)

  def extract_metadata(self):
    logging.info("[" + self.get_tid() + " extract_metadata]: Extracting metadata!")
    self.start_driver()
    self.driver.get(self.current_title_base_url)

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
    