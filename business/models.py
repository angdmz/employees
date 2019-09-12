from django.db import models

# Create your models here.


class Office(models.Model):
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return "Country: {} City: {} Address: {}".format(self.country, self.city, self.address)

    class Meta:
        db_table = 'offices'


# modeling Departments as a DAG, where vertex is Department and edges are the superdepartment relation
class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "departments"


# edges of the graph
class DepartmentRelation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')
    superdepartment = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, related_name='superdepartment')

    def __str__(self):
        return "{} is superdepartment of {}".format(str(self.department), str(self.superdepartment))

    class Meta:
        db_table = "department_relationship"
        unique_together = (('department', 'superdepartment'), )


# modeling Employees as a DAG, where vertex is Employee and edges are the manager relation
class Employee(models.Model):
    first = models.CharField(max_length=25)
    last = models.CharField(max_length=25)
    department = models.ForeignKey(Department,on_delete=models.CASCADE, null=True, default=None, blank=True)
    manager = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True, default=None, blank=True)
    office = models.ForeignKey(Office,on_delete=models.CASCADE, null=True, default=None, blank=True)

    def __str__(self):
        return "{} {}".format(str(self.first), str(self.last))

    class Meta:
        db_table = "employees"
