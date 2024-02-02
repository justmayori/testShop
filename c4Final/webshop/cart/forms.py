from django import forms
from .models import Order


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [ 'email', 'name']
    order_number = forms.IntegerField(required=False, widget=forms.HiddenInput())
