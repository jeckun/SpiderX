from datetime import date

class Book:
    def __init__(self, story_path : string, author_path : string, publish_date_path : string, category_path : string, label_path : list):
        self.__story_path = story_path
        self.__author_path = author_path
        self.__publish_date_path = publish_date_path
        self.__category_path = category_path
        self.__label_path = label_path
    
    @property
    def story_name(self):
        return self.__story_name