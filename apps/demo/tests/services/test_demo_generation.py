from django.test import TestCase

from demo.services import DemoService
from dictionaries.models import Dictionary, Word


class DemoTests(TestCase):
    def test_generate_demo_dictionary(self):
        self.assertEqual(Dictionary.objects.count(), 0)
        dictionary = DemoService.generate_demo_dictionary()
        self.assertEqual(Dictionary.objects.count(), 1)
        self.assertEqual(dictionary.profile.user.email, "anonymous@example.fr")
        self.assertFalse(dictionary.profile.user.is_confirm)
        self.assertEqual(dictionary.category.name, "English Example")
        self.assertEqual(dictionary.words.count(), 10)

        first_word: Word = dictionary.words.first()
        self.assertEqual(first_word.title, "shallow")
        self.assertEqual(first_word.definition.lower(), "Superficiel".lower())
        self.assertFalse(first_word.is_known)
        self.assertIsNone(first_word.last_played)

        last_word: Word = dictionary.words.last()
        self.assertEqual(last_word.title, "play")
        self.assertEqual(last_word.definition.lower(), "jouer".lower())
        self.assertFalse(last_word.is_known)
        self.assertIsNone(last_word.last_played)

    def test_generate_demo_dictionary_json_error(self):
        self.assertEqual(Dictionary.objects.count(), 0)
        dictionary = DemoService.generate_demo_dictionary(jsonfile="wrong.json")
        self.assertEqual(Dictionary.objects.count(), 1)
        self.assertEqual(dictionary.words.count(), 0)
