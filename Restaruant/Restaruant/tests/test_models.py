import unittest
from django.test import TestCase
from Management.models import foodtype

class SettingsTestCase(TestCase):
    def setup(self):
        foodtype.objects.create(type="french")
        foodtype.objects.create(type="German")
