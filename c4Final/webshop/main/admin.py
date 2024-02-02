from django.contrib import admin
from .models import Product, Image, Stats, Category, Review
from django.urls import reverse
from django.utils.http import urlencode

class ImageInline(admin.TabularInline): 
    model = Image


class StatsInline(admin.TabularInline):
    model = Stats


class CategoryInline(admin.TabularInline):
    model = Category 


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
        StatsInline,
    ]
    list_display = ['name','id', 'category', 'price', 'view_reviews_link']
    autocomplete_fields = ['category']
    search_fields = ['name']
    ordering = ['category']
    list_filter = ['name', 'category']

    def view_reviews_link(self, obj):
        from django.utils.html import format_html
        count = obj.review.count()
        url = (
            reverse("admin:main_review_changelist")
            +
            "?"
            +
            urlencode({'product__id': f'{obj.id}'})
        )
        return format_html('<a href="{}">{} Reviews</a>', url, count)
    
    view_reviews_link.short_description = "Reviews"




class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'product_id', 'pub_date')
    search_fields = ['product']
    autocomplete_fields = ['product']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
