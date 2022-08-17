from dictionaries.factories import CategoryFactory, DictionaryFactory, WordFactory
from dictionaries.models import Category, Dictionary, Word
from django.db.utils import IntegrityError
from django.test import TestCase
from profiles.factories import ProfileFactory


class CategoryModelTests(TestCase):
    def test_category_creation(self):
        self.assertEqual(Category.objects.count(), 0)
        category = Category.objects.create(name="test")
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.name, "test")

    def test_category_creation_without_name(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create()

    def test_category_str(self):
        category = CategoryFactory(name="test")
        self.assertEqual(category.__str__(), "test")


class DictionaryModelTests(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.category = CategoryFactory(name="Test")

    def test_dictionary_creation(self):
        self.assertEqual(Dictionary.objects.count(), 0)
        dictionary = Dictionary.objects.create(
            profile=self.profile, category=self.category
        )
        self.assertEqual(Dictionary.objects.count(), 1)
        self.assertEqual(dictionary.profile, self.profile)
        self.assertEqual(dictionary.category.name, "Test")
        self.assertEqual(dictionary.words.count(), 0)

    def test_dictionary_creation_without_profile(self):
        with self.assertRaises(IntegrityError):
            Dictionary.objects.create(category=self.category)

    def test_dictionary_creation_without_category(self):
        with self.assertRaises(IntegrityError):
            Dictionary.objects.create(profile=self.profile)

    def test_dictionary_str(self):
        self.profile.user.email = "test@example.fr"
        self.profile.user.save()
        dictionary = DictionaryFactory(profile=self.profile, category=self.category)
        self.assertEqual(dictionary.words.count(), 0)
        self.assertEqual(dictionary.__str__(), "Test - 0 - test@example.fr")


class WordModelTests(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.category = CategoryFactory(name="Test")
        self.dictionary = DictionaryFactory(
            category=self.category, profile=self.profile
        )

    def test_word_creation(self):
        self.assertEqual(Word.objects.count(), 0)
        word = Word.objects.create(
            dictionary=self.dictionary, title="Test"
        )
        self.assertEqual(Word.objects.count(), 1)
        self.assertEqual(word.title, "Test")
        self.assertEqual(word.dictionary, self.dictionary)
        self.assertEqual(word.definition, "")
        self.assertFalse(word.is_known)
        self.assertIsNone(word.last_played)

    def test_word_creation_without_dictionary(self):
        with self.assertRaises(IntegrityError):
            Word.objects.create(title="Test")

    def test_word_factory_creation_empty(self):
        self.assertEqual(Word.objects.count(), 0)
        word = WordFactory()
        self.assertEqual(Word.objects.count(), 1)
        self.assertIn("title", word.title)
        self.assertIsNotNone(word.dictionary)

    def test_word_str(self):
        word = WordFactory(title="example")
        self.assertEqual(word.__str__(), "example")
