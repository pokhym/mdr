from selenium import webdriver 
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
import argparse
import time
import logging
import base64

# This is actually looking for "Pg. 1 / 2"
PAGE_COUNT_CLASS = "//div[contains(@class, 'flex-grow')]"
PAGE_KEYWORD_START = "Pg."
PAGE_KEYWORD_END = "\n"
# 1 / 11 slash is the delimiter
PAGE_DELIM_CURR_TOTAL = "/"
# Image XCLASS
IMAGE_XCLASS = "//img[contains(@class, 'img sp limit-width limit-height mx-auto')]"
# Attribute containing the blob url
IMAGE_BLOB_ATTR = "src"

def get_blob_contents(driver, uri):
  """
  Downloads a blob image and returns the bytes
  https://stackoverflow.com/questions/47424245/how-to-download-an-image-with-python-3-selenium-if-the-url-begins-with-blob

  Arguments
  --------------------
  driver
  uri: blob:https://mangadex.org/499f94d4-dfae-4354-8875-6fbf22f67eef

  Returns
  --------------------
  bytes: The image data
  """
  result = driver.execute_async_script("""
    var uri = arguments[0];
    var callback = arguments[1];
    var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'arraybuffer';
    xhr.onload = function(){ callback(toBase64(xhr.response)) };
    xhr.onerror = function(){ callback(xhr.status) };
    xhr.open('GET', uri);
    xhr.send();
    """, uri)
  if type(result) == int :
    raise Exception("Request failed with status %s" % result)
  return base64.b64decode(result)

def extract_current_page(driver):
  content = driver.find_element(By.XPATH, PAGE_COUNT_CLASS).text
  # 'Site Rules\nPrivacy Policy\nAnnouncements\nv2023.11.27\n© MangaDex 2024\nCtrl\nK\nImmigrants and Doosu (2)\nIsekai Nonbiri Nouka\nCh. 222\nPg. 1 / 11\nMenu\nLHTranslation\n1\n11'
  assert(content.count(PAGE_KEYWORD_START) == 1)
  # ` 1 / 11\nMenu\nLHTranslation\n1\n11'
  stripped = content[content.find(PAGE_KEYWORD_START) + len(PAGE_KEYWORD_START):]
  # ` 1/ 11`
  stripped = stripped[:stripped.find(PAGE_KEYWORD_END)]
  # ` 1`
  curr_page = stripped[:stripped.find(PAGE_DELIM_CURR_TOTAL)]
  curr_page = curr_page.strip()
  curr_page_num = None
  try:
    curr_page_num = int(curr_page)
  except Exception as e:
    raise Exception("Unable to convert current page number " + curr_page) from e
  logging.info("Start page: " + str(curr_page) + " " +  str(curr_page_num))
  return curr_page_num

def extract_total_pages(driver):
  content = driver.find_element(By.XPATH, PAGE_COUNT_CLASS).text
  # 'Site Rules\nPrivacy Policy\nAnnouncements\nv2023.11.27\n© MangaDex 2024\nCtrl\nK\nImmigrants and Doosu (2)\nIsekai Nonbiri Nouka\nCh. 222\nPg. 1 / 11\nMenu\nLHTranslation\n1\n11'
  assert(content.count(PAGE_KEYWORD_START) == 1)
  # ` 1 / 11\nMenu\nLHTranslation\n1\n11'
  stripped = content[content.find(PAGE_KEYWORD_START) + len(PAGE_KEYWORD_START):]
  # ` 1/ 11`
  stripped = stripped[:stripped.find(PAGE_KEYWORD_END)]

  # ` 11`
  end_page = stripped[stripped.find(PAGE_DELIM_CURR_TOTAL) + len(PAGE_DELIM_CURR_TOTAL):]
  end_page = end_page.strip()
  end_page_num = None
  try:
    end_page_num = int(end_page)
  except Exception as e:
    raise Exception("Unable to convert current page number " + end_page) from e
  logging.info("End page: " + str(end_page) + " " +  str(end_page_num))

  return end_page_num

def extract_single_image(driver, i, base_path=""):
  blob_location = driver.find_element(By.XPATH, IMAGE_XCLASS).get_attribute(IMAGE_BLOB_ATTR)

  for x in driver.find_elements(By.XPATH, IMAGE_XCLASS):
    print(x.get_attribute("src"))

  logging.info("Downloading image " + str(i) + " with uri " + blob_location)
  extract_current_page(driver)

  bytes = get_blob_contents(driver, blob_location)
  with open(base_path + str(i) + ".png", "wb") as fd:
    fd.write(bytes)
    fd.close()
  return blob_location

def extract_chapter_images(driver):
  """
  Extracts the number of pages, and the pages of a chapter.
  This expects that the driver is already loaded for the chapter
  """
  curr_page_num = extract_current_page(driver)
  end_page_num = extract_total_pages(driver)

  # Save the image
  # for i in range(curr_page_num, end_page_num + 1):
  #   extract_single_image(driver, i)
  #   driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.ARROW_RIGHT)
  #   time.sleep(5)
  previous_blob = None
  counter = 0
  driver.find_element(By.CSS_SELECTOR, "body").send_keys("m")
  time.sleep(1)
  while True:
    if counter > end_page_num:
      break
    returned_blob = extract_single_image(driver, counter)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/button[2]").click()
    time.sleep(5)

    if previous_blob == None:
      previous_blob = returned_blob
      counter += 1
    elif previous_blob != returned_blob:
      previous_blob = returned_blob
      counter += 1

  a = 0
  return

if __name__ == "__main__":
  # Setup Logging
  logging.basicConfig(level=logging.INFO)
  
  # Setup argparse
  parser = argparse.ArgumentParser(
                    prog='webpage_utils',
                    description='Obtains JavaScript webpages',
                    epilog='')
  parser.add_argument('-u', '--url', help="URL, required arg")
  args = parser.parse_args()

  # Error check the arguments
  if(args.url == None):
    print("FAIL")
    exit(0)
  
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
  driver = Firefox(options=options, service=driver_service) 
  # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
  driver.implicitly_wait(5)

  url = args.url

  driver.get(url)

  time.sleep(5)
  print(driver.page_source)
  print("----------------------")
  extract_chapter_images(driver)
  driver.close()