from django.contrib import admin
from .models import Unit, Category, Ingredient, Recipe, RecipeIngredient, FavoriteRecipe

# Unit
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

    def __str__(self):
        return self.name

# Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)
    ordering = ('name',)

# Ingredient
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('unit',)
    ordering = ('name',)

    def __str__(self):
        return self.list_filter


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ['ingredient']

# Recipe
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description_short', 'difficulty', 'author', 'created_at', 'updated_at', 'is_archived')
    list_display_links = ('title',)
    search_fields = ('title', 'description')
    list_filter = ('difficulty', 'category', 'author', 'created_at', 'is_archived')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    inlines = [RecipeIngredientInline]

    def description_short(self, obj):
        return obj.description[:50] + '...'

    def get_queryset(self, request):
        return Recipe.all_objects.select_related('author').prefetch_related('recipe_ingredients__ingredient')
        # return super().get_queryset(request)


# RecipeIngredient
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')
    search_fields = ('recipe__title', 'ingredient__name')
    list_filter = ('recipe', 'ingredient')

@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__title')
    list_filter = ('user', 'recipe')
