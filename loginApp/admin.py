from django.contrib import admin
from .models import Recipe, Allergies, Ingredient, CustomUser, Category

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Allergies)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Category)

class Media:
    js = (
        ''
    )