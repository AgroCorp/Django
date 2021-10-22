import json
import logging

from django.contrib import messages  # import messages
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from . import forms
from . import utils
from .serialize import ApiModelSerializer
from .models import Recipe, Allergies, Category, Ingredient, PreIngredients, AllIngredients, APIModel, CustomUser
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from imap_tools import MailBox, AND

imap = MailBox(settings.IMAP_HOST).login(settings.IMAP_USERNAME, settings.IMAP_PASSWORD)

logger = logging.getLogger(__name__)


# Create your views here.


@login_required(login_url="/recipes/login?next=/recipes/recipe_list")
def homepage(request):
    return render(request, "loginApp/home.html")


def permission_denied(request):
    if request.method == 'GET':
        perm_codename = request.GET.get('perm', None)
    if perm_codename:
        perm = Permission.objects.get(codename=perm_codename)

    return render(request, 'loginApp/permissionPopUp.html', {'perm': perm})


@api_view(['POST'])
@csrf_exempt
def save_api_call(request):
    if request.method == 'POST':
        saveserialize = ApiModelSerializer(data=request.data)
        if saveserialize.is_valid():
            saveserialize.save()
            return Response(saveserialize.data, status=status.HTTP_201_CREATED)


def recipe_to_pdf(request, recipe_id):
    recipe_id = settings.FERNET.decrypt(recipe_id.encode()).decode()
    recipe_obj = Recipe.objects.get(pk=recipe_id)
    ings = Ingredient.objects.filter(recipe_id=recipe_id)
    pdf = utils.render_to_pdf('../templates/sablon/recipe.html', {'recipe': recipe_obj, 'ings': ings})
    return FileResponse(pdf, content_type='application/pdf')


@login_required(login_url="/recipes/login?next=/recipes/recipe_list")
def recipe_list(request):
    lista = Recipe.objects.all().order_by('name', 'difficulty')
    page_number = request.GET.get('page')
    page_count = request.GET.get('count', 10)

    paginator = Paginator(lista, page_count)

    # unseen emails list from imap
    emails = [msg for msg in imap.fetch(AND(seen=False))]

    print(len(emails))

    page_obj = paginator.get_page(page_number)

    return render(request, "loginApp/recipes.html", {'QuerySet': page_obj, 'per_page': page_obj.paginator.per_page})


def register_request(request):
    if request.method == "POST":
        form = forms.NewUserForm(request.POST, initial={"moderator": False})
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, "Registration successful.")
            plaintext = get_template('loginApp/email.txt')
            htmly = get_template('loginApp/emailTemplate.html')

            subject, from_email, to_email = 'registration successfully', 'noreply@sativus.space', user.email

            token = settings.FERNET.encrypt(str(user.pk).encode()).decode()

            text_content = plaintext.render({'user': user})
            html_content = htmly.render({'user': user, 'link': f"http://192.168.2.10:8000/recipes/activation?token={token}"})

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

            return render(request, 'loginApp/activationComplete.html', {})
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return render(request=request, template_name="loginApp/register.html", context={"register_form": form})
    form = forms.NewUserForm
    return render(request=request, template_name="loginApp/register.html", context={"register_form": form})


def activation(request):
    if request.method == "GET":
        user_id = request.GET.get('token', None)
        if user_id:
            real_user_id = settings.FERNET.decrypt(user_id.encode()).decode()
            user = CustomUser.objects.get(pk=real_user_id)
            if user:
                user.is_active = True
                user.save()
                messages.success(request, 'Sikeresen aktivaltad a fiokod')
                return redirect(to='loginApp:homepage')


@login_required(login_url="/recipes/login?next=/recipes/recipe_list")
@permission_required(raise_exception=False, login_url='/recipes/permission?perm=change_allergies',
                     perm="change_allergies")
def update_allergie(request, allergies_id):
    obj = get_object_or_404(Allergies, id=allergies_id)
    if request.method == "POST":
        form = forms.AllergiesFrom(request.POST, instance=obj, formstate='update')
        if form.is_valid():
            instance = form.save()
            # return redirect("loginApp:allergies")
            return HttpResponse(
                '<script>opener.closePopup(window, "%s", "%s", "#id_allergie");</script>' % (instance.pk, instance))
        else:
            messages.error(request, "Hiba történt a mentés során")
            return render(request, "loginApp/allergies_detail.html", {"form": form, 'obj_id': obj.pk})
    else:
        form = forms.AllergiesFrom(instance=obj, formstate='update')
    return render(request, "loginApp/allergies_detail.html", {"form": form, 'obj_id': obj.pk})


@csrf_exempt
def get_allergies_id(request):
    if request.is_ajax():
        allergies_name = request.GET['name']
        allergies_id = Allergies.objects.get(name=allergies_name).pk
        data = {'allergies_id': allergies_id, }

        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def view_allergie(request, allergies_id):
    obj = get_object_or_404(Allergies, id=allergies_id)
    form = forms.AllergiesFrom(request.POST, instance=obj, formstate='view')
    return render(request, "loginApp/allergies_detail.html", {"form": form})


def add_allergie(request):
    if request.method == "POST":
        form = forms.AllergiesFrom(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.info(request, "Mentés sikeres!")
            # return redirect("loginApp:allergies")
            return HttpResponse(
                '<script>opener.closePopup(window, "%s", "%s", "#id_allergies");</script>' % (instance.pk, instance))
        else:
            messages.error(request, "hiba törtent a mentés soran")
            return render(request, "loginApp/allergies_detail.html", {"form": form})
    form = forms.AllergiesFrom()
    return render(request, "loginApp/allergies_detail.html", {"form": form})


def del_allergies(request, allergies_id):
    obj = Allergies.objects.get(pk=allergies_id)
    obj.delete()
    return HttpResponse(
        '<script>opener.closePopupDel(window, "%s", "%s", "#id_allergies");</script>' % (obj.pk, obj))


def api_login(request):
    username = request.GET.get("username", None)
    if username:
        try:
            user_in_api_table = APIModel.objects.get(username=username)
            user = CustomUser.objects.get(username=username)
            current_date = timezone.now()
            if user_in_api_table.valid_to > current_date and user.rfid_id == user_in_api_table.rfid_id:
                login(request, user)
            else:
                user_in_api_table.delete()
                messages.error(request, "RFID belepes sikertelen (lejart az ido vagy a kartya azonosito nem egyezik)")
                form = AuthenticationForm()
                return render(request=request, template_name="loginApp/login.html", context={"login_form": form})

            if user.is_authenticated:
                user_in_api_table.delete()

            return redirect("loginApp:homepage")
        except APIModel.DoesNotExist:
            messages.error(request, "RFID belepes sikertelen")
            form = AuthenticationForm()
            return render(request=request, template_name="loginApp/login.html", context={"login_form": form})

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


def login_request(request):
    next_url = request.GET.get("next", None)
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Sikeresen bejelentkeztél {username}.")
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect("loginApp:recipes")
                else:
                    messages.error(request, "Meg nem aktivaltad a fiokod")
            else:
                messages.error(request, "Hibás felhasználónév vagy jelszó")
        else:
            messages.error(request, "Hibás felhasználónév vagy jelszó")
    form = AuthenticationForm()
    return render(request=request, template_name="loginApp/login.html", context={"login_form": form})


@login_required(login_url="/recipes/login?next=/recipes/recipe_list")
def add_recipe(request):
    if request.method == "POST":
        form = forms.RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Mentés sikeres!")
            return redirect("loginApp:recipes")
        else:
            messages.error(request, "hiba törtent a mentés soran")
            return render(request, "loginApp/add_recipe.html", {"recipe_form": form})
    form = forms.RecipeForm()
    return render(request, "loginApp/add_recipe.html", {"recipe_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Sikeresen kijelentkeztél")
    return redirect("loginApp:homepage")


def allergiesList(request):
    obj = Allergies.objects.all().order_by('pk')
    paginator = Paginator(obj, 10)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, "loginApp/allergies.html", {"QuerySet": obj, "page_obj": page_obj})


def get_ingredient_list_by_recipeId(recipe_id):
    ings = Ingredient.objects.filter(recipe_id=recipe_id)
    groups = []
    for ing in ings:
        group = PreIngredients.objects.get(measure=ing.unit).group
        groups.append((ing, group))
    return groups


@login_required(login_url="/recipes/login?next=/recipes/recipe_list")
def update_recipe(request, recipe_id):
    real_recipe_id = settings.FERNET.decrypt(recipe_id.encode()).decode()
    obj = get_object_or_404(Recipe, id=real_recipe_id)
    groups = get_ingredient_list_by_recipeId(real_recipe_id)
    if request.method == "POST":
        form = forms.RecipeForm(request.POST or None, request.FILES or None, instance=obj, formstate='update')
        if form.is_valid():
            form.save()
            messages.success(request, 'Sikeres mentes')
            return redirect(reverse('loginApp:recipe_edit', kwargs={'recipe_id': recipe_id}))
        else:
            messages.error(request, "Hiba történt a mentés során")
            return render(request, "loginApp/detail.html", {"recipe": form, "ings": groups, 'recipe_obj': obj})
    else:
        form = forms.RecipeForm(instance=obj, formstate='update')
    return render(request, "loginApp/detail.html", {"recipe": form, "ings": groups, 'recipe_obj': obj})


def delete_recipe(request, recipe_id):
    real_recipe_id = settings.FERNET.decrypt(recipe_id.encode()).decode()
    obj = get_object_or_404(Recipe, id=real_recipe_id)
    obj.delete()
    return redirect(reverse("loginApp:recipes"))


def view_recipe(request, recipe_id):
    real_recipe_id = settings.FERNET.decrypt(recipe_id.encode()).decode()
    obj = get_object_or_404(Recipe, id=real_recipe_id)
    groups = get_ingredient_list_by_recipeId(real_recipe_id)
    form = forms.RecipeForm(request.POST, request.FILES, instance=obj, formstate='view')
    return render(request, "loginApp/detail.html", {"recipe": form, "recipe_obj": obj, 'ings': groups})


def categoryList(request):
    objs = Category.objects.all()
    paginator = Paginator(objs, 10)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, "loginApp/categories.html", context={"QuerySet": objs, 'page_obj': page_obj})


def add_category(request):
    if request.method == "POST":
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.info(request, "Mentés sikeres!")
            # return redirect("loginApp:allergies")
            return HttpResponse(
                '<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))
        else:
            messages.error(request, "hiba törtent a mentés soran")
            return render(request, "loginApp/category_detail.html", {"form": form})
    form = forms.CategoryForm()
    return render(request, "loginApp/category_detail.html", {"form": form})


def get_category_id(request):
    if request.is_ajax():
        category_name = request.GET['name']
        category_id = Category.objects.get(name=category_name).pk
        data = {'category_id': category_id, }
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def view_category(request, category_id):
    obj = get_object_or_404(Category, id=category_id)
    form = forms.CategoryForm(request.POST, instance=obj, formstate='view')
    return render(request, "loginApp/category_detail.html", {"form": form})


def update_category(request, category_id):
    obj = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = forms.CategoryForm(request.POST, instance=obj, formstate='update')
        if form.is_valid():
            instance = form.save()
            # return redirect("loginApp:allergies")
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>'
                                % (instance.pk, instance))
        else:
            messages.error(request, "Hiba történt a mentés során")
            return render(request, "loginApp/category_detail.html", {"form": form, 'obj_id': obj.pk})
    else:
        form = forms.CategoryForm(instance=obj, formstate='update')
    return render(request, "loginApp/category_detail.html", {"form": form, 'obj_id': obj.pk})


def del_category(request, category_id):
    obj = Category.objects.get(pk=category_id)
    obj.delete()
    return HttpResponse(
        '<script>opener.closePopupDel(window, "%s", "%s", "#id_category");</script>' % (obj.pk, obj))


def ingredientList(request):
    objs = Ingredient.objects.all().order_by('pk')
    paginator = Paginator(objs, 2)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, "loginApp/ingredients.html", context={"QuerySet": objs, 'page_obj': page_obj})


def add_ingredient(request):
    form = forms.IngredientForm(selected_name_id=1)
    if request.method == "GET":
        recipe_id = request.GET.get("recipe_id")
        storage_id = request.GET.get('storage_id')
        selected_name_id = request.GET.get('selected_name_id')
        form = forms.IngredientForm(selected_name_id=selected_name_id,
                                    initial={"name": selected_name_id, "recipe_id": recipe_id,
                                             'storage_id': storage_id})
        return render(request, "loginApp/ingredient_detail.html", {"form": form})
    if request.method == "POST":
        selected_name_id = request.POST.get('name')
        form = forms.IngredientForm(request.POST, selected_name_id=selected_name_id)
        if form.is_valid():
            print('storage_id:', form.cleaned_data['storage_id'])
            print('recipe_id:', form.cleaned_data['recipe_id'])
            instance = form.save()
            messages.info(request, "Mentés sikeres!")
            # return redirect("loginApp:allergies")
            return HttpResponse(
                '<script>opener.closePopup(window, "%s", "%s", "#id_ingredient");</script>' % (instance.pk, instance))
        else:
            messages.error(request, "hiba törtent a mentés soran")
            return render(request, "loginApp/ingredient_detail.html", {"form": form})
    return render(request, "loginApp/ingredient_detail.html", {"form": form})


def view_ingredient(request, ingredient_id):
    obj = get_object_or_404(Ingredient, id=ingredient_id)
    all_ingredient = get_object_or_404(AllIngredients, name=obj.name).pk
    form = forms.IngredientForm(instance=obj, formstate='view', selected_name_id=all_ingredient)
    return render(request, "loginApp/ingredient_detail.html", {"form": form})


def update_ingredient(request, ingredient_id):
    obj = Ingredient.objects.get(pk=ingredient_id)
    all_ingredient = get_object_or_404(AllIngredients, name=obj.name)
    pre_ingredient = get_object_or_404(PreIngredients, measure=obj.unit)
    form = forms.IngredientForm(instance=obj, selected_name_id=all_ingredient.pk,
                                initial={'name': all_ingredient.pk,
                                         'measure': obj.measure / pre_ingredient.multiply,
                                         'unit': pre_ingredient.pk,
                                         'recipe_id': obj.recipe_id,
                                         'storage_id': obj.storage_id})
    if request.method == "GET":
        if 'selected_name_id' in request.GET and ('recipe_id' in request.GET or 'storage_id' in request.GET):
            recipe_id = request.GET.get("recipe_id")
            storage_id = request.GET.get('storage_id')
            selected_name_id = request.GET.get('selected_name_id')
            form = forms.IngredientForm(selected_name_id=selected_name_id,
                                        initial={"name": selected_name_id, "recipe_id": recipe_id,
                                                 'storage_id': storage_id})
            return render(request, "loginApp/ingredient_detail.html", {"form": form})
        else:
            return render(request, "loginApp/ingredient_detail.html", {"form": form, })
    elif request.method == 'POST':
        selected_name_id = request.POST.get('name')
        form = forms.IngredientForm(request.POST, instance=obj, selected_name_id=selected_name_id,
                                    initial={'name': all_ingredient.pk,
                                             'measure': obj.measure,
                                             'unit': pre_ingredient.pk,
                                             'recipe_id': obj.recipe_id,
                                             'storage_id': obj.storage_id})

        if form.is_valid():
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>'
                                % (instance.pk, instance))
        else:
            messages.error(request, "Hiba történt a mentés során")
            return render(request, "loginApp/category_detail.html", {"form": form})
    return render(request, "loginApp/ingredient_detail.html", {"form": form})


def delete_ingredient(request, ingredient_id):
    parent = request.GET.get('parent', '/')
    Ingredient.objects.get(pk=ingredient_id).delete()
    return redirect(parent)


def get_ingredient_list_by_storage_id(storage_id):
    ings = Ingredient.objects.filter(storage_id=storage_id)
    groups = []
    for ing in ings:
        group = PreIngredients.objects.get(measure=ing.unit).group
        groups.append((ing, group))

    return groups


def storage(request):
    storage_pk = request.user.storage
    groups = get_ingredient_list_by_storage_id(storage_pk)

    return render(request, 'loginApp/storage.html', {'ings': groups})
