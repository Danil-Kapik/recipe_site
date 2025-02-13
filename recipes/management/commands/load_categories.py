from django.core.management.base import BaseCommand
from recipes.models import Category

class Command(BaseCommand):
    help = 'Заполняет таблицу Category тестовыми данными'

    def handle(self, *args, **options):
        categories_data = [
            {"id": 1, "name": "Завтраки", "parent": None},
            {"id": 2, "name": "Обеды", "parent": None},
            {"id": 3, "name": "Салаты", "parent": None},
            {"id": 4, "name": "Десерты", "parent": None}
        ]

        # Создаем корневые категории
        for category_data in categories_data:
            parent = None
            if category_data['parent'] is not None:
                # Если есть родительская категория, то найдем ее
                parent = Category.objects.get(id=category_data['parent'])
            Category.objects.create(name=category_data['name'], parent=parent)
        self.stdout.write(self.style.SUCCESS('Таблица Category успешно заполнена'))