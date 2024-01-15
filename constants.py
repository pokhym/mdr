from enum import Enum

class TargetLanguageEnum(Enum):
  ENGLISH = 1

""" --- BEGIN METADATA FILE NAME ---"""
METADATA_FILE_NAME = "metadata.txt"

"""--- BEGIN TARGET LANGUAGE ---"""
TARGET_LANGUAGE = TargetLanguageEnum.ENGLISH
"""--- END TARGET LANGUAGE ---"""

"""--- BEGIN SOURCE NAMES ---"""
SOURCE_MANGADEX = "MangaDex"
"""--- END SOURCE NAMES ---"""

"""--- START PER SOURCE CONSTANTS ---"""

"""--- BEGIN MANADEX CONSTANTS ---"""
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
# Image XCLASS
MANGADEX_IMAGE_XCLASS = "//img[contains(@class, 'img sp limit-width limit-height mx-auto')]"
# Attribute containing the blob url
MANGADEX_IMAGE_BLOB_ATTR = "src"
# Next image visibility attribute
MANGADEX_IMAGE_VISIBILITY_ATTR = "style"
MANGADEX_IMAGE_VISIBILITY_ATTR_NOT_VISIBLE_VALUE = "display: none"
# Next image button 
MANGADEX_NEXT_IMAGE_BUTTON_XCLASS = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/button[2]"
"""--- END MANADEX CONSTANTS ---"""

"""--- END START PER SOURCE CONSTANTS ---"""