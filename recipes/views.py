from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
import random
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Unit, Category, Ingredient, Recipe
from .forms import RecipeIngredientFormSet


class HomeView(ListView):
    model = Recipe
    template_name = "recipes/index.html"
    context_object_name = "random_recipes"

    def get_queryset(self):
        queryset = super().get_queryset()
        # Преобразуем QuerySet в список и выбираем 3 случайных элемента
        random_recipes = random.sample(list(queryset), min(3, queryset.count()))
        return random_recipes


# Unit Views
class UnitListView(ListView):
    model = Unit
    template_name = "recipes/unit_list.html"
    context_object_name = "units"


class UnitCreateView(CreateView):
    model = Unit
    template_name = "recipes/unit_form.html"
    fields = ['name']
    success_url = reverse_lazy('recipes:unit-list')


class UnitUpdateView(UpdateView):
    model = Unit
    template_name = "recipes/unit_update_form.html"
    fields = ['name']
    success_url = reverse_lazy('recipes:unit-list')


class UnitDeleteView(DeleteView):
    model = Unit
    template_name = "recipes/unit_confirm_delete.html"
    success_url = reverse_lazy('recipes:unit-list')


# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = "recipes/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(CreateView):
    model = Category
    template_name = "recipes/category_form.html"
    fields = ['name', 'parent']
    success_url = reverse_lazy('recipes:category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = "recipes/category_update_form.html"
    fields = ['name', 'parent']
    success_url = reverse_lazy('recipes:category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "recipes/category_confirm_delete.html"
    success_url = reverse_lazy('recipes:category-list')


# Ingredient Views
class IngredientListView(ListView):
    model = Ingredient
    template_name = "recipes/ingredient_list.html"
    context_object_name = "ingredients"


class IngredientCreateView(CreateView):
    model = Ingredient
    template_name = "recipes/ingredient_form.html"
    fields = ['name', 'unit']
    success_url = reverse_lazy('recipes:ingredient-list')


class IngredientUpdateView(UpdateView):
    model = Ingredient
    template_name = "recipes/ingredient_update_form.html"
    fields = ['name', 'unit']
    success_url = reverse_lazy('recipes:ingredient-list')


class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = "recipes/ingredient_confirm_delete.html"
    success_url = reverse_lazy('recipes:ingredient-list')


# Recipe Views
class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = Recipe.all_objects.filter(is_archived=False)
        if query:
            queryset = queryset.filter(title__icontains=query)
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['category'] = Category.objects.all()
        context['total_recipes'] = self.get_queryset().count()
        context['total_pages'] = context['paginator'].num_pages if context.get('paginator') else 1
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"


class RecipeCreateView(CreateView):
    model = Recipe
    template_name = "recipes/recipe_form.html"
    fields = [
        'title', 'description', 'instructions', 'cooking_time',
        'preparation_time', 'difficulty', 'servings', 'category', 
        'image', 'author'
    ]
    success_url = reverse_lazy('recipes:recipe-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredients'] = RecipeIngredientFormSet(self.request.POST)
        else:
            context['ingredients'] = RecipeIngredientFormSet()
        return context

    def form_valid(self, form):
        # Устанавливаем автора рецепта
        form.instance.author = self.request.user
        self.object = form.save()
        context = self.get_context_data()
        ingredients = context['ingredients']
        if ingredients.is_valid():
            ingredients.instance = self.object
            ingredients.save()
        return super().form_valid(form)


class RecipeUpdateView(UpdateView):
    model = Recipe
    template_name = "recipes/recipe_form.html"
    fields = [
        'title', 'description', 'instructions', 'cooking_time',
        'preparation_time', 'difficulty', 'servings', 'category', 
        'image', 'author',
    ]
    success_url = reverse_lazy('recipes:recipe-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredients'] = RecipeIngredientFormSet(self.request.POST, instance=self.object)
        else:
            context['ingredients'] = RecipeIngredientFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data()
        ingredients = context['ingredients']
        if ingredients.is_valid():
            ingredients.instance = self.object
            ingredients.save()
        return super().form_valid(form)


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = "recipes/recipe_confirm_delete.html"
    success_url = reverse_lazy('recipes:recipe-list')


def recipe_restore(request, pk):
    recipe = get_object_or_404(Recipe.all_objects, pk=pk)
    recipe.is_archived = False
    recipe.save()
    return redirect('recipes:recipe-list')

