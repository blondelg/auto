from django.core.management.base import BaseCommand, CommandError
from apps.scrapper.scrapper import AnnonceListScrapper


class Command(BaseCommand):
    help='from a search URL, load all add urls'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)
        parser.add_argument(
           '--all', 
           '-a',
           action='store_true', 
           help='load all ad urls from a give search url',
        )        

    def handle(self, *args, **options):
        if options['all']:
            AnnonceListScrapper(options['url'][0])
