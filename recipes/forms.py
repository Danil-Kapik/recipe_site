# forms.py
from django import forms
from django.forms.models import inlineformset_factory
from .models import RecipeIngredient, Ingredient, Unit, Recipe

class RecipeIngredientForm(forms.ModelForm):
    ingredient_name = forms.CharField(max_length=100, label="Название ингредиента")
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), label="Единица измерения")

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient_name', 'quantity', 'unit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['ingredient_name'].initial = self.instance.ingredient.name
            self.fields['unit'].initial = self.instance.ingredient.unit

    def clean(self):
        cleaned_data = super().clean()
        ingredient_name = cleaned_data.get('ingredient_name')
        unit = cleaned_data.get('unit')
        if ingredient_name and unit:
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_name,
                defaults={'unit': unit}
            )
            cleaned_data['ingredient'] = ingredient
        return cleaned_data

    def save(self, commit=True):
        self.instance.ingredient = self.cleaned_data.get('ingredient')
        return super().save(commit=commit)

RecipeIngredientFormSet = inlineformset_factory(
    Recipe, RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
    can_delete=True
)
