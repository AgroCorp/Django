from django.urls import path

from . import views

app_name = 'loginApp'

urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("register/", views.register_request, name='register'),
    path("login/", views.login_request, name='login'),
    path("logout/", views.logout_request, name='logout'),
    path('permission/', views.permission_denied, name='permission'),
    path("allergies/", views.allergiesList, name="allergies"),
    path("allergies/new", views.add_allergie, name='add_allergie'),
    path("allergies/ajax/get_allergies_id", views.get_allergies_id, name='get_allergies_id'),
    path("allergies/<int:allergies_id>/view", views.view_allergie, name="allergies_view"),
    path("allergies/<int:allergies_id>/edit", views.update_allergie, name="allergies_edit"),
    path("allergies/<int:allergies_id>/delete", views.del_allergies, name="allergies_del"),
    path("categories/", views.categoryList, name='categories'),
    path("category/new", views.add_category, name="add_category"),
    path("category/ajax/get_category_id", views.get_category_id, name='get_category_id'),
    path("category/<int:category_id>/view", views.view_category, name='category_view'),
    path("category/<int:category_id>/edit", views.update_category, name="category_edit"),
    path("category/<int:category_id>/delete", views.del_category, name='category_del'),
    path("recipe_list/", views.recipeList, name='recipes'),
    path("recipes/new", views.add_recipe, name='add_recipe'),
    path("recipes/<str:recipe_id>/view", views.view_recipe, name='recipe_view'),
    path("recipes/<str:recipe_id>/edit", views.update_recipe, name='recipe_edit'),
    path("recipes/<str:recipe_id>/pdf", views.recipe_to_pdf, name='recipe_pdf_generate'),
    path("recipes/<str:recipe_id>/delete", views.delete_recipe, name='recipe_delete'),
    path("ingredients/", views.ingredientList, name='categories'),
    path("ingredient/new", views.add_ingredient, name="add_ingredient"),
    path("ingredient/<int:ingredient_id>/view", views.view_ingredient, name='ingredient_view'),
    path("ingredient/<int:ingredient_id>/edit", views.update_ingredient, name="ingredient_edit"),
    path("ingredient/<int:ingredient_id>/delete", views.delete_ingredient, name='ingredient_del'),
    path("login_api/", views.save_api_call, name='login_api'),
    path("login_with_api/", views.api_login, name='login_with_api'),
    path("storage/", views.storage, name='storage')
]
