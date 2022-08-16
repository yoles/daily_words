import factory
from dictionaries.models import Dictionary, Category, Word
from profiles.factories import ProfileFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Sequence(lambda n: f"name{n}")


class DictionaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dictionary
    category = factory.SubFactory(CategoryFactory)
    profile = factory.SubFactory(ProfileFactory)


class WordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Word

    dictionary = factory.SubFactory(DictionaryFactory)
    title = factory.Sequence(lambda n: f"title{n}")