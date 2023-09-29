import csv
from django.core.management.base import BaseCommand
from courses.models import Graduate


class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not Graduate.objects.filter(registration_number=row["registration_number"]).exists():
                    Graduate.objects.create(**row)
