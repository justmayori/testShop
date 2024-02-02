from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from main.models import Product
from .forms import CartAddProductForm, OrderForm
from .models import Order
import random
from webshop.settings import MONOBANK_TOKEN
import requests


# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id) 
    form =CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id) 
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial=
                                                          {'quantity':item['quantity'],
                                                           'override':True})
    return render(request, 'cart/detail.html', {'cart': cart})


def order(request):
    return render(request, 'cart/order_page.html')

def monobank_payment():
    headers = {
    'X-Token': MONOBANK_TOKEN,
    }

    redirect_url = 'http://127.0.0.1:8000/cart/order/orderconf/'

    res = requests.post('https://api.monobank.ua/api/merchant/invoice/create', headers=headers, json = {
        'amount': 10000,
        'ccy': 840,
        'redirectUrl': redirect_url,
    })

    print(res.text)

    if res.status_code == 200:
    
        response_json = res.json()
    
        page_url = response_json.get('pageUrl', None)

    return page_url

    
def created_order(request):
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            random_order_number = random.randint(1000, 9999)
            form.instance.order_number = random_order_number
            form.save()

            request.session['order_number'] = random_order_number
            print('order created')
            order_number = request.session.get('order_number')

            page_url = monobank_payment()
            return redirect(page_url)

    else:
        form = OrderForm()
        
    return render(request, 'cart/order_confirm.html', {'form': form})

