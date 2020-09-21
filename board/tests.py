from django.test import TestCase
from board import models
# Create your tests here.

models.select_order({'g_no': 4, 'parent_no': 11})
