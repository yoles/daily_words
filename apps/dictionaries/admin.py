from django.contrib import admin

from dictionaries.models import Category, Dictionary, Word


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ["__str__"]


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    model = Dictionary
    list_display = ["__str__"]


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    model = Word
    list_display = ["__str__"]
    list_filter = ('is_known', 'last_played')

