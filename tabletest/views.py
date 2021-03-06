# from re import I
import copy
import logging

# import django_filters
# from bootstrap_modal_forms.generic import (BSModalCreateView, BSModalDeleteView, BSModalReadView)
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
# from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
# from django_filters.views import FilterView
# from django_tables2 import (MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView)
from django_tables2 import RequestConfig

# Create your views here.
# from .forms import (ConfirmOrderForm, ModalShowDeleteFileForm, ModalUploadFileForm, ProductOrderForm, UploadFileForm, ViewOnlyOrderForm)
from .forms import (ConfirmOrderForm, ModalShowDeleteFileForm,
                    ModalUploadFileForm, ProductOrderForm)
from .models import Document, ProductOrder
from .tables import Bootstrap4Table

# from django_tables2.export.views import ExportMixin
# from django_tables2.paginators import LazyPaginator


# import sys


class Logger():

    logger = logging.getLogger(__name__)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    logger.propagate = False
    # DEBUG INFO WARNIG ERROR CRTICAL
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    logger.disabled = False

    def __init__(self, funcname) -> None:

        self.funcname = funcname

    def msg(self, message):
        # self.logger.debug(self.funcname + ' : ' + message)
        formatter = logging.Formatter('-> %(asctime)s - %(name)s - %(message)s')
        Logger.ch.setFormatter(formatter)
        Logger.logger.debug(self.funcname + ' : ' + message)


def set_unrelated_documents(request, user):
    return Document.objects.filter(order__isnull=True, user=request.user)


def set_related_documents(request, user, id=None):
    if id is None:
        return Document.objects.filter(order__isnull=True, user=request.user)
    else:
        return Document.objects.filter(order=id, user=user)


def display_POST_key_value(request):
    l = Logger('display_POST_key_value')
    for item in request.POST:
        key = item
        value = request.POST[key]
        l.msg(f'{key=} {value=}')
    del l


def createProductOrder(cleaned_data, user):
    return ProductOrder(
        id=cleaned_data['orderid'],
        goods=cleaned_data['goods'],
        product_price=cleaned_data['product_price'],
        type_of_estimation=cleaned_data['type_of_estimation'],
        product_type=cleaned_data['product_type'],
        product_use=cleaned_data['product_use'],
        alternative=cleaned_data['alternative'],
        expected_purchase_date=cleaned_data['expected_purchase_date'],
        user=user,
    )


def set_initialDict4ConfirmOrderForm(productorder):
    l = Logger('set_initialDict4ConfirmOrderForm')
    l.msg(f'{type(productorder)=}')

    if isinstance(productorder, ProductOrder):

        l.msg(f'{productorder.id=} set to orderid')
        return {
            'orderid': productorder.id,
            'goods': productorder.goods,
            'product_price': productorder.product_price,
            'type_of_estimation': productorder.type_of_estimation,
            'product_type': productorder.product_type,
            'product_use': productorder.product_use,
            'alternative': productorder.alternative,
            'expected_purchase_date': productorder.expected_purchase_date.strftime("%Y-%m-%d"),
            'comment': productorder.comment,
        }

    elif isinstance(productorder, dict):
        return {
            'orderid': productorder['orderid'],
            'goods': productorder['goods'],
            'product_price': productorder['product_price'],
            'type_of_estimation': productorder['type_of_estimation'],
            'product_type': productorder['product_type'],
            'product_use': productorder['product_use'],
            'alternative': productorder['alternative'],
            'expected_purchase_date': productorder['expected_purchase_date'],
        }

    else:
        l = Logger(set_initialDict4ConfirmOrderForm)
        l.msg(f'unsupported data format {type(productorder)=} {productorder}')

        return None


@login_required(redirect_field_name='accounts/login')
def place_order(request):

    l = Logger('place_order')

    if request.user.is_approver:
        l.msg(f'your are a approver! {request.user.is_approver=}')
    else:
        l.msg(f'your are not a approver! {request.user.is_approver=}')

    if request.method == 'POST':

        display_POST_key_value(request)

        l.msg(f'{request.POST.get("submitprimary")=} {request.POST.get("submitsecondary")=}')

        form = ProductOrderForm(request.POST)

        if form.is_valid() is False:

            messages.error(request, '?????????????????????????????????????????????')
            return redirect('index')

        l.msg(f'{form.fields["goods"]=}')
        l.msg(f'{form.cleaned_data["orderid"]=}')

        # ???????????????
        order_product = createProductOrder(form.cleaned_data, request.user)
        order_product.status = "S"
        order_product.comment = form.cleaned_data['comment']

        # ???????????????????????????
        # if form.cleaned_data["orderid"]:
        #     productorder = ProductOrder.objects.get(pk=form.cleaned_data['orderid'])
        #     order_product.created_on = productorder.created_on

        # ???????????????(ID???????????????)?????????(???????????????)????????????????????????ID???????????????
        l.msg(f'---> {form.cleaned_data["orderid"]=}')
        if form.cleaned_data["orderid"] is None:
            # ???????????????
            order_product.save()
        else:
            # ?????????????????????????????????????????????????????????????????????????????????????????????
            # form = ProductOrderForm(request.POST)
            # if form.is_valid():
            # order_product = ProductOrder.objects.get(pk=orderid)
            order_product = ProductOrder.objects.get(pk=form.cleaned_data['orderid'])
            order_product.goods = form.cleaned_data['goods']
            order_product.product_price = form.cleaned_data['product_price']
            order_product.type_of_estimation = form.cleaned_data['type_of_estimation']
            order_product.product_type = form.cleaned_data['product_type']
            order_product.product_use = form.cleaned_data['product_use']
            order_product.alternative = form.cleaned_data['alternative']
            order_product.expected_purchase_date = form.cleaned_data['expected_purchase_date']
            order_product.user = request.user
            order_product.save()

        l.msg(f'order_product.saved as save_as_draft {order_product.id=}')
        if request.POST.get('submitsecondary') is not None:
            # ?????????????????????????????????????????????????????????????????????
            order_product.status = "S"
            order_product.save()
            l.msg(f'order_product.saved as save_as_draft ')
            return redirect('bootstrap4')

        # ???????????????
        # l.msg(f'{type(form.cleaned_data)=}')
        # initial_dict = set_initialDict4ConfirmOrderForm(form.cleaned_data)

        form2 = ConfirmOrderForm(instance=order_product)

        books = set_related_documents(request, request.user, form.cleaned_data["orderid"])
        if not books:
            books = set_related_documents(request, request.user)

        context = {
            'form': form2,
            'comment': form.cleaned_data['comment'],
            'books': books,
            'orderid': order_product.id,
        }
        l.msg(f'{context=}')
        return render(request, 'tabletest/confirm_details.html', context)

    messages.error(request, '?????????????????????????????????????????????')

    return redirect('/')


def confirm_details(request):
    l = Logger('confirm_details')

    l.msg(f'{request.POST.get("CDApprove")=} {request.POST.get("CDReturn")=} {request.POST.get("nonAPgoback")=} {request.method=}')
    l.msg(f'{request.POST.keys()=}')

    if request.method == 'POST':

        display_POST_key_value(request)

        form = ConfirmOrderForm(request.POST)
        if form.is_valid():
            l.msg(f'{form.cleaned_data["orderid"]=} {form.cleaned_data["comment"]=}')

            # ??????????????????????????????????????????????????????????????????
            if request.user.is_approver:

                l.msg(f'POST and approver')

                if 'approvertotables' in request.POST.keys():
                    l.msg(f'POST and approver aprrovertotables')
                    return redirect('bootstrap4')

                if 'CDApprove' in request.POST.keys():
                    status = 'A'
                elif 'CDReturn' in request.POST.keys():
                    status = 'S'

                # ?????????????????????????????????????????????
                productorder = ProductOrder.objects.get(pk=form.cleaned_data['orderid'])
                user = productorder.user

            else:  # ?????????

                l.msg(f'nonAPgoback0')
                if 'nonAPgoback' in request.POST.keys():
                    l.msg(f'nonAPgoback1')
                    return redirect('productorder_detail', form.cleaned_data['orderid'])

                status = 'P'
                user = request.user

            # ???????????????????????????????????????ProductOrder????????????????????????????????????????????????id?????????????????????save()
            order_product = createProductOrder(form.cleaned_data, user)
            order_product.status = status

            # ??????????????????????????????orderid?????????????????????
            if form.cleaned_data["orderid"]:
                productorder = ProductOrder.objects.get(pk=form.cleaned_data['orderid'])
                order_product.id = form.cleaned_data["orderid"]
                order_product.created_on = productorder.created_on
                order_product.comment = form.cleaned_data['comment']
                order_product.user = productorder.user

            if not len(set_related_documents(request, request.user, form.cleaned_data["orderid"])):
                books = set_related_documents(request, request.user)
                for book in books:
                    book.order = order_product
                    l.msg(f'book.order was set to {book.order}')
                    book.save()

            order_product.save()
            l.msg(f'order_product.saved')
        else:
            l.msg(f'form is invalid {form.cleaned_data=}')
    else:
        return HttpResponse('something wrong at confirm_details()')

    return redirect('/')


@ login_required(redirect_field_name='accounts/login')
def index(request):

    l = Logger('index')

    form = ProductOrderForm()

    lsts = set_related_documents(request, request.user)

    context = {
        'form': form,
        'books': lsts,
    }
    return render(request, 'tabletest/index.html', context)


@ login_required(redirect_field_name='accounts/login')
def bootstrap4(request):
    """Demonstrate the use of the bootstrap4 template"""

    table_saved = Bootstrap4Table(ProductOrder.objects.filter(status="S"), order_by="-updated_on")
    RequestConfig(request, paginate={"per_page": 2}).configure(table_saved)

    table_proc = Bootstrap4Table(ProductOrder.objects.filter(status='P'), order_by="-updated_on", prefix="2-")
    RequestConfig(request, paginate={"per_page": 2}).configure(table_proc)

    table_apro = Bootstrap4Table(ProductOrder.objects.filter(status='A'), order_by="-updated_on", prefix="3-")
    RequestConfig(request, paginate={"per_page": 2}).configure(table_apro)

    return render(request, "tabletest/bootstrap4_template.html",
                  {"table": table_saved, "table_proc": table_proc, "table_apro": table_apro})


def set_checkbox_choices(context, product_type, product_use, alternative):
    new_context = copy.deepcopy(context)

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


def reconfirm(request, pk):
    l = Logger('reconfirm')
    l.msg(f'called {pk=}')

    try:
        productorder = get_object_or_404(ProductOrder, pk=pk)
    except ProductOrder.DoesNotExist:
        raise Http404("No MyModel matches the given query. productorder_detail()")

    l.msg(f'{productorder=}')
    lsts = set_related_documents(request, productorder.user, productorder.id)
    if len(lsts) == 0:
        lsts = set_related_documents(request, request.user)

    l.msg(f'{lsts=}')
    if not request.user.is_approver:

        initial_dict = set_initialDict4ConfirmOrderForm(productorder)
        formx = ConfirmOrderForm(request.POST or None, initial=initial_dict)

        context = {
            'form': formx,
            'comment': productorder.comment,
            'status': productorder.status,
            'books': lsts,
            'orderid': pk,
        }
        l.msg(f'{context=}')
        return render(request, 'tabletest/confirm_details.html', context)

    l.msg(f'return 2 productorder_detail')
    return redirect('productorder_detail', pk)


def productorder_detail(request, pk):
    # ????????????????????????ID?????????????????????????????????????????????
    l = Logger('productorder_detail')
    try:
        productorder = get_object_or_404(ProductOrder, pk=pk)
    except ProductOrder.DoesNotExist:
        raise Http404("productorder_detail get_object_or_404 failed")

    l.msg(f'{type(productorder)=}')

    lsts = set_related_documents(request, productorder.user, productorder.id)
    if len(lsts) == 0:
        lsts = set_related_documents(request, request.user)

    if request.user.is_approver:

        initial_dict = set_initialDict4ConfirmOrderForm(productorder)
        form2 = ConfirmOrderForm(request.POST or None, initial=initial_dict)

        context = {
            'form': form2,
            'comment': productorder.comment,
            'status': productorder.status,
            'books': lsts,
            'orderid': productorder.id,
        }
        l.msg(f'{context=}')
        return render(request, 'tabletest/confirm_details.html', context)

    else:

        if productorder.status == 'A':
            # ??????????????????????????????????????????RO??????????????????ConfirmOrderForm???????????????????????????RO???
            # ???????????????????????????????????????if user.is_approver and status == 'P'???????????????RW??????????????????????????????RO?????????

            initial_dict = set_initialDict4ConfirmOrderForm(productorder)

            form2 = ConfirmOrderForm(request.POST or None, initial=initial_dict)

            context = {
                'form': form2,
                'comment': productorder.comment,
                'status': productorder.status,
                'books': lsts,
                'orderid': productorder.id,
            }

            l.msg(f'not approver readonly {context=}')
            return render(request, 'tabletest/confirm_details.html', context)

        else:
            # non-approver??????????????????????????????ID?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
            # ????????????????????????????????????place_order?????????

            l.msg(f'{productorder.id=}')
            l.msg(f'{set_related_documents(request, productorder.user, productorder.id)=}')
            lsts = set_related_documents(request, productorder.user, productorder.id)
            if len(lsts) == 0:
                lsts = set_related_documents(request, request.user)

            form = ProductOrderForm(instance=productorder)
            l.msg(f'{form=}')
            context = {
                'form': form,
                "expected_purchase_date": productorder.expected_purchase_date.strftime("%Y-%m-%d"),
                'orderid': productorder.id,
                'comment': productorder.comment,
                'books': lsts,
            }

            # set_checkbox_choices???context??????????????????????????????????????????????????????
            context = set_checkbox_choices(
                context,
                productorder.product_type,
                productorder.product_use,
                productorder.alternative)
            l.msg(f'non-approver {context=}')
            return render(request, "tabletest/index.html", context)


class RedirectToPreviousMixin:

    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


class FileFieldFormView(RedirectToPreviousMixin, BSModalCreateView):
    form_class = ModalUploadFileForm
    template_name = 'tabletest/modal_file_upload.html'  # Replace with your template.
    success_url = "/productorder_detail/{id}/"

    def form_valid(self, form):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = self.request.FILES.getlist('file_field')
        # ?????????????????????2???????????????????????????????????????self.request.headers.get() ==?????????
        # django???is_ajax()?????????????????????????????????
        if form.is_valid() and self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            for f in files:
                instance = Document(file_field=f)
                instance.title = form.cleaned_data['title']
                instance.file_field.name = f.name
                instance.user = self.request.user
                instance.file_name = self.request.upload_handlers[0].file_name
                instance.order = ProductOrder.objects.get(id=self.kwargs['orderid'])
                instance.save()

        formx = ConfirmOrderForm(initial={'goods': 'ABC', 'orderid': 160})

        return redirect('reconfirm', self.kwargs['orderid'])
        # return reverse_lazy('company', kwargs={'pk': companyid})

        # return redirect('productorder_detail', self.kwargs['orderid'])

        # return redirect(reverse('confirm_details', kwargs={'form': formx}))


def fup_success(request):
    str_out = "Success!<p />"
    str_out += "??????<p />"
    return HttpResponse(str_out)


class FileShowOnlyFormView(RedirectToPreviousMixin, ListView):
    form_class = ModalShowDeleteFileForm
    template_name = 'tabletest/modal_file_showonly.html'  # Replace with your template.
    # success_url = '/tabletest/fup_success/'  # Replace with your URL or reverse().

    def get_queryset(self):
        order = ProductOrder.objects.get(id=self.kwargs['orderid'])
        user = order.user
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if self.kwargs['orderid'] != 0:
                query_result = Document.objects.filter(order=self.kwargs['orderid'], user=user)
                if not query_result:
                    query_result = Document.objects.filter(order__isnull=True, user=user)
            else:
                query_result = Document.objects.filter(order__isnull=True, user=user)
            return query_result


class FileShowDeleteFormView(RedirectToPreviousMixin, ListView):
    form_class = ModalShowDeleteFileForm
    template_name = 'tabletest/modal_file_showdelete.html'  # Replace with your template.

    def get_queryset(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if self.kwargs['orderid'] != 0:
                query_result = Document.objects.filter(order=self.kwargs['orderid'], user=self.request.user)
                if not query_result:
                    query_result = Document.objects.filter(order__isnull=True, user=self.request.user)
            else:
                query_result = Document.objects.filter(order__isnull=True, user=self.request.user)
            return query_result


class DocumentDeleteView(RedirectToPreviousMixin, BSModalDeleteView):
    model = Document
    template_name = 'tabletest/delete_book.html'
    success_message = 'Success: Book was deleted.'
