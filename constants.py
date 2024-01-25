from enum import Enum

class TargetLanguageEnum(Enum):
  ENGLISH = 1

"""--- BEGIN SELENIUM FIREFOX OPTIONS ---"""
# USE ONLY IF ONLY WINDOWS
FIREFOX_BIN_PATH = "C:/Program Files/Mozilla Firefox/firefox.exe"
# USE ON BOTH LINUX AND WINDOWS
GECKO_BIN_PATH = "/snap/bin/geckodriver"

""" --- BEGIN METADATA FILE NAME ---"""
METADATA_FILE_NAME = "metadata.txt"

""" --- GLOBAL SLEEP TIME --- """
SLEEP_SEC = 5

"""--- BEGIN TARGET LANGUAGE ---"""
TARGET_LANGUAGE = TargetLanguageEnum.ENGLISH
"""--- END TARGET LANGUAGE ---"""

"""--- BEGIN SOURCE NAMES ---"""
SOURCE_MANGADEX = "MangaDex"
SOURCE_MANGADEX_BASE_URL = "https://mangadex.org"
SOURCE_MANGADEX_BASE_WWW_URL = "https://www.mangadex.org"
SOURCE_MANGAHERE = "MangaHere"
SOURCE_MANGAHERE_BASE_URL = "https://mangahere.cc"
SOURCE_MANGAHERE_BASE_WWW_URL = "https://www.mangahere.cc"
"""--- END SOURCE NAMES ---"""

"""--- START PER SOURCE CONSTANTS ---"""

"""--- BEGIN MANAGDEX CONSTANTS ---"""
# User Icon XPATH
MANGADEX_USER_ICON_XPATH = "//*[@id='avatar']"
MANGADEX_USER_ICON_ID = "avatar"
# Language submenu in user
MANGADEX_USER_ICON_CHAPTER_LANGUAGES_XPATH = "/html/body/div[1]/div[3]/div[2]/div/div[1]/button[2]"
# English language selection XPATHs
MANGADEX_USER_ICON_CHAPTER_LANGUAES_ENGLISH_XPATH = "/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/label"
MANGADEX_USER_ICON_CHAPTER_LANGUAES_ENGLISH_CHECKED_ATTR = "aria-checked"

# Cover Image XPATH
MANGADEX_TITLE_COVER_IMAGE_XPATH = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/div/a/img[1]"
MANGADEX_TITLE_COVER_IMAGE_URL_ATTR = "src"

# Next page of available chapters XPATHS
MANGADEX_TITLE_RIGHT_ARROW_XPATH = "//*[contains(@class, 'feather feather-arrow-right icon')]"
MANGADEX_TITLE_RIGHT_ARROW_BUTTON_CLASS_ATTR = "class"
MANGADEX_TITLE_RIGHT_ARROW_BUTTON_CLASS_DISABLED = "disabled"

# Title XPATH
MANGADEX_TITLE_XCLASS = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[4]/p"
# Description XPATH
MANGADEX_DESCRIPTION_XCLASS = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[8]/div/div/div/div[1]/div/p"
# Genres XPATH
MANGADEX_GENRES_XCLASS = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[9]/div[2]/div[1]/div[3]/div[2]"
MANGADEX_GENRES_TAG_OBJ_CLASS = "tag"
MANGADEX_GENRES_TAG_OBJ_TAG = "span"
# Themes XPATH
MANGADEX_THEMES_XCLASS = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[9]/div[2]/div[1]/div[4]/div[2]"
MANGADEX_THEMES_TAG_OBJ_CLASS = "tag"
MANGADEX_THEMES_TAG_OBJ_TAG = "span"
# Demographic XPATH
MANGADEX_DEMOGRAPHIC_XCLASS = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[9]/div[2]/div[1]/div[5]/div[2]"
MANGADEX_DEMOGRAPHIC_TAG_OBJ_CLASS = "tag"
MANGADEX_DEMOGRAPHIC_TAG_OBJ_TAG = "span"
# Format XPATH
MANGADEX_FORMAT_XCLASS = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[9]/div[2]/div[1]/div[6]/div[2]"
MANGADEX_FORMAT_TAG_OBJ_CLASS = "tag"
MANGADEX_FORMAT_TAG_OBJ_TAG = "span"
# English Title
MANGADEX_ENGLISH_TITLE = "English"
# Chapter top level XPATH this includes both the language and title name
MANGADEX_CHAPTER_TOP_LEVEL_XCLASS = "//a[contains(@class, 'flex flex-grow items-center')]"
# Inner portion of the top level chapter that returns the flag
MANGADEX_CHAPTER_TOP_LEVEL_INNER_LANGUAGE_CLASS = "//img[contains(@class, 'inline-block select-none flex-shrink-0 !h-5 !w-5 -mx-0.5')]"
# String containing the language
MANGADEX_CHAPTER_TOP_LEVEL_INNER_LANGUAGE_ATTR = "title"
# Link to chapter
MANGADEX_CHAPTER_TOP_LEVEL_INNER_URL_ATTR = "href"

# This is actually looking for "Pg. 1 / 2"
MANGADEX_PAGE_COUNT_CLASS = "//div[contains(@class, 'flex-grow')]"
MANGADEX_PAGE_COUNT_XPATH = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]"
MANGADEX_PAGE_KEYWORD_START = "Pg."
MANGADEX_PAGE_KEYWORD_END = "\n"
# 1 / 11 slash is the delimiter
MANGADEX_PAGE_DELIM_CURR_TOTAL = "/"
# Image class
MANGADEX_IMAGE_CLASS = "img ls limit-width"
# Image XCLASS
MANGADEX_IMAGE_XCLASS = "//img[contains(@class, '" + MANGADEX_IMAGE_CLASS + "')]"
# Delete image scripte
MANGADEX_IMAGE_DELETE_SCRIPT = """
  if(document.getElementsByClassName(""" + '"' + MANGADEX_IMAGE_CLASS + '"' + """).length > 0) {
    var l = document.getElementsByClassName(""" + '"' + MANGADEX_IMAGE_CLASS + '"' + """)[0];
    l.parentNode.removeChild(l);
  }
"""
# Attribute containing the blob url
MANGADEX_IMAGE_BLOB_ATTR = "src"
# Next image visibility attribute
MANGADEX_IMAGE_VISIBILITY_ATTR = "style"
MANGADEX_IMAGE_VISIBILITY_ATTR_NOT_VISIBLE_VALUE = "display: none"
# Next image button 
MANGADEX_NEXT_IMAGE_BUTTON_XCLASS = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/button[2]"

# The following are for webtoons
# <outer>
#   <overflow wrapper>
#     <img>
MANGADEX_WEBTOON_OUTER_XCLASS = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div"
MANGADEX_WEBTOON_OUTER_OVERFLOW_XCLASS = ".//*"

# CHange the view type (eg. single page, double page) button
# Single Page -> Double Page -> Long Strip -> Wide Strip
MANGADEX_CHANGE_READER_TYPE = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[7]/button[1]"

# MangaUpdates XCLASS
MANGADEX_MANGAUPDATES_XCLASS = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[9]/div[2]/div[1]/div[8]/div[2]/a[1]"
MANGADEX_MANGAUPDATES_ATTRIBUTE = "href"
"""--- END MANAGDEX CONSTANTS ---"""

"""--- BEGIN MANGAHERE CONSTANTS ---"""
# Title location
MANGAHERE_TITLE_XPATH = "/html/body/div[5]/div/div[2]/p[1]/span[1]"

# Description might need to be expanded
MANGAHERE_DESCRIPTION_XPATH = "/html/body/div[5]/div/div[2]/p[4]"
MANGAHERE_DESCRIPTION_MORE_XPATH = "/html/body/div[5]/div/div[2]/p[4]/a"

# Categories outer xpath
MANGAHERE_CATEGORIES_OUTER_XPATH = '/html/body/div[5]/div/div[2]/p[3]'

# Chapters XPATH
MANGAHERE_CHAPTERS_OUTER_XPATH =  "/html/body/div[6]/div/div[1]/div[2]/div/ul"
# 'Expand' button for Chapters XPATH
MANGAHERE_CHAPTERS_EXPAND_BUTTON_XPATH = "/html/body/div[6]/div/div[1]/div[2]/div/div/a"
# Chapter's individual element within outer
MANGAHERE_CHAPTERS_OUTER_INNER_TAG = "li"
# Chapter's link tag
MANGAHERE_CHAPTERS_OUTER_INNER_LINK_TAG = "a"
# Chapter's link attribute
MANGAHERE_CHAPTERS_OUTER_INNER_LINK_ATTR = "href"

# Cover image XPATH
MANGAHERE_COVER_IMAGE_XPATH = "/html/body/div[5]/div/div[1]/img"

# Page buttons outer XPATH
MANGAHERE_PAGE_BUTTONS_OUTER_XPATH = "/html/body/div[5]/div/span"
# Contains the links to various pages or left right buttons
MANGAHERE_PAGE_BUTTONS_INNER_TAG = "a"

# Hide yd-mask overlay thingy script
MANGAHERE_HIDE_OVERLAY_SCRIPT = """
  if(document.getElementsByClassName("yd-mask").length > 0) {
    var l = document.getElementsByClassName("yd-mask")[0];
    l.parentNode.removeChild(l);
  }
"""
# Hide danmaku XPATH
MANGAHERE_HIDE_DANMAKU_XPATH = "/html/body/div[13]/a[2]"
MANGAHERE_SHOW_DANMAKU_XPATH = "/html/body/div[12]/a"
# Chapter Image XPATH
MANGAHERE_CHAPTER_IMAGE_XPATH = "/html/body/div[7]/div/img"
"""--- END START PER SOURCE CONSTANTS ---"""

"""--- BEGIN MANGAUPDATES CONSTANTS ---"""
# Link to click to view all translated chapters
MANGAUPDATES_MAIN_PAGE_TRANSLATED_CHAPTERS_LINK_XCLASS = "//a[contains(@rel, 'nofollow')]"
MANGAUPDATES_MAIN_PAGE_TRANSLATED_CHAPTERS_LINK_ATTRIBUTE = "href"
# Must contain the following substring for it to list the releases
MANGAUPDATES_MAIN_PAGE_TRANSLATED_CHAPTERS_LINK_SUBSTR = "https://www.mangaupdates.com/releases.html?search="
# The column containing all the chapter numbers
MANGAUPDATES_TRANSLATED_PAGE_CHAPTERS_XCLASS = "//div[contains(@class, 'col-1 text text-center')]/span"
# The next button XPATH when we have 40 items per page
MANGAUPDATES_TRANSLATED_PAGE_CHAPTERS_NEXT_40_PER_XCLASS = "/html/body/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div[207]/div/div[3]/a"
"""--- END MANGAUPDATES CONSTANTS ---"""