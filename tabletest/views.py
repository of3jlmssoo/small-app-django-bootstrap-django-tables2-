from re import I
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from .forms import ProductOrderForm, ConfirmOrderForm
from .models import ProductOrder
from django.contrib import messages
import copy

def set_checkbox_choices(request, context):
    new_context = copy.deepcopy(context)

    # print(f'=> {request.POST=}')
    # 'product_type': ['D'], 'product_use': ['M'], 'alternative': ['true'],
    if request.POST['product_type'] == 'D':
        new_context['daily_goods'] = 'checked'
    elif request.POST['product_type'] == 'L':
        new_context['luxury_goods'] = 'checked'
    else:
        pass

    if request.POST['product_use'] == 'M':
        new_context['personal'] = 'checked'
    elif request.POST['product_use'] == 'F':
        new_context['family'] = 'checked'
    elif request.POST['product_use'] == 'G':
        new_context['gift'] = 'checked'
    else:
        pass

    if request.POST['alternative'] == 'true':
        new_context['alt_available'] = 'checked'
    elif request.POST['alternative'] == 'false':
        new_context['alt_unavailable'] = 'checked'
    else:
        pass


    return  new_context

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
                type_of_estimation=form.cleaned_data['type_of_estimation'],
                product_type=form.cleaned_data['product_type'],
                product_use=form.cleaned_data['product_use'],
                alternative=form.cleaned_data['alternative'],
                expected_purchase_date=form.cleaned_data['expected_purchase_date'],
            )
            order_product.save()

        context = {
            'goods':form.cleaned_data['goods'],
            'product_price':form.cleaned_data['product_price'],
        }
        print(f'=> place order before render {request.POST=}')
    

        initial_dict = dict(goods='hi music', alternative=True)
        form = ConfirmOrderForm(
            initial={
                'goods':request.POST['goods'],
                'product_price':request.POST['product_price'],
                'type_of_estimation':request.POST['type_of_estimation'],
                'product_type':request.POST['product_type'],
                'product_use':request.POST['product_use'],
                'alternative':request.POST['alternative'],
                'expected_purchase_date':request.POST['expected_purchase_date'],
            }
        )

        # context = { 'form': form }
        # context = { 'form': form, 'luxury_goods':'checked', "expected_purchase_date": request.POST['expected_purchase_date']}
        context = { 'form': form,  "expected_purchase_date": request.POST['expected_purchase_date']}

        context = set_checkbox_choices(request, context)


        print(f'=> {context=}')
        return render(request, 'tabletest/confirm_details.html' , context)

    # return redirect('confirm_details')
    # return render(request, 'confirm_details')
    messages.error(request, '入力が正常完了しませんでした。')
    return redirect('/')


def confirm_details(request):
    # print(f'=> confirm_details {request.POST=}')
    form = ConfirmOrderForm(request.POST, initial={'goods': 'Hi there!'})
    return redirect('/')


def index(request):

    form = ProductOrderForm()
    # return redirect('index')
    # return render(request, 'tabletest/index.html')
    return render(request, 'tabletest/index.html', {'form': form})


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# def indexcopy(request):

#     # return redirect('index')
#     form = ProductOrderForm()
#     return render(request, 'tabletest/indexcopy.html', {'form': form})
