from re import I
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse,Http404

# Create your views here.
from .forms import ProductOrderForm, ConfirmOrderForm
from .models import ProductOrder
from django.contrib import messages
import copy

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

    return new_context

@login_required(redirect_field_name='accounts/login')
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

        context = set_checkbox_choices(request, context)




        initial_dict = {
            'goods':form.cleaned_data['goods'],
            'product_price':form.cleaned_data['product_price'],
            'type_of_estimation':form.cleaned_data['type_of_estimation'],
            'product_type':form.cleaned_data['product_type'],
            'product_use':form.cleaned_data['product_use'],
            'alternative':form.cleaned_data['alternative'],
            'expected_purchase_date':form.cleaned_data['expected_purchase_date'],
        }

        print(f'=> place_order {initial_dict=}')

        form2 = ConfirmOrderForm(request.POST or None, initial=initial_dict)

        context = {'form': form2 } #, "expected_purchase_date": request.POST['expected_purchase_date']}

        print(f'=> before render() {context=}')
        return render(request, 'tabletest/confirm_details.html', context)

    # return redirect('confirm_details')
    # return render(request, 'confirm_details')
    messages.error(request, '入力が正常完了しませんでした。')
    return redirect('adin/')


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

        print(f'=> confirm_details boundfield {form["goods"].initial=}')
        print(f"=> confirm_details boundfield {form.get_initial_for_field(form.fields['goods'], 'goods')=}")

        if form.is_valid():
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
    table = Bootstrap4Table(ProductOrder.objects.all(), order_by="-goods")
    RequestConfig(request, paginate={"per_page": 5}).configure(table)

    return render(request, "tabletest/bootstrap4_template.html", {"table": table})


def productorder_detail(request, pk):
    # productorder = get_object_or_404(ProductOrder, pk=pk)
    try:
        productorder = get_object_or_404(ProductOrder, pk=pk)
        # obj = MyModel.objects.get(pk=1)
    except ProductOrder.DoesNotExist:
        raise Http404("No MyModel matches the given query. productorder_detail()")

    form = ProductOrderForm(instance=productorder)

    return render(request, "tabletest/index.html", {"form": form})

    # form = ConfirmOrderForm(instance=productorder)

    # return render(request, "tabletest/confirm_details.html", {"form": form})

