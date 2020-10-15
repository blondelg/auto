from django.core.management.base import BaseCommand, CommandError
from apps.scrapper.scrapper import AnnonceListScrapper
#  Draft command line
#  Telecharger les données pour toute les annonces
#  > load-data --all
#  > load-data --url  --all
#  > load-data --url  --last


class Command(BaseCommand):
    help='some help'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)
        parser.add_argument(
           '--all', 
           action='store_true', 
           help='charge toute les données',
        )        
        parser.add_argument(
           '--last', 
           action='store_true', 
           help='charge toute les données',
        )


    def handle(self, *args, **options):
        if options['all']:
            print(options['url'][0])
            AnnonceListScrapper(options['url'][0])
        if options['last']:
            print('last')
        
