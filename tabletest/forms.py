from django import forms

from .models import ProductOrder


class ProductOrderForm(forms.ModelForm):
    class Meta:
        model = ProductOrder
        fields = [
            'product_type',
        ]