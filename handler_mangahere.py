from handler import Handler

class HandlerMangaHere(Handler):
  
  def extract_current_page(self):
    return super().extract_current_page()
  
  def extract_total_pages(self):
    return super().extract_total_pages()
  
  def extract_single_page(self):
    return super().extract_single_page()
  
  def extract_chapter_images(self):
    return super().extract_chapter_images()
  
  def create_comic_info(self):
    # TODO: Move into parent (also handler_mangadex.py)
    return super().create_comic_info()
  
  def create_cbz(self):
    # TODO: Move into parent (also handler_mangadex.py)
    return super().create_cbz()
  
  def extract_title_name(self):
    return super().extract_title_name()
  
  def extract_description(self):
    return super().extract_description()
  
  def extract_categories(self):
    return super().extract_categories()
  
  def extract_chapter_numbers(self):
    return super().extract_chapter_numbers()
  
  def extract_cover(self):
    return super().extract_cover()
  
  def get_update(self):
    return super().get_update()
  