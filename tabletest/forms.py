from django import forms

from .models import ProductOrder


class ProductOrderForm(forms.ModelForm):
    # goods = forms.CharField(max_length=50)
    alternative = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'style': 'width:25px;height:25;'}))
    orderid = forms.IntegerField(required=False)

    class Meta:
        model = ProductOrder
        # fields = [
        #     'product_type',
        # ]
        fields = '__all__'
        # exclude = ['user', 'status', 'comment']
        exclude = ['user', 'status', ]

    # apply bootstrap to django form

    def __init__(self, *args, **kwargs):
        super(ProductOrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ConfirmOrderForm(forms.ModelForm):
    # ROのフォーム。ただし、comment欄はテンプレート内で条件設定によりRW、ROを設定している
    # https://stackoverflow.com/questions/4662848/disabled-field-is-not-passed-through-workaround-needed

    alternative = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'style': 'width:20px;height:20px;'}))
    orderid = forms.IntegerField(required=False)
    # comment = forms.CharField(required=False)

    class Meta:
        model = ProductOrder
        # fields = [
        #     'product_type',
        # ]
        fields = '__all__'
        # exclude = ['user', 'status', 'comment']
        exclude = ['user', 'status', ]
        # exclude = ['user']

    # apply bootstrap to django form
    def __init__(self, *args, **kwargs):
        super(ConfirmOrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            # print(f'=> {field=}')
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['goods'].widget.attrs['disabled'] = 'disabled'
            self.fields['product_price'].widget.attrs['disabled'] = 'disabled'
            self.fields['type_of_estimation'].widget.attrs['disabled'] = 'disabled'
            self.fields['product_use'].widget.attrs['disabled'] = 'disabled'
            self.fields['product_type'].widget.attrs['disabled'] = 'disabled'
            self.fields['alternative'].widget.attrs['disabled'] = 'disabled'
            self.fields['expected_purchase_date'].widget.attrs['disabled'] = 'disabled'
            self.fields['orderid'].widget.attrs['disabled'] = 'disabled'


class ViewOnlyOrderForm(forms.ModelForm):
    # https://stackoverflow.com/questions/4662848/disabled-field-is-not-passed-through-workaround-needed

    alternative = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'style': 'width:20px;height:20px;'}))
    orderid = forms.IntegerField(required=False)
    # comment = forms.CharField(required=False)

    class Meta:
        model = ProductOrder
        # fields = [
        #     'product_type',
        # ]
        fields = '__all__'
        # exclude = ['user', 'status', 'comment']
        exclude = ['user', 'status', ]
        # exclude = ['user']

    # apply bootstrap to django form
    def __init__(self, *args, **kwargs):
        super(ViewOnlyOrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            print(f'=> {field=}')
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['goods'].widget.attrs['disabled'] = 'disabled'
            self.fields['product_price'].widget.attrs['disabled'] = 'disabled'
            self.fields['type_of_estimation'].widget.attrs['disabled'] = 'disabled'
            self.fields['product_use'].widget.attrs['disabled'] = 'disabled'
            self.fields['product_type'].widget.attrs['disabled'] = 'disabled'
            self.fields['alternative'].widget.attrs['disabled'] = 'disabled'
            self.fields['expected_purchase_date'].widget.attrs['disabled'] = 'disabled'
            self.fields['orderid'].widget.attrs['disabled'] = 'disabled'
            self.fields['comment'].widget.attrs['disabled'] = 'disabled'
