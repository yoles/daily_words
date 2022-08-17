from django.test import TestCase
from dictionaries.models import Dictionary
from django.core.management import call_command


class DemoTests(TestCase):
    def test_generate_demo_command(self):
        self.assertEqual(Dictionary.objects.count(), 0)
        call_command('generate_demo')
        self.assertEqual(Dictionary.objects.count(), 1)
