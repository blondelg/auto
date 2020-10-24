from django.core.management.base import BaseCommand, CommandError
from apps.scrapper.scrapper import AnnonceListScrapper
from apps.scrapper.scrapper import AnnonceScrapper
from apps.scrapper.models import Url


class Command(BaseCommand):
    help='scrappe all ATTENTE urls in Url table, scrappe one given url'

    def add_arguments(self, parser):
        parser.add_argument(
           '--all', 
           '-a',
           action='store_true', 
           help='load all ad urls with ATTENTE status',
        )        

        parser.add_argument(
           '--one', 
           '-o',
           type=str,
           help='load data from the given url',
        )        

    def handle(self, *args, **options):
        if options['all']:
            # Get all ATTENTE Urls
            urls_attente = Url.objects.filter(STATUS = 'ATTENTE')
            for url in urls_attente:
                AnnonceScrapper(url)

        else:
            print('DEBUG : ', options['one'])
            # define Url object
            url = Url(URL=options['one'])
            url.CIBLE = url.get_target_from_url()
            # try to scrappe it
            try:
                url.save()
                scrapper = AnnonceScrapper(url)
            except:
                pass
            # record Url object thanks to the result
