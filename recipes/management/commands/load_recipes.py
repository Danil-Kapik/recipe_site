from django.core.management.base import BaseCommand
from recipes.models import Recipe, Ingredient, Category, User

class Command(BaseCommand):
    help = 'Заполняет таблицу Recipe тестовыми данными'

    def handle(self, *args, **options):
        recipes_data = [
        {
        "id": 1,
        "title": "Блинчики",
        "description": "Тонкие домашние блинчики на молоке.",
        "instructions": "Смешайте муку, молоко, яйца и сахар. Выпекайте на сковороде.",
        "cooking_time": 20,
        "preparation_time": 10,
        "difficulty": "easy",
        "servings": 4,
        "category": 1,
        "image": "recipes/images/blinchiki.jpg",
        "author": 1,
        "video_url": "http://example.com/video1",
        "source_url": "http://example.com/blinchiki"
      },
      {
        "id": 2,
        "title": "Салат Цезарь",
        "description": "Классический салат с курицей, салатом и сыром.",
        "instructions": "Смешайте листья салата, курицу, гренки, сыр и заправьте соусом.",
        "cooking_time": 10,
        "preparation_time": 15,
        "difficulty": "medium",
        "servings": 2,
        "category": 3,
        "image": "recipes/images/caesar.jpg",
        "author": 2,
        "video_url": "http://example.com/video2",
        "source_url": "http://example.com/caesar"
      },
      {
        "id": 3,
        "title": "Шоколадный торт",
        "description": "Пышный торт с шоколадной глазурью.",
        "instructions": "Испеките бисквит, покройте глазурью и украсьте.",
        "cooking_time": 40,
        "preparation_time": 20,
        "difficulty": "hard",
        "servings": 8,
        "category": 4,
        "image": "recipes/images/chocolate_cake.jpg",
        "author": 1,
        "video_url": "http://example.com/video3",
        "source_url": "http://example.com/chocolate_cake"
      }
        ]

        for recipe_data in recipes_data:
            # Получение связанных объектов
            category = Category.objects.get(id=recipe_data['category'])
            author = User.objects.get(id=recipe_data['author'])
            ingredients = Ingredient.objects.filter(id__in=recipe_data['ingredients'])

            # Создание рецепта
            recipe = Recipe.objects.create(
                title=recipe_data['title'],
                description=recipe_data['description'],
                instructions=recipe_data['instructions'],
                cooking_time=recipe_data['cooking_time'],
                preparation_time=recipe_data['preparation_time'],
                difficulty=recipe_data['difficulty'],
                servings=recipe_data['servings'],
                category=category,
                image=recipe_data['image'],
                author=author,
                video_url=recipe_data['video_url'],
                source_url=recipe_data['source_url']
            )
            recipe.ingredients.set(ingredients)
            recipe.total_time = recipe.cooking_time + recipe.preparation_time
            recipe.save()

        self.stdout.write(self.style.SUCCESS('Таблица Recipe успешно заполнена'))