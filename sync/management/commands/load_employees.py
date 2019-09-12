from django.core.management import BaseCommand
from django.conf import settings
import json, requests

from business.models import Employee,  Office, Department


class Command(BaseCommand):
    employee_manager = Employee.objects
    office_manager = Office.objects
    department_manager = Department.objects

    def add_arguments(self, parser):
        parser.add_argument('--url', help='Employees endpoint', type=str)
        parser.set_defaults(url=settings.EMPLOYEES_SOURCE_URL)

    def handle(self, *args, **options):
        res = requests.get(options['url'])
        if res.status_code == 200:
            employees = json.loads(res.content.decode())
            loaded = {}
            for e in employees:
                employee_object, updated = self.employee_manager.update_or_create(
                    pk=e['id'],
                    defaults={
                        'first': e['first'],
                        'last': e['last'],
                        'office_id': e['office'],
                        'department_id': e['department']
                    })
                self.stdout.write("Employee loaded: {}, was inserted: {}".format(str(employee_object), str(updated)))
                loaded[e['id']] = {'managerid':e['manager'], 'employee':employee_object, }

            for k, v in loaded.items():
                if v['managerid'] is not None:
                    v['employee'].manager_id = v['managerid']
                    v['employee'].save()
                    self.stdout.write(
                        "Employee brute manager loaded: {}, was inserted: {}".format(str(v['employee']), str(v['managerid'])))

        else:
            self.stdout.write("ERROR, request with response status code not 200, res: {}".format(str(res)))
            raise NotADirectoryError(options['json_file'] + "is not a directory")