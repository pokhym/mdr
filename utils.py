import base64
import shutil
from os.path import split as path_split, join as path_join, isfile
from os import listdir
from selenium import webdriver
from selenium.webdriver.common.by import By
from math import floor
import logging
import re

def get_xpath(elm):
    """
    https://stackoverflow.com/questions/71699032/find-the-xpath-with-get-attribute-in-python-selenium
    """
    e = elm
    xpath = elm.tag_name
    while e.tag_name != "html":
        e = e.find_element(By.XPATH, "..")
        neighbours = e.find_elements(By.XPATH, "../" + e.tag_name)
        level = e.tag_name
        if len(neighbours) > 1:
            level += "[" + str(neighbours.index(e) + 1) + "]"
        xpath = level + "/" + xpath
    return "/" + xpath

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

def is_char_digit(c):
  return c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def is_char_period(c):
  return c == "."

def extract_chapter_num_string(chapter_title):
  """
  Ch. 227 - Tried Various Things (3) -> 227

  Returns
  ------------
  ch_num: str
    String representation of the chapter number
  """
  found_first_digit = False
  num_string = ""
  for c in chapter_title:
    # First character must be a number
    if is_char_digit(c) and found_first_digit == False:
      found_first_digit = True
      num_string += c
      continue
    elif found_first_digit == False:
      continue
    # Any subsequent char must be a digit or period
    if found_first_digit and (is_char_digit(c) or is_char_period(c)):
      num_string += c
    # Terminate if no more digits or periods are found
    else:
      break
  
  if num_string == "":
    raise Exception("Unable to find chapter number for '" + chapter_title + "'")
  
  return num_string

def extract_chapter_num_range(num_string):
  """
  Returns a tuple of strings
    Low, High
  If there is no hypen High will be None

  TODO: This does not handle any chapters with a period
  and gets rounded down. eg. 46.5 -> 46
  """
  # https://www.mangaupdates.com/releases.html?search=73433348200&stype=series
  # This has chapters with alpha characters in it delete all of them
  # Handle 15a-c
  num_string = re.sub("[a-zA-Z]-[a-zA-Z]", "", num_string)
  # Handle 15c-19
  num_string = re.sub("[a-zA-Z]", "", num_string)
  if "-" not in num_string:
    if "." in num_string:
      logging.warn("[extract_chapter_num_range]: num_string got converted from " + num_string + " to " + str(int(floor(float(num_string)))))
      num_string = str(int(floor(float(num_string))))
      return num_string, None
    else:
      return extract_chapter_num_string(num_string), None
  else:
    splitted = num_string.split("-")
    assert(len(splitted) == 2)
    low = extract_chapter_num_string(splitted[0])
    high = extract_chapter_num_string(splitted[1])

    if "." in low:
      logging.warn("[extract_chapter_num_range]: Low got converted from " + low + " to " + str(int(floor(float(low)))))
      low = str(int(floor(float(low))))
    if "." in high:
      logging.warn("[extract_chapter_num_range]: Low got converted from " + high + " to " + str(int(floor(float(high)))))
      high = str(int(floor(float(high))))
    return low, high
  
def generate_ch_range(low_str, high_str):
  """
  55 None -> [55]
  55 57 -> [55, 56, 57]
  """
  if low_str == None:
    raise Exception("Low should not be None!")
  if high_str == None:
    return [str(low_str)]
  
  low_num = None
  high_num = None
  try:
    low_num = int(low_str)
    high_num = int(high_str)
  except:
    raise Exception("Unable to convert chapter string to int!")
  
  ret = [str(i) for i in range(low_num, high_num + 1)]
  return ret

def count_chapter_existence(ch_strs_list, title_base_path):
  """
  Takes a list of strings representing the chapters that should exist
  Takes a path to the title folder
  
  Counts the number of chapters for a specfici prefix.

  eg. ch_strs_list = ["45", "44", "43"]
  eg. path contains = ["45.cbz", "43.1.cbz', "43.2.cbz"]

  Returns a dict
  {
    "45" : 1,
    "44" : 0,
    "43" : 2
  }
  """
  ret = {}
  cbzs = [f for f in listdir(title_base_path) if isfile(path_join(title_base_path, f))]
  cbzs = [f.replace(".cbz", "") for f in cbzs if ".cbz" in f]

  for ch_str in ch_strs_list:
    ret[ch_str] = 0
  
  for ch_str in cbzs:
    ch_str_strip = ch_str
    period_idx = ch_str.find(".")
    if period_idx != -1:
      ch_str_strip = ch_str_strip[:period_idx]
    for k in ret.keys():
      if k in ch_str_strip:
        ret[k] += 1
        break
  return ret
      

def zip_folder_into_cbz(abs_folder_path):
  split_path = path_split(abs_folder_path)
  assert(len(split_path) == 2)

  shutil.make_archive(abs_folder_path, 'zip', abs_folder_path)
  shutil.move(abs_folder_path + ".zip", abs_folder_path + ".cbz")


if __name__ == "__main__":
  ns = extract_chapter_num_string("Ch. 227 - Tried Various Things (3)")
  print(ns)
  zip_folder_into_cbz("test/Isekai Nonbiri Nouka/216")