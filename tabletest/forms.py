from django import forms

from .models import ProductOrder


class ProductOrderForm(forms.ModelForm):
    # goods = forms.CharField(max_length=50)

    class Meta:
        model = ProductOrder
        # fields = [
        #     'product_type',
        # ]
        fields = '__all__'

    # apply bootstrap to django form
    def __init__(self, *args, **kwargs):
        super(ProductOrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
