from django.core.management.base import BaseCommand, CommandError
from apps.scrapper.scrapper import AnnonceListScrapper
from apps.scrapper.scrapper import AnnonceScrapper
from apps.scrapper.models import Url


class Command(BaseCommand):
    help='From a search URL, load all add urls'

    def add_arguments(self, parser):
        parser.add_argument(
           '--all', 
           action='store_true', 
           help='load all ad urls with ATTENTE status',
        )        

    def handle(self, *args, **options):
        if options['all']:
            # Get all ATTENTE Urls
            urls_attente = Url.objects.filter(STATUS = 'ATTENTE')
            for url in urls_attente:
                AnnonceScrapper(url)
