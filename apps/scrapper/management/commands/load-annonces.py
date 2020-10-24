from django.core.management.base import BaseCommand, CommandError
from apps.scrapper.scrapper import AnnonceListScrapper
from apps.scrapper.scrapper import AnnonceScrapper
from apps.scrapper.models import Url


class Command(BaseCommand):
    help='scrappe all ATTENTE urls in Url table, if --one is passed, only scrappe the given ad url'

    def add_arguments(self, parser):

        parser.add_argument(
           '--one', 
           '-o',
           action='store_true',
           help='load data from a single add passed in argument',
        )        

        parser.add_argument(
           '--url', 
           '-u',
           type=str,
           help='target url for --one argument',
        )        

    def handle(self, *args, **options):
        if options['one']:
            pass

        else:
            # Get all ATTENTE Urls
            for url in Url.objects.filter(STATUS = 'ATTENTE'):
                AnnonceScrapper(url)

