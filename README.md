# tachiyomicompanion

PC tool to replace the auto-update/download features of Tachiyomi extensions post v0.15.2.

This serves as a tool to help collate content for PLEXing to official Tachiyomi extensions.

Currently targeting the Kavita official extension.


## Dependencies

Because I'm dumb and don't know how to do anything web development wise, I am farming out the GET requests to Python.

### Python Dependencies

* `pip install selenium`

## Files/Structure

* `constants.py`
  * Global constants used throuhout the project
* `handler_mangadex.py`
  * Handles MangaDex titles
* `handler.py`
  * General handler which all all other handlers inherit from
* `test_handler_mangadex.py`
  * Tests for `handler_manadex.py`
* `utils.py`
  * General utility functions
* `webpage_utils.py`
  * General scratch file

## TODOs

* Global time.sleep() value
* Compress to cbz in python
* Add ComicInfo.xml for all chapters
  * Include metadata
* Add covers to all chapters
* Add other sources
* Create a store to store all the currently existing ongoing stories
* More metadata
  * Status of publishing
* Create a UI to handle everything with PySimpleGUI?
* Manual redownloading feature if a download fails
* Logging to know what was done on each session