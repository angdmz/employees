import os

from django.core.management import BaseCommand
import json

from business.models import Department, DepartmentRelation, Office


class Command(BaseCommand):
    department_manager = Department.objects
    departmentrelation_manager = DepartmentRelation.objects
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
                        relation, r_updated = self.departmentrelation_manager.update_or_create(department=v['department'],
                                                                         defaults={
                                                                             'superdepartment':loaded[v['superdepartmentid']]['department'],
                                                                         })
                        self.stdout.write(
                            "Department relation loaded: {}, was inserted: {}".format(str(relation), str(r_updated)))
        else:
            self.stdout.write("ERROR, not a valid parameter")
            raise NotADirectoryError(options['json_file'] + "is not a directory")