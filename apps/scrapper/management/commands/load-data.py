from django.core.management.base import BaseCommand, CommandError

#  Draft command line
#  Telecharger les données pour toute les annonces
#  > load-data --all


class Command(BaseCommand):
    help='some help'

    def add_arguments(self, parser):
           parser.add_argument(
           '--all', 
           action='store_true', 
           help='charge toute les données',
       )

    def handle(self, *args, **options):
        print('la commande marche')
        if options['all']:
            print('télécharge toute les données')
        
