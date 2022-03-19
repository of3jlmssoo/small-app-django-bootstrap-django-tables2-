from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from .forms import ProductOrderForm
from .models import ProductOrder


def place_order(request):

    if request.method == 'POST':

        for item in request.POST:
            key = item
            value = request.POST[key]
            print(f'{key=} {value}')

        print(f'=> place_order() POST!')

        form = ProductOrderForm(request.POST)

        print(f'{form=}')
        print(f'{form.is_valid()=}')
        print(f'{form.cleaned_data=}')

        if form.is_valid():
            # orderdata = ProductOrder()
            # orderdata.product_type = form.cleaned_data['product_type']
            order_product = ProductOrder(
                goods=form.cleaned_data['goods'],
                product_price=form.cleaned_data['product_price'],
                product_type=form.cleaned_data['product_type'],
                product_use=form.cleaned_data['product_use'],
                alternative=form.cleaned_data['alternative'],
                expected_purchase_date=form.cleaned_data['expected_purchase_date'],
            )
            order_product.save()

    return redirect('/')


def index(request):

    form = ProductOrderForm()
    # return redirect('index')
    # return render(request, 'tabletest/index.html')
    return render(request, 'tabletest/index.html', {'form': form})


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def indexcopy(request):

    # return redirect('index')
    form = ProductOrderForm()
    return render(request, 'tabletest/indexcopy.html', {'form': form})
