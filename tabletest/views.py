# from re import I
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse, Http404

# Create your views here.
from .forms import ProductOrderForm, ConfirmOrderForm
from .models import ProductOrder
from django.contrib import messages
import copy

import django_filters
from django_filters.views import FilterView

from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
from django_tables2.paginators import LazyPaginator


from .tables import (
    Bootstrap4Table,
    # BootstrapTable,
    # BootstrapTablePinnedRows,
    # CheckboxTable,
    # CountryTable,
    # PersonTable,
    # SemanticTable,
    # ThemedCountryTable,
)


# def set_checkbox_choices(request, context):
#     new_context = copy.deepcopy(context)

#     # print(f'=> {request.POST=}')
#     # 'product_type': ['D'], 'product_use': ['M'], 'alternative': ['true'],
#     if request.POST['product_type'] == 'D':
#         new_context['daily_goods'] = 'checked'
#     elif request.POST['product_type'] == 'L':
#         new_context['luxury_goods'] = 'checked'
#     else:
#         pass

#     if request.POST['product_use'] == 'M':
#         new_context['personal'] = 'checked'
#     elif request.POST['product_use'] == 'F':
#         new_context['family'] = 'checked'
#     elif request.POST['product_use'] == 'G':
#         new_context['gift'] = 'checked'
#     else:
#         pass

#     if request.POST['alternative'] == 'true':
#         new_context['alt_available'] = 'checked'
#     elif request.POST['alternative'] == 'false':
#         new_context['alt_unavailable'] = 'checked'
#     else:
#         pass

#     return new_context


@login_required(redirect_field_name='accounts/login')
def place_order(request):

    if request.method == 'POST':

        for item in request.POST:
            key = item
            value = request.POST[key]
            print(f'{key=} {value}')

        print(f'=> place_order() POST! 0 {request.POST.get("submitprimary")=} {request.POST.get("submitsecondary")=}')

        # filter = ProductOrderFilter(request.GET, queryset=ProductOrder.objects.filter(product_type='D'))
        # print(f'=> place_order() POST! 00 {filter=}')

        form = ProductOrderForm(request.POST)

        print(f'=> place_order() POST! 1-1 {form=}')
        print(f'=> place_order() POST! 1-2 {form.is_valid()=}')
        print(f'=> place_order() POST! 1-3 {form.cleaned_data=}')
        print(f'=> place_order() POST! 2 {form.fields["expected_purchase_date"]=} {type(form.fields["expected_purchase_date"])=}')
        print(f'=> place_order() POST! 3 {request.POST["expected_purchase_date"]=} {type(request.POST["expected_purchase_date"])=}')

        if form.is_valid() is False:

            messages.error(request, '入力が正常完了しませんでした。')
            return redirect('index')
            # order_product = ProductOrder(
            #     goods=form.cleaned_data['goods'],
            #     product_price=form.cleaned_data['product_price'],
            #     type_of_estimation=form.cleaned_data['type_of_estimation'],
            #     product_type=form.cleaned_data['product_type'],
            #     product_use=form.cleaned_data['product_use'],
            #     alternative=form.cleaned_data['alternative'],
            #     expected_purchase_date=form.cleaned_data['expected_purchase_date'],
            # )
            # order_product.save()

        context = {'form': form, "expected_purchase_date": request.POST['expected_purchase_date']}

        # context = set_checkbox_choices(request, context)

        initial_dict = {
            'goods': form.cleaned_data['goods'],
            'product_price': form.cleaned_data['product_price'],
            'type_of_estimation': form.cleaned_data['type_of_estimation'],
            'product_type': form.cleaned_data['product_type'],
            'product_use': form.cleaned_data['product_use'],
            'alternative': form.cleaned_data['alternative'],
            'expected_purchase_date': form.cleaned_data['expected_purchase_date'],
            'orderid': form.cleaned_data['orderid'],
        }

        print(f'=> place_order()10 {initial_dict=}')

        form2 = ConfirmOrderForm(request.POST or None, initial=initial_dict)

        context = {'form': form2}  # , "expected_purchase_date": request.POST['expected_purchase_date']}

        print(f'=> place_order()11 before render() {context=}')
        return render(request, 'tabletest/confirm_details.html', context)

    # return redirect('confirm_details')
    # return render(request, 'confirm_details')
    messages.error(request, '入力が正常完了しませんでした。')
    return redirect('/')


def confirm_details(request):
    print(f'=> confirm_details1 {request.POST=}')
    # form = ConfirmOrderForm(request.POST, initial={'goods': 'Hi there!'})
    print(f'=> confirm_details2!')
    if request.method == 'POST':

        print(f'=> confirm_details()3 POST! {request.user=}')

        for item in request.POST:
            key = item
            value = request.POST[key]
            print(f'{key=} {value}')

        form = ConfirmOrderForm(request.POST)

        # print(f'=> confirm_details boundfield {form["goods"].initial=}')
        # print(f"=> confirm_details boundfield {form.get_initial_for_field(form.fields['goods'], 'goods')=}")

        print(f'=> confirm_details()4 {form=}')
        print(f'=> confirm_details()5 {form.fields["expected_purchase_date"]=} {type(form.fields["expected_purchase_date"])=}')

        if form.is_valid():
            print(f'=> confirm_details()6 {form.cleaned_data["orderid"]=}')

            if form.cleaned_data["orderid"] is None:
                order_product = ProductOrder(
                    goods=form.cleaned_data['goods'],
                    product_price=form.cleaned_data['product_price'],
                    type_of_estimation=form.cleaned_data['type_of_estimation'],
                    product_type=form.cleaned_data['product_type'],
                    product_use=form.cleaned_data['product_use'],
                    alternative=form.cleaned_data['alternative'],
                    expected_purchase_date=form.cleaned_data['expected_purchase_date'],
                    user=request.user,
                )
            else:
                productorder = ProductOrder.objects.get(pk=form.cleaned_data['orderid'])
                print(f'=> confirm_details()7 {productorder.created_on=}')
                order_product = ProductOrder(
                    id=form.cleaned_data["orderid"],
                    goods=form.cleaned_data['goods'],
                    product_price=form.cleaned_data['product_price'],
                    type_of_estimation=form.cleaned_data['type_of_estimation'],
                    product_type=form.cleaned_data['product_type'],
                    product_use=form.cleaned_data['product_use'],
                    alternative=form.cleaned_data['alternative'],
                    expected_purchase_date=form.cleaned_data['expected_purchase_date'],
                    user=request.user,
                    created_on=productorder.created_on
                )

            order_product.save()
            print(f'order_product.saved')
        else:
            print(f'=> confirm_details form is invalid {form.cleaned_data=}')
    else:
        return HttpResponse('something wrong at confirm_details()')

    return redirect('/')


@login_required(redirect_field_name='accounts/login')
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


def bootstrap4(request):
    """Demonstrate the use of the bootstrap4 template"""

    # create_fake_data()
    # table = Bootstrap4Table(ProductOrder.objects.all(), order_by="-goods")
    table_saved = Bootstrap4Table(ProductOrder.objects.filter(product_type='L'), order_by="-goods", prefix="1-")
    RequestConfig(request, paginate={"per_page": 2}).configure(table_saved)

    table_proc = Bootstrap4Table(ProductOrder.objects.filter(product_type='D'), order_by="-goods", prefix="2-")
    RequestConfig(request, paginate={"per_page": 2}).configure(table_proc)

    return render(request, "tabletest/bootstrap4_template.html", {"table": table_saved, "table_proc": table_proc})


def set_checkbox_choices(context, product_type, product_use, alternative):
    new_context = copy.deepcopy(context)

    # print(f'=> {request.POST=}')
    # 'product_type': ['D'], 'product_use': ['M'], 'alternative': ['true'],
    if product_type == 'D':
        new_context['daily_goods'] = 'checked'
    elif product_type == 'L':
        new_context['luxury_goods'] = 'checked'
    else:
        pass

    if product_use == 'M':
        new_context['personal'] = 'checked'
    elif product_use == 'F':
        new_context['family'] = 'checked'
    elif product_use == 'G':
        new_context['gift'] = 'checked'
    else:
        pass

    if alternative:
        new_context['alt_available'] = 'checked'
    elif alternative == False:
        new_context['alt_unavailable'] = 'checked'
    else:
        pass

    return new_context


def productorder_detail(request, pk):
    # productorder = get_object_or_404(ProductOrder, pk=pk)
    try:
        productorder = get_object_or_404(ProductOrder, pk=pk)
        # obj = MyModel.objects.get(pk=1)
    except ProductOrder.DoesNotExist:
        raise Http404("No MyModel matches the given query. productorder_detail()")

    print(f'=> productorder_detail {request=}')
    print(f'=> productorder_detail {productorder.id=}')
    print(f'=> productorder_detail {productorder.goods=}')
    print(f'=> productorder_detail {productorder.product_price=}')
    print(f'=> productorder_detail {productorder.type_of_estimation=}')
    print(f'=> productorder_detail {productorder.product_type=}')
    print(f'=> productorder_detail {productorder.product_use=}')
    print(f'=> productorder_detail {productorder.alternative=}')
    print(f'=> productorder_detail {productorder.expected_purchase_date=}')
    print(f'=> productorder_detail {productorder.expected_purchase_date.strftime("%Y-%m-%d")=}')

    initial_dict = {
        # 'goods':form.cleaned_data['goods'],
        # 'product_price':form.cleaned_data['product_price'],
        # 'type_of_estimation':form.cleaned_data['type_of_estimation'],
        # 'product_type':form.cleaned_data['product_type'],
        # 'product_use':form.cleaned_data['product_use'],
        # 'alternative':form.cleaned_data['alternative'],
        # 'expected_purchase_date':productorder.expected_purchase_date.strftime("%Y-%m-%d")
        'expected_purchase_date': "placeholder='2022-02-22'",
    }

    form = ProductOrderForm(instance=productorder)
    print(f'=> {form=}')
    # context = {'form': form, "expected_purchase_date": "2022-02-22"}
    context = {
        'form': form,
        "expected_purchase_date": productorder.expected_purchase_date.strftime("%Y-%m-%d"),
        'orderid': productorder.id
    }

    context = set_checkbox_choices(context, productorder.product_type, productorder.product_use, productorder.alternative)
    return render(request, "tabletest/index.html", context)

    # messages.error(request, '入力が正常完了しませんでした。')
    # return redirect('/')
