import json
import os.path
import logging

from dictionaries.factories import CategoryFactory, DictionaryFactory, WordFactory
from dictionaries.models import Word
from profiles.factories import ProfileFactory


class DemoService:
    @staticmethod
    def generate_demo_dictionary(jsonfile="words.json"):
        logging.info("service generate_demo_dictionary called")
        profile = ProfileFactory(user__email="anonymous@example.fr")
        category = CategoryFactory(name="English Example")
        dictionary = DictionaryFactory(profile=profile, category=category)
        dir_name = os.path.dirname(__file__)
        file_name = os.path.join(dir_name, jsonfile)
        try:
            with open(file_name, 'r', encoding="utf-8") as file_:
                words_list = json.load(file_)
            for word in words_list:
                Word.objects.create(dictionary=dictionary, **word)
        except Exception as e:
            logging.error(e)
        return dictionary
