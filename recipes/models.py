from django.db import models
from django.contrib.auth.models import User


class RecipeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=False)

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Units"

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name='subcategories'
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['parent__name', 'name']

    def __str__(self):
        return f"{self.parent.name} -> {self.name}" if self.parent else self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='ingredients')

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ['name']

    def __str__(self):
        return self.name

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ]

    title = models.CharField(max_length=200, unique=True, db_index=True)
    description = models.TextField()
    instructions = models.TextField()
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes", default=1)
    preparation_time = models.PositiveIntegerField(help_text="Preparation time in minutes", default=1)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    servings = models.PositiveIntegerField()
    category = models.ManyToManyField(Category, related_name='recipes')
    image = models.ImageField(upload_to='recipes/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipes')
    total_time = models.PositiveIntegerField(help_text="Total time in minutes", editable=False)
    is_archived = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(Ingredient, related_name='used_in_recipes', through='RecipeIngredient')

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ['-created_at']

    objects = RecipeManager()
    all_objects = models.Manager()

    def delete(self):
        self.is_archived = True
        self.save()

    def save(self, *args, **kwargs):
        self.total_time = self.preparation_time + self.cooking_time
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient_recipes')
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipe Ingredients"
        unique_together = ['recipe', 'ingredient']

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit.name} of {self.ingredient.name}"


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        verbose_name = "Favorite Recipe"
        verbose_name_plural = "Favorite Recipes"
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f"{self.user.username} -> {self.recipe.title}"