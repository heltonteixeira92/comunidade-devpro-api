import argparse

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'import os autores a partir de csv'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'))

    def handle(self, *args, csv, **kwargs):
        self.stdout.write('ok')
