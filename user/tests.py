from django.test import TestCase
from user import models


obj = models.login({"email": "123156", "password": "123123"})
print(len(obj))
