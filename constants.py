"""--- BEGIN SOURCE NAMES ---"""
SOURCE_MANGADEX = "MangaDex"
"""--- END SOURCE NAMES ---"""

"""--- START PER SOURCE CONSTANTS ---"""

"""--- BEGIN MANADEX CONSTANTS ---"""
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
# This is actually looking for "Pg. 1 / 2"
MANGADEX_PAGE_COUNT_CLASS = "//div[contains(@class, 'flex-grow')]"
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