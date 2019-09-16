from django.db import models


class Office(models.Model):
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return "Country: {} City: {} Address: {}".format(self.country, self.city, self.address)

    class Meta:
        db_table = 'offices'


class Department(models.Model):
    name = models.CharField(max_length=50)
    superdepartment = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, default=None, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "departments"


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
