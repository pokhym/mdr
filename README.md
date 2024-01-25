# mdr

PC tool to replace the auto-update/download features of Tachiyomi extensions post v0.15.2.
This serves as a tool to help collate content for PLEXing to self hosted content servers such as Kavita/Komga and is intended to be used with them.

Currently supports

* Operating Systems
  * Linux
  * Windows
* Sources
  * MangaDex
  * MangaHere (except those marked as 18+)

## Dependencies

* `pip install selenium`
  * Used to render JavaScript webpages
  * Used to navigate/parse HTML pages
  * Used to interact with JavaScript pages
* Gecko driver: Obtain the one for your architecture
  * `https://github.com/mozilla/geckodriver/releases`
* Firefox
  * Make sure this is installed and place wherever you wish

## Usage

If you are using Windows make sure in `constants.py` the following are correctly set.
Below is an example.

```
FIREFOX_BIN_PATH = "C:/Program Files/Mozilla Firefox/firefox.exe"
GECKO_BIN_PATH = "./geckodriver.exe"
```

If you are using Linux make sure in `constants.py` the following are correctly set
Below is an example.

```
GECKO_BIN_PATH = "/snap/bin/geckodriver"
```

This is currently a work in progress and can be buggy (specifically if `MAX_THREADS` is not 1 in `main.py`) due to webpage load times.
APIs are not used when accessing MangaDex meaning that the page is loaded and parsed with Selenium instead.
For examples of how to download a specific chapter/title, refer to `test_handler_mangadex.py`.

If you run into problems with timeouts causing exceptions please modify `SLEEP_SEC` in `constant.py`.
This governs how long `selenium` waits before it decides to fail.

For trying to batch download run `main.py`.
This requires a file (by default `library_links.txt`) located in the root directory.
Feel free to change constants in `main.py` to modify behavior.
It's format is like

```
https://mangadex.org/title/XXXX
https://mangadex.org/title/XXXX
https://mangadex.org/title/XXXX
https://mangadex.org/title/XXXX
https://mangahere.cc/manga/XXXX
https://mangahere.cc/manga/XXXX
https://mangahere.cc/manga/XXXX
https://mangahere.cc/manga/XXXX
```

If you have a `.tachibk` file, extract it and parse it with `grab_urls.sh`.

## Files/Structure

* `comic_info.py`
  * Generates a `ComicInfo.xml` per chapter
* `constants.py`
  * Global constants used throuhout the project
* `grab_urls.sh`
  * Parses an unzipped tachibk file to extract certain source's links
    * Supported
      * MangaDex
      * MangaHere
* `handler_mangadex.py`
  * Handles MangaDex titles
* `handler_mangahere.py`
  * Handles MangaHere titles
* `handler.py`
  * General handler which all all other handlers inherit from
* `main.py`
  * Main wrapper
* `test_handler_mangadex.py`
  * Tests for `handler_mangadex.py`
* `test_handler_mangahere.py`
  * Tests for `handler_mangahere.py`
* `title_metadata.py`
  * Metadata for a title and its chapters used in the `Handler`
* `utils.py`
  * General utility functions
* `webpage_utils.py`
  * General scratch file

## TODOs

* Add migration
* Remove timeouts for explicit waits?
  * MangaHere
* Add other sources
* More metadata
  * Status of publishing
  * Capture content type in MangaDex? (eg. Suggestive)
* Create a UI to handle everything with PySimpleGUI?
* Manual redownloading feature if a download fails
