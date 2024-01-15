# mdr

PC tool to replace the auto-update/download features of Tachiyomi extensions post v0.15.2.
This serves as a tool to help collate content for PLEXing to self hosted content servers such as Kavita/Komga and is intended to be used with them.

## Dependencies

* `pip install selenium`
  * Used to render JavaScript webpages
  * Used to navigate/parse HTML pages
  * Used to interact with JavaScript pages

## Files/Structure

* `comic_info.py`
  * Generates a `ComicInfo.xml` per chapter
* `constants.py`
  * Global constants used throuhout the project
* `grab_urls.sh`
  * Parses an unzipped tachibk file to extract certain source's links
    * Supported
      * MangaDex
* `handler_mangadex.py`
  * Handles MangaDex titles
* `handler.py`
  * General handler which all all other handlers inherit from
* `main.py`
  * Main wrapper
* `test_handler_mangadex.py`
  * Tests for `handler_manadex.py`
* `title_metadata.py`
  * Metadata for a title and its chapters used in the `Handler`
* `utils.py`
  * General utility functions
* `webpage_utils.py`
  * General scratch file

## TODOs

* Add tool to match the mangaupdates status with ones from current sources
  * Add migration
* Remove timeouts for explicit waits?
* Support Windows
* Swap back to Chromium (?) or add search function for Gecko
* Add other sources
* More metadata
  * Status of publishing
* Create a UI to handle everything with PySimpleGUI?
* Manual redownloading feature if a download fails
