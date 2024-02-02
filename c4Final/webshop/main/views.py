from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ReviewForm
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from .models import *
from cart.forms import CartAddProductForm
from math import ceil
from random import sample

from django.core.paginator import Paginator
# Create your views here.

def get_recently_viewed_products(request):
    recently_viewed_qs = Product.objects.filter(pk__in=request.session.get("recently_viewed", []))
    print("qs", recently_viewed_qs)
    return sorted(recently_viewed_qs, key=lambda x: request.session["recently_viewed"].index(x.id))

def home(request):
    recently_viewed_qs = get_recently_viewed_products(request)
    all_products = Product.objects.all()
    random_five_products = sample(list(all_products), min(5, len(all_products)))
    return render(request, 'main/home.html', {'products':random_five_products, 'recently_viewed': recently_viewed_qs})

def recently_viewed(request, product_id):
    if not "recently_viewed" in request.session:
        request.session["recently_viewed"] = []
        request.session["recently_viewed"].append(product_id)
    else:
        if product_id in request.session["recently_viewed"]:
            request.session["recently_viewed"].remove(product_id)
        request.session["recently_viewed"].insert(0, product_id)
        if len(request.session["recently_viewed"]) > 5:
            request.session["recently_viewed"].pop()
    request.session.modified =True

def product_detail(request, category_name, pk):
    product = get_object_or_404(Product, category__name=category_name, pk=pk)
    images = Image.objects.filter(product=product)
    stats = Stats.objects.filter(product=product)
    reviews = Review.objects.filter(product=product)
    cart_product_form =CartAddProductForm()

    recently_viewed(request, pk)
    recently_viewed_qs = get_recently_viewed_products(request)

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            
            if form.is_valid():
            
                review = form.save(commit=False)
                review.product = product
                review.save()
        else:
            form = ReviewForm()
    elif not request.user.is_authenticated:
        form = ReviewForm()

    return render(request, 'main/product_page.html', {'product': product, 'images': images, \
                                                 'stats': stats, 'reviews': reviews, 'user': request.user ,
                                                 'cart_product_form': cart_product_form, \
                                                 'recently_viewed': recently_viewed_qs, 'form': form})

def get_categories():
    categories = Category.objects.all()
    return {'categories': categories}

def category_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products_by_category = Product.objects.filter(category=category)
    page = request.GET.get('page')
    if not page:
        page = 1
    else:
        page = int(page)

    count_on_one_page = 2
    count_pages = range(1, ceil(len(products_by_category) / count_on_one_page) + 1)
    return render(request, 'main/category.html', {'products_by_category':products_by_category[count_on_one_page * (page - 1):count_on_one_page * page],
                                                         'count_pages': count_pages, 'category': category,
                                                        })

    
def search_product(request):
    queryset = Product.objects.all()
    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) 
        ).distinct()

        paginator = Paginator(queryset, 2) 
        page = request.GET.get('page', 1)

        try:
            current_page = paginator.page(page)
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)

        context = {
            "queryset": current_page,
            'count_pages': paginator.page_range,
            'q': query
        }
        return render(request, 'main/search_product.html', context)
    return render(request, 'main/search_product.html')


def all_reviews(request, category_name, pk):
    product = get_object_or_404(Product, category__name=category_name, pk=pk)
    reviews = Review.objects.filter(product=product)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            print("xddsds")
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.save()
        else:
            form = ReviewForm()
    elif not request.user.is_authenticated:
        form = ReviewForm()
    return render(request, 'main/all_reviews.html', {'product': product, 'reviews': reviews, 'form': form})


