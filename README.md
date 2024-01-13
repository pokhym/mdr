# tachiyomicompanion

PC tool to replace the auto-update/download features of Tachiyomi extensions post v0.15.2.

This serves as a tool to help collate content for PLEXing to official Tachiyomi extensions.

Currently targeting the Komga official extension.


## Dependencies

Because I'm dumb and don't know how to do anything web development wise, I am farming out the GET requests to Python.

### Python Dependencies

* `pip install selenium`

## Files/Structure

* `webpage_utils.py`
  * Handles pulling JavaScript webpages
  * Handles downloading of images