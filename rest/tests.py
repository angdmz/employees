from django.test import TestCase
from business.models import *
from rest.services import *

# Create your tests here.

class TestExpander(TestCase):

    def setUp(self) -> None:
        self.boss_boss = Employee.objects.create(first='someones', last='boss boss')
        self.boss = Employee.objects.create(first='someones', last='boss', manager=self.boss_boss)
        self.some_guy = Employee.objects.create(first='someone', last='cool', manager=self.boss)

    def test_expander(self):
        expander = ModelExpander()
        res = self.some_guy.__dict__
        expander.expand(self.some_guy,['manager','manager'], res)
        self.assertTrue(isinstance(res, dict))
        self.assertTrue('manager' in res)
        self.assertTrue(isinstance(res['manager'], dict))
        self.assertTrue('manager' in res['manager'])
        self.assertTrue(isinstance(res['manager']['manager'], dict))
