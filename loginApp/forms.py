from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


from .models import *


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        storage = Storage.objects.create()
        storage.save()
        user.storage_id = storage.pk
        user.moderator = False
        if commit:
            user.save()
        return user


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.formstate = 'update'
        if 'formstate' in kwargs:
            self.formstate = kwargs.pop('formstate')
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True if self.formstate == 'view' else False

    class Meta:
        model = Category
        fields = ['name']

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        name = cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Hianyzo adatok")

    def save(self, commit=True):
        category = super(CategoryForm, self).save(commit=False)
        category.name = self.cleaned_data['name']

        if commit:
            category.save()
        return category


class AllergiesFrom(ModelForm):
    def __init__(self, *args, **kwargs):
        self.formstate = 'update'
        if 'formstate' in kwargs:
            self.formstate = kwargs.pop('formstate')
        super(AllergiesFrom, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True if self.formstate == 'view' else False


    class Meta:
        model = Allergies
        fields = ('name', 'tej', 'gluten', 'hus', 'tojas')

    def clean(self):
        cleaned_data = super(AllergiesFrom, self).clean()
        name = cleaned_data.get('name')
        tej = cleaned_data.get('tej')
        gluten = cleaned_data.get('gluten')
        hus = cleaned_data.get('hus')
        tojas = cleaned_data.get('tojas')
        if not name and not tej and not gluten and not hus and not tojas:
            raise forms.ValidationError("Hianyzo adatok")

    def save(self, commit=True):
        allergies = super(AllergiesFrom, self).save(commit=False)
        allergies.name = self.cleaned_data['name']
        allergies.tej = self.cleaned_data['tej']
        allergies.gluten = self.cleaned_data['gluten']
        allergies.hus = self.cleaned_data['hus']
        allergies.tojas = self.cleaned_data['tojas']

        if commit:
            allergies.save()
        return allergies


class RecipeForm(ModelForm):
    masked_id = forms.HiddenInput()

    def __init__(self, *args, **kwargs):
        self.formstate = 'update'
        if 'formstate' in kwargs:
            self.formstate = kwargs.pop('formstate')
        super(RecipeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True if self.formstate == 'view' else False
        self.fields['category'].empty_label = None
        self.fields['allergies'].empty_label = None

    class Meta:
        model = Recipe
        fields = ("name", "description", "category", "difficulty", "allergies", "image",)

    def clean(self):
        cleaned_data = super(RecipeForm, self).clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        category = cleaned_data.get('category')
        difficulty = cleaned_data.get('difficulty')
        allergies = cleaned_data.get('allergies')
        image = cleaned_data.get('image')
        if not name and not description and not category and not difficulty and not allergies:
            raise forms.ValidationError("Hianyzo adatok!")
        if 1 >= difficulty <= 5:
            raise forms.ValidationError("nehézség csak 1-5 lehet")

    def save(self, commit=True):
        recipe = super(RecipeForm, self).save(commit=False)
        recipe.name = self.cleaned_data['name']
        recipe.description = self.cleaned_data['description']
        recipe.category = self.cleaned_data['category']
        recipe.difficulty = self.cleaned_data['difficulty']
        recipe.allergies = self.cleaned_data['allergies']
        recipe.image = self.cleaned_data['image']

        if commit:
            recipe.save()
        return recipe


class IngredientForm(ModelForm):
    name = forms.ChoiceField(choices=[(iter.pk, iter.name) for iter in AllIngredients.objects.all()], widget=forms.Select(attrs={"onchange": "nameChanged(this,'ingredient')"}))
    unit = forms.ChoiceField(choices=[(iter.pk, iter.measure) for iter in PreIngredients.objects.filter(group=AllIngredients.objects.get(pk=1).group)])
    recipe_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    storage_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.formstate = 'update'
        self.selected_name_id = 0
        if 'formstate' in kwargs:
            self.formstate = kwargs.pop('formstate')
        if 'selected_name_id' in kwargs:
            self.selected_name_id = kwargs.pop('selected_name_id')

        super(IngredientForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].disabled = True if self.formstate == 'view' else False
        try:
            unit_choices = [(iter.pk, iter.measure) for iter in PreIngredients.objects.filter(group=AllIngredients.objects.get(pk=self.selected_name_id).group)]
            self.fields['unit'].choices = unit_choices
        except AllIngredients.DoesNotExist as e:
            print("nem kerdezheto le a unit lista", e)

    class Meta:
        model = Ingredient
        fields = ['name', 'measure', 'unit']

    def clean(self):
        cleaned_data = super(IngredientForm, self).clean()
        name = cleaned_data.get('name', None)
        unit = cleaned_data['unit']
        measure = cleaned_data['measure']
        recipe_id = cleaned_data['recipe_id']
        storage_id = cleaned_data['storage_id']
        print(recipe_id, storage_id)
        if not name and not unit and not measure:
            raise forms.ValidationError('Hianyzo adatok')
        if not recipe_id and not storage_id:
            raise forms.ValidationError('A hozzavalo nem tartozik sem recepthez, sem raktarhoz')

    def save(self, commit=True):
        ing = super(IngredientForm, self).save(commit=False)
        ing.name = AllIngredients.objects.get(pk=self.cleaned_data['name']).name
        ing.unit = PreIngredients.objects.get(pk=self.cleaned_data['unit']).measure
        ing.measure = self.cleaned_data['measure'] * PreIngredients.objects.get(pk=self.cleaned_data['unit']).multiply
        if self.cleaned_data['recipe_id']:
            ing.recipe = Recipe.objects.get(pk=self.cleaned_data['recipe_id'])
        if self.cleaned_data['storage_id']:
            ing.storage = Storage.objects.get(pk=self.cleaned_data['storage_id'])

        if commit:
            ing.save()
        return ing