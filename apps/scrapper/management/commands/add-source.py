from django.core.management.base import BaseCommand, CommandError
from apps.scrapper.scrapper import AnnonceListScrapper
from apps.scrapper.models import Cible
from apps.scrapper.models import Url


class Command(BaseCommand):
    help='add new source-pattern mapping'

    def add_arguments(self, parser):
        parser.add_argument('domain', nargs='+', type=str)
        parser.add_argument('target', nargs='+', type=str)


    def handle(self, *args, **options):
        try:
            cible = Cible(DOMAINE=options['domain'][0], CIBLE=options['target'][0])
            cible.save()
        except Exception as e:
            print('ERREUR : ', e)  
