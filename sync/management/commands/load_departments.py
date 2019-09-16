import os

from django.core.management import BaseCommand
import json

from business.models import Department, Office


class Command(BaseCommand):
    department_manager = Department.objects
    office_manager = Office.objects

    def add_arguments(self, parser):
        parser.add_argument('json_file', help='Departments json file path', type=str)

    def handle(self, *args, **options):
        if os.path.exists(options['json_file']):
            with open(options['json_file']) as f:
                departments = json.load(f)
                loaded = {}
                for d in departments:
                    department_object, updated = self.department_manager.update_or_create(pk=d['id'],
                                                                                 defaults={
                                                                                    'name' : d['name']
                                                                                 })
                    self.stdout.write("Department loaded: {}, was inserted: {}".format(str(department_object), str(updated)))
                    loaded[d['id']] = {'superdepartmentid':d['superdepartment'], 'department':department_object, }

                for k, v in loaded.items():
                    if v['superdepartmentid'] is not None:
                        v['department'].superdepartment_id = v['superdepartmentid']
                        v['department'].save()
                        self.stdout.write(
                            "Superdepartment loaded: {}, was inserted: {}".format(str(v['department']),
                                                                                         str(v['superdepartmentid'])))
        else:
            self.stdout.write("ERROR, not a valid parameter")
            raise NotADirectoryError(options['json_file'] + "is not a directory")