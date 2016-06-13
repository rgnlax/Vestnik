# -*- coding: utf-8 -*-

import json, os
from docs.models import Department
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.json')) as data_file:
            data = json.load(data_file)

            for obj in data:
                short_name = obj["short_name"]
                full_name = obj["full_name"]
                head_first_name = obj["first_name"]
                head_last_name = obj["last_name"]
                head_patronymic = obj["patronymic"]


                d = Department(short_name=short_name,
                               full_name=full_name,
                               head_first_name=head_first_name,
                               head_last_name=head_last_name,
                               head_patronymic=head_patronymic)
                try:
                    d.save()
                    print d.short_name
                except:
                    print d.short_name + '-Exception!'

