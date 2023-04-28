import os
from random import randint
import django
import ipdb;ipdb.set_trace()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

django.setup()

from faker import factory, Faker
from core.models import *
from model_bakery.recipe import Recipe, foreign_key, related

fake = Faker()

"""Omitted fields will be generated automatically."""
for _ in range(100):
    author = Recipe(Author,
                    name=fake.name(),
                    )
    book = Recipe(Book,
                  name=fake.name(),
                  edition=randint(0, 999),
                  publication_year=fake.year(),
                  authors=related(author),
                  )
