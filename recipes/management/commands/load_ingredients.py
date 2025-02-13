from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Unit

class Command(BaseCommand):
    help = 'Заполняет таблицу Ingredient тестовыми данными'

    def handle(self, *args, **options):
        ingredients_data = [
            {"id": 1, "name": "Мука", "unit_id": 1},
            {"id": 2, "name": "Молоко", "unit_id": 2},
            {"id": 3, "name": "Яйцо", "unit_id": 3},
            {"id": 4, "name": "Сахар", "unit_id": 1},
            {"id": 5, "name": "Масло сливочное", "unit_id": 1},
            {"id": 6, "name": "Курица", "unit_id": 1},
            {"id": 7, "name": "Листья салата", "unit_id": 3},
            {"id": 8, "name": "Гренки", "unit_id": 3},
            {"id": 9, "name": "Сыр", "unit_id": 1},
            {"id": 10, "name": "Шоколад", "unit_id": 1}
        ]

        for ingredient_data in ingredients_data:
            unit = Unit.objects.get(id=ingredient_data['unit_id'])
            Ingredient.objects.create(name=ingredient_data['name'], unit=unit)
        self.stdout.write(self.style.SUCCESS('Таблица Ingredient успешно заполнена'))