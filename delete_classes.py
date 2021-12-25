from assignments import models
import json
from urllib.request import urlopen
import datetime


def main(num_classes = None, testing=False):
    models.Class_Item.objects.all().delete()
