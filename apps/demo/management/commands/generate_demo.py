import logging

from demo.services import DemoService
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logging.info("Generating demo ...")
        DemoService.generate_demo_dictionary()
        logging.info("Demo generated with success.")
