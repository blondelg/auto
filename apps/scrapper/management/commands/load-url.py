from django.core.management.base import BaseCommand, CommandError
from apps.scrapper.scrapper import AnnonceListScrapper
from apps.scrapper.models import Url


class Command(BaseCommand):
    help='from a seach url, load all ad urls. if --one argiment is passed, load only the inputed url'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)
        parser.add_argument(
           '--one', 
           '-o',
           action='store_true', 
           help='load one url inputed',
        )        


    def handle(self, *args, **options):

        if options['one']:
            url = Url(URL = options['url'][0])
            # get target from URL
            url.CIBLE = url.get_target_from_url()
            # save url
            try:
                url.save()
            except:
                print('ad already recorded')

        else:
            url = Url(URL = options['url'][0])
            AnnonceListScrapper(url.URL)

