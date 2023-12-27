import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from VHStore.forms import EquipmentForm, MovieForm, CassetteForm, RegisterForm
from VHStore.models import Cassette, Equipment, Movie, MembershipStatus, CartItem, Cart

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("catalog")
    template_name = "registration/signup.html"


def unknown_page(request):
    return render(request, 'error_page.html', {'message': 'page not found'})


def seller_required(function):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.role == 'seller' or request.user.is_superuser):
            return function(request, *args, **kwargs)
        else:
            return render(request, 'error_page.html', {'message': 'Access Denied'})

    return _wrapped_view


@login_required(login_url="/login/")
@seller_required
def seller_dashboard(request):
    equipments = Equipment.objects.all()
    movies = Movie.objects.all()
    cassettes = Cassette.objects.all()

    if request.method == 'POST':
        equipment_form = EquipmentForm(request.POST, request.FILES)
        movie_form = MovieForm(request.POST, request.FILES)
        cassette_form = CassetteForm(request.POST)

        if equipment_form.is_valid():
            equipment_form.save()

        if movie_form.is_valid():
            movie_form.save()

        if cassette_form.is_valid():
            cassette_form.save()
    else:
        equipment_form = EquipmentForm()
        movie_form = MovieForm()
        cassette_form = CassetteForm()

    context = {
        'equipments': equipments,
        'movies': movies,
        'cassettes': cassettes,
        'equipment_form': equipment_form,
        'movie_form': movie_form,
        'cassette_form': cassette_form,
    }

    return render(request, 'seller_dashboard.html', context)

@login_required(login_url="/login/")
def catalog(request):
    equipments = Equipment.objects.all()
    movies = Movie.objects.all()
    cassettes = Cassette.objects.all()
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = cart.items.all()
    cart_total = 0

    cart_list = []
    for item in cart_items:
        cart_list.append({
            'name':  f"{item.cassette.movie.title} {item.cassette.condition}" if item.cassette else item.equipment.name,
            'price': item.cassette.price if item.cassette else item.equipment.price
        })
        cart_total += item.cassette.price if item.cassette else item.equipment.price

    user_discount = request.user.plan.discount if request.user.is_authenticated else None
    discount_amount = cart_total * user_discount / 100

    context = {
        'equipments': equipments,
        'movies': movies,
        'cassettes': cassettes,
        'cart_list': cart_list,
        'cart_total': cart_total-discount_amount,
        'discount_amount': discount_amount
    }
    return render(request, 'catalog.html', context)

@login_required(login_url="/login/")
def add_to_cart(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        item_id = body["item_id"]
        item_type = body['item_type']  # 'cassette' или 'equipment'

        # Определите, что именно нужно добавить в корзину: кассету или оборудование
        if item_type == 'cassette':
            item = get_object_or_404(Cassette, pk=item_id)
        elif item_type == 'equipment':
            item = get_object_or_404(Equipment, pk=item_id)
        else:
            return JsonResponse({item_type: False})

        # Получите корзину пользователя или создайте новую
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Добавьте товар в корзину

        if item_type == 'cassette':
            new_item = CartItem.objects.create(cassette=item)
            cart.items.add(new_item)
        elif item_type == 'equipment':
            new_item = CartItem.objects.create(equipment=item)
            cart.items.add(new_item)
        return JsonResponse({'success': True})

    return JsonResponse({'successRES': False})

@login_required(login_url="/login/")
def place_order(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()
        cart_items = cart.items.all()
        cart_total = 0

        for item in cart_items:
            cart_total += item.cassette.price if item.cassette else item.equipment.price

        user_discount = request.user.plan.discount if request.user.is_authenticated else None
        discount_amount = cart_total * user_discount / 100
        actual_price = cart_total - discount_amount

        for item in cart_items:
            item.cassette.delete() if item.cassette else item.equipment.delete()
            CartItem.delete(item)

        request.user.total_purchases += actual_price
        request.user.save()

        for status in reversed(MembershipStatus.objects.all()):
            if request.user.total_purchases >= status.milestone:
                request.user.status = status

        return JsonResponse({'success': True})
