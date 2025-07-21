import json
from django.core.management import BaseCommand
from time import time
from django.conf import settings
from codespace.models import Syntax


def load_data(filepath:str)->dict:
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


class Command(BaseCommand):
    help = "Create Syntaxes Data"

    def handle(self, *args, **options):
        data = []
        syntaxes = load_data(settings.BASE_DIR/"codespace/fixtures/syntaxes.json")
        for syntax in syntaxes['syntaxes']:
            data.append(Syntax(title=syntax['title'] ,description=syntax['description']))
        Syntax.objects.bulk_create(objs=data, ignore_conflicts=True)
        self.stdout.write(
            self.style.SUCCESS("Syntaxes Added Successfully")
        )        