import logging
import multiprocessing as mp
from os.path import exists, expanduser

from handler_mangadex import HandlerMangaDex
from constants import *

# The full path to the root library location
ROOT_LIB_PATH = expanduser("~/Desktop/manga_library/")

# A file containing all links to Manga to be downloaded
# Each line contains a link
#   ...
#   https://mangadex.org/title/XXXX
#   https://mangadex.org/title/XXXX
#   ...
#
# This can be generated via grab_urls.sh
LIBRARY_LINKS_FILE_PATH = "library_links.txt"

# The path to the log file so that problems may be debugged
# such as when a download fails or the last operation that
# occured before an exception was raised
LOG_FILE_PATH = "log.txt"

# The number of concurrent HandlerMangadex instances to exist
MAX_THREADS = 1

# Mappin between thread id to URLs
# Key: tid (int)
# Value: URLs (Set[str])
TID_TO_URLS = dict()

def create_thread_mapping():
  """
  Map URLs in LIBRARY_LINKS_FILE_PATH to a thread id
  modulo MAX_THREADS
  """
  logging.info("[create_thread_mapping]: Parsing " + LIBRARY_LINKS_FILE_PATH)
  assert(exists(LIBRARY_LINKS_FILE_PATH))

  with open(LIBRARY_LINKS_FILE_PATH, "r") as fd:
    lines = fd.readlines()
    counter = 0

    for l in lines:
      counter = counter % MAX_THREADS
      if counter not in TID_TO_URLS.keys():
        TID_TO_URLS[counter] = set()
      TID_TO_URLS[counter].add(l)
      counter += 1
    fd.close()
  
  logging.info("[create_thread_mapping]: Done parsing " + LIBRARY_LINKS_FILE_PATH)
    
def run_handler_thread(tid):
  # Obtain the URLs that are for this thread
  logging.info("[run_handler_thread]: Starting tid " + str(tid))

  for url in sorted(TID_TO_URLS[tid]):
    url = url.strip()
    # logging.info("[run_handler_thread]: Thread " + str(tid) + " handling: " + str(url))

    if "mangadex" in url:
      mh = HandlerMangaDex(tid, SOURCE_MANGADEX)
      mh.reset_for_next_title()
      mh.init_for_title(ROOT_LIB_PATH, url)
      mh.extract_metadata()
      mh.get_update()
    else:
      raise Exception("Unknown source!")


if __name__ == "__main__":
  # Setup Logging
  logging.basicConfig(level=logging.INFO
                      , format="%(asctime)s;%(levelname)s;%(message)s"
                      , datefmt="%Y-%m-%d %H:%M:%S"
                      , filename="log.txt"
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

  logging.info("[main]: Starting!")

  create_thread_mapping()
  run_handler_thread(0)
  # p = mp.Pool(MAX_THREADS)
  # p.map(run_handler_thread, [i for i in range(MAX_THREADS)])
  
  logging.info("[main]: Completed!")