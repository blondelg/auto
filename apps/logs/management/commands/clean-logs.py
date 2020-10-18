from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from datetime import timedelta
from datetime import datetime
import glob
import os


class Command(BaseCommand):
    help='clean logs orlder than a certain number of days'

    def add_arguments(self, parser):
        parser.add_argument(
           '-d',
           '--days', 
           type = int,
           help = 'maximum log age',
        )


    def handle(self, *args, **options):
        min_age = options.get('days')

        # If min age not passed as argument, get default stored in config
        if not min_age: min_age = int(settings.CONFIG['GENERAL']['LOG_AGE'])
        
        # Logs to keep
        pattern_list = [(datetime.now() - timedelta(days =
            day)).strftime("%Y%m%d") for day in range(min_age)]
        to_keep = [f".log/log_{pat}.txt" for pat in pattern_list] 
        print("DEBUG to_keep : ", to_keep)
        to_delete = [log for log in glob.glob(".log/*") if log not in to_keep]
        print("DEBUG to_delete : ", to_delete)
        # build patterns to keep

        for log in to_delete:
            try:
                print(log)
                os.remove(log)
            except Exception as e:
                settings.LOGGER.error(f"delete log {e}")
                
            





