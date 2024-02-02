from django.contrib import admin
from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'  # Или перечислите поля, которые вы хотите включить

class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('email', 'name' ,'created_at')
    search_fields = ('email', 'name') 
    list_filter = ('name',) 
    ordering = ('name',)  

admin.site.register(Order, OrderAdmin)
