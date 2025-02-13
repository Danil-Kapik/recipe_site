from django.core.management.base import BaseCommand
from recipes.models import Unit

class Command(BaseCommand):
    help = 'Заполняет таблицу Unit тестовыми данными'

    def handle(self, *args, **options):
        units_data = [
            {"id": 1, "name": "г"},
            {"id": 2, "name": "л"},
            {"id": 3, "name": "шт"},
            {"id": 4, "name": "мл"}
        ]

        for unit_data in units_data:
            Unit.objects.create(**unit_data)
        self.stdout.write(self.style.SUCCESS('Таблица Unit успешно заполнена'))