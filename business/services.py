from business.models import EmployeeDepartment, EmployeeOffice


class EmployeeAssigner:
    employee_office_manager =  EmployeeOffice.objects
    employee_department_manager =  EmployeeDepartment.objects

    def assign_office(self, employee, office):
        self.employee_office_manager.update_or_create(employee=employee, defaults={'office':office})

    def assign_department(self, employee, department):
        self.employee_department_manager.update_or_create(employee=employee, defaults={'department':department})
