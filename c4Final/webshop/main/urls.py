from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_product, name='search_product'),
    path('<str:category_name>/<int:pk>/', product_detail, name='product'),
    path('<str:category_name>/<int:pk>/all_reviews/', all_reviews, name='all_reviews'),
    # path('<str:category_name>/<int:pk>/<slug:product_name>/add_review/', add_review, name='add_review'),
    path('<str:category_name>/', category_view, name='category'),
]