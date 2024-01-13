"""--- BEGIN SOURCE NAMES ---"""
SOURCE_MANGADEX = "MangaDex"
"""--- END SOURCE NAMES ---"""

"""--- START PER SOURCE CONSTANTS ---"""

"""--- BEGIN MANADEX CONSTANTS ---"""
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