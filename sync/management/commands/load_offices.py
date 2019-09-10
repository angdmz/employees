import os

from django.core.management import BaseCommand
import json

from business.models import Office
from sync.models import OfficeLoad


class Command(BaseCommand):
    office_manager = Office.objects
    office_load_manager = OfficeLoad.objects
    office_load_manager = OfficeLoad.objects

    def add_arguments(self, parser):
        parser.add_argument('json_file', help='Offices json file path', type=str)

    def handle(self, *args, **options):
        if os.path.exists(options['json_file']):
            with open(options['json_file']) as f:
                offices = json.load(f)
                for o in offices:
                    office_object = self.office_manager.update_or_create(source_id=o['id'],
                                                                         defaults={
                                                                            'city': o['city'],
                                                                            'address': o['address'],
                                                                            'country': o['country'],
                                                                         })
                    self.stdout.write("Office syncronized: {}".format(str(office_object)))
