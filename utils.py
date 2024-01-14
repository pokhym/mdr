import base64
import shutil
from os.path import split as path_split, join as path_join

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

def zip_folder_into_cbz(abs_folder_path):
  split_path = path_split(abs_folder_path)
  assert(len(split_path) == 2)

  shutil.make_archive(abs_folder_path, 'zip', abs_folder_path)
  shutil.move(abs_folder_path + ".zip", abs_folder_path + ".cbz")


if __name__ == "__main__":
  ns = extract_chapter_num_string("Ch. 227 - Tried Various Things (3)")
  print(ns)
  zip_folder_into_cbz("test/Isekai Nonbiri Nouka/216")