# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import get_object_or_404

from django.db import models
from utils.utils import *
from utils.templator import work_dir_archive_path

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    birthday = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    post = models.CharField(max_length=50)

    def __str__(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.patronymic)

    def contacts(self):
        return "%s, %s" % (self.phone, self.email)


class Reviewer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    diplom = models.CharField(max_length=20)
    post = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)

    def __str__(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.patronymic)

class Department(models.Model):
    full_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20)
    head_first_name = models.CharField(max_length=100)
    head_last_name = models.CharField(max_length=100)
    head_patronymic = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % (self.short_name)

    @classmethod
    def write_table_to_csv(cls):
        import csv
        resultFile = open("output.csv", 'a')
        wr = csv.writer(resultFile, dialect='excel')

        for d in Department.objects.all():
            wr.writerows([[d.full_name, d.short_name, d.head_first_name, d.head_last_name, d.head_patronymic]])

    def get_head(self):
        return ("%s. %s. %s") % (self.head_last_name, self.head_first_name[0], self.head_patronymic[0])


class Article(models.Model):
    title = models.CharField(max_length=255)
    udk = models.CharField(max_length=100)
    main_author = models.ForeignKey(Author, related_name='article')
    reviewer = models.ForeignKey(Reviewer)
    authors = models.ManyToManyField(Author, related_name='author_articles')
    department = models.ForeignKey(Department)

    @classmethod
    def create(cls, **kwargs):
        if "json" in kwargs:
            article = Article()
            json = kwargs.get("json")

            r = Reviewer(**json["reviewer"])
            r.save()

            authors = []
            for author_json in json["authors"]:
                a = Author(**author_json)
                a.save()
                authors.append(a)

            article.title = json["title"]
            article.udk = json["udk"]
            article.reviewer = r
            article.department = get_object_or_404(Department, short_name=json["department"])
            article.main_author = authors[0]

            article.save()
            article.authors = authors
            return article


class Archieve(models.Model):
    identifier = models.CharField(max_length=64, unique=True)
    path = models.FilePathField()
    name = models.CharField(max_length=32)

    @classmethod
    def create(cls, file_name):
        path = work_dir_archive_path(file_name)
        identifier = id_generator(path)

        a = Archieve(path=path, identifier=identifier, name=file_name)
        a.save()
        return a
