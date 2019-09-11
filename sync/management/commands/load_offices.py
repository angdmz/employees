import os

from django.core.management import BaseCommand
import json

from business.models import Office


class Command(BaseCommand):
    office_manager = Office.objects

    def add_arguments(self, parser):
        parser.add_argument('json_file', help='Offices json file path', type=str)

    def handle(self, *args, **options):
        if os.path.exists(options['json_file']):
            with open(options['json_file']) as f:
                offices = json.load(f)
                for o in offices:
                    office_object = self.office_manager.update_or_create(pk=o['id'],
                                                                         defaults={
                                                                            'city': o['city'],
                                                                            'address': o['address'],
                                                                            'country': o['country'],
                                                                         })
                    self.stdout.write("Office syncronized: {}".format(str(office_object)))
