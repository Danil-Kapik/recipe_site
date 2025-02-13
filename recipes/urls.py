from django.urls import path
from .views import *


app_name = 'recipes'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    # Units
    path('units/', UnitListView.as_view(), name='unit-list'),
    path('units/create/', UnitCreateView.as_view(), name='unit-create'),
    path('units/<int:pk>/update/', UnitUpdateView.as_view(), name='unit-update'),
    path('units/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit-delete'),
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    # Ingredients
    path('ingredients/', IngredientListView.as_view(), name='ingredient-list'),
    path('ingredients/create/', IngredientCreateView.as_view(), name='ingredient-create'),
    path('ingredients/<int:pk>/update/', IngredientUpdateView.as_view(), name='ingredient-update'),
    path('ingredients/<int:pk>/delete/', IngredientDeleteView.as_view(), name='ingredient-delete'),
    # Recipes
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipes/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe-update'),
    path('recipes/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipes/<int:pk>/detail/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/<int:pk>/restore/', recipe_restore, name='recipe-restore'),
]