from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
from .forms import ProductOrderForm
from .models import ProductOrder


def place_order(request):
    
    if request.method == 'POST':
        form = ProductOrderForm(request.POST)
        print(f'{form.is_valid()=}')

        if form.is_valid():
            orderdata = ProductOrder()
            orderdata.product_type = form.cleaned_data['product_type']

def index(request):
    
    # return redirect('index')
    return render(request, 'tabletest/index.html')


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")