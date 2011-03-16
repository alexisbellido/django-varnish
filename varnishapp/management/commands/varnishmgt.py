from django.core.management.base import BaseCommand
from django.conf import settings
from varnishapp.manager import manager
from pprint import pprint

class Command(BaseCommand):
    def handle(self, *args, **options):
        if args:
            pprint(manager.run(*args, secret=getattr(settings, 'VARNISH_SECRET', None)))
        else:
            print manager.help()
