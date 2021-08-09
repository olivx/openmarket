from django.core.management import BaseCommand

from api.services.load_data import LoadData


class Command(BaseCommand):
    def handle(self, *args, **options):
        LoadData(options["file"]).execute()

    def add_arguments(self, parser):
        parser.add_argument("-f", action="store", dest="file", help="""File location""")
