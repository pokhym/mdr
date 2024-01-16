if [[ $# -ne 1 ]] then
  echo "Extracts the urls from a tachibk file"
  echo "Currently supports MangaDex, MangaHere, and Batoto"
  echo "Expects 1 argument being the path to the extracted .tachibk file"
  echo "Must provide the path to an extracted tachibk file!"
  echo "eg. ./grab_urls.sh eu.kanade.atchiyomi_XXXX-XX-XX_XX-XX"
  exit 1
fi

# uploads.mangadex.org/cover
#   - MangaDex
# /manga/
#   - MangaHere
# /series/
#   - Batoto
grep -a -e "uploads.mangadex.org/covers" -e "/manga/" -e "/series/" $1 | while read -r line ; do
  if [[ $(echo ${line} | grep -a -e "uploads.mangadex.org/covers" | wc -l) -eq 1 ]] then
    # A=""
    # echo "1"
    # Remove the beginning of the url
    STRIP="${line#*https://uploads.mangadex.org/covers/}"
    # Extract only the ID of the manga
    if [[ $(echo "${STRIP}" | grep -a -e ".jpg" | wc -l) -eq 1 ]] then
      STRIP2="${STRIP%.jpg*}"
    elif [[ $(echo "${STRIP}" | grep -a -e ".png" | wc -l) -eq 1 ]] then
      STRIP2="${STRIP%.png*}"
    else
      echo "UNKNOWN COVER TYPE: ${line}"
      exit 1
    fi
    
    STRIP3="https://mangadex.org/title/"$STRIP2
    echo "${STRIP3}"
  elif [[ $(echo $line | grep -a -e "mangahere" | wc -l) -eq 1 ]] then
    STRIP="${line#*/manga/}"
    STRIP2="${STRIP%%/*}"
    STRIP3="https://mangahere.cc/manga/"$STRIP2
    echo "${STRIP3}"
    # echo "MangaHere!"
    # echo "----"
  fi
done

