# from re import I
import copy
import logging
import sys

import django_filters
from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import FormView
from django_filters.views import FilterView
from django_tables2 import (MultiTableMixin, RequestConfig, SingleTableMixin,
                            SingleTableView)
from django_tables2.export.views import ExportMixin
from django_tables2.paginators import LazyPaginator

# Create your views here.
from .forms import (ConfirmOrderForm, ModalUploadFileForm, ProductOrderForm,
                    UploadFileForm, ViewOnlyOrderForm)
from .models import Document, ProductOrder
from .tables import Bootstrap4Table


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

            messages.error(request, '入力が正常完了しませんでした。')
            return redirect('index')

        if request.POST.get('submitsecondary') is not None:
            # お買い物申請フォームで保存ボタンが押された場合

            l.msg(f'{form.cleaned_data["orderid"]=}')
            # 共通データ
            order_product = createProductOrder(form.cleaned_data, request.user)
            order_product.status = "S"
            order_product.comment = form.cleaned_data['comment']

            # 既存レコードの場合
            if form.cleaned_data["orderid"]:
                productorder = ProductOrder.objects.get(pk=form.cleaned_data['orderid'])
                order_product.created_on = productorder.created_on

            # 保存用save()
            order_product.save()
            l.msg(f'order_product.saved as save_as_draft ')
            return redirect('bootstrap4')

        # 申請時処理
        l.msg(f'{type(form.cleaned_data)=}')
        initial_dict = set_initialDict4ConfirmOrderForm(form.cleaned_data)

        form2 = ConfirmOrderForm(request.POST or None, initial=initial_dict)

        books = set_related_documents(request, request.user, form.cleaned_data["orderid"])
        if not books:
            # books = set_unrelated_documents(request, request.user)
            books = set_related_documents(request, request.user)
            # for book in books:
            #     book.order = form.cleaned_data['orderid']
            #     book.save()

        context = {
            'form': form2,
            'comment': form.cleaned_data['comment'],
            'books': books,
        }
        l.msg(f'{context=}')
        return render(request, 'tabletest/confirm_details.html', context)

    messages.error(request, '入力が正常完了しませんでした。')
    return redirect('/')


def confirm_details(request):
    l = Logger('confirm_details')

    l.msg(f'{request.POST.get("CDApprove")=} {request.POST.get("CDReturn")=}')
    l.msg(f'{request.POST.keys()=}')

    if request.method == 'POST':

        display_POST_key_value(request)

        form = ConfirmOrderForm(request.POST)

        if form.is_valid():
            l.msg(f'{form.cleaned_data["orderid"]=} {form.cleaned_data["comment"]=}')

            # 承認者がアクションに応じてステータスをセット
            if request.user.is_approver:

                if 'CDApprove' in request.POST.keys():
                    status = 'A'
                elif 'CDReturn' in request.POST.keys():
                    status = 'S'

                # 承認者なのでレコードは存在する
                productorder = ProductOrder.objects.get(pk=form.cleaned_data['orderid'])
                user = productorder.user

            else:
                status = 'P'
                user = request.user
            order_product = createProductOrder(form.cleaned_data, user)
            # order_product = createProductOrder(form.cleaned_data, form.cleaned_data['user'])
            order_product.status = status

            # 既存レコードの場合、orderid等をセットする
            if form.cleaned_data["orderid"]:
                productorder = ProductOrder.objects.get(pk=form.cleaned_data['orderid'])
                # id=form.cleaned_data["orderid"],
                # created_on=productorder.created_on,
                # comment=form.cleaned_data['comment'],
                order_product.id = form.cleaned_data["orderid"]
                order_product.created_on = productorder.created_on
                order_product.comment = form.cleaned_data['comment']
                order_product.user = productorder.user

            if not len(set_related_documents(request, productorder.user, form.cleaned_data["orderid"])):
                books = set_related_documents(request, productorder.user)
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
    # return render(request, 'tabletest/index.html', {'form': form})

    # lsts = Document.objects.filter(order__isnull=True, user=request.user)
    lsts = set_related_documents(request, request.user)

    context = {
        'form': form,
        # 'books': docs,
        'books': lsts,
    }
    # 'comment': productorder.comment,
    # 'status': productorder.status, }
    return render(request, 'tabletest/index.html', context)


@ login_required(redirect_field_name='accounts/login')
def bootstrap4(request):
    """Demonstrate the use of the bootstrap4 template"""

    table_saved = Bootstrap4Table(ProductOrder.objects.filter(status="S"), order_by="-updated_on")
    RequestConfig(request, paginate={"per_page": 2}).configure(table_saved)

    # table_proc = Bootstrap4Table(ProductOrder.objects.filter(status='P'), order_by="-goods", prefix="2-")
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


def productorder_detail(request, pk):
    # ダッシュボードでIDをクリックした際にコールされる
    l = Logger('productorder_detail')
    # productorder = get_object_or_404(ProductOrder, pk=pk)
    try:
        productorder = get_object_or_404(ProductOrder, pk=pk)
        # obj = MyModel.objects.get(pk=1)
    except ProductOrder.DoesNotExist:
        raise Http404("No MyModel matches the given query. productorder_detail()")

    l.msg(f'{type(productorder)=}')

    lsts = set_related_documents(request, productorder.user, productorder.id)
    if len(lsts) == 0:
        lsts = set_related_documents(request, request.user)

    print(f'============= {productorder.id}')
    print(f'============= {lsts}')

    if request.user.is_approver:

        initial_dict = set_initialDict4ConfirmOrderForm(productorder)
        form2 = ConfirmOrderForm(request.POST or None, initial=initial_dict)

        context = {
            'form': form2,
            'comment': productorder.comment,
            'status': productorder.status,
            'books': lsts,
        }
        l.msg(f'{context=}')
        return render(request, 'tabletest/confirm_details.html', context)

    else:

        if productorder.status == 'A':
            # 承認済みの場合、全フィールドROで表示する。ConfirmOrderFormはコメント欄以外はRO。
            # コメント欄はテンプレートでif user.is_approver and status == 'P'の場合のみRW、それ以外の条件ではROとなる

            initial_dict = set_initialDict4ConfirmOrderForm(productorder)

            form2 = ConfirmOrderForm(request.POST or None, initial=initial_dict)

            context = {'form': form2, 'comment': productorder.comment, 'status': productorder.status, 'books': lsts}

            l.msg(f'not approver readonly {context=}')
            return render(request, 'tabletest/confirm_details.html', context)

        else:
            # non-approverがダッシュボードからIDをクリックした場合、編集画面に行く。そこで中身を編集するかしないで申請か保存を選ぶことになる。
            # 編集する可能性があるのでplace_orderにいく

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

            # set_checkbox_choicesでcontextに第二引数以降のエントリーを追加する
            context = set_checkbox_choices(
                context,
                productorder.product_type,
                productorder.product_use,
                productorder.alternative)
            l.msg(f'non-approver {context=}')
            return render(request, "tabletest/index.html", context)

            # messages.error(request, '入力が正常完了しませんでした。')
            # return redirect('/')


def file_upload_single(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Document(file_field=request.FILES['file'])
            print(f"=== 1 === {request.FILES['file']}")
            instance.title = form.cleaned_data['title']
            instance.user = request.user
            instance.save()
            return HttpResponseRedirect('/tabletest/fup_success/')
    else:
        form = UploadFileForm()
    return render(request, 'tabletest/file_upload.html', {'form': form})


# class FileFieldFormView(FormView):
class FileFieldFormView(BSModalCreateView):
    form_class = ModalUploadFileForm
    template_name = 'tabletest/modal_file_upload.html'  # Replace with your template.
    success_url = '/tabletest/fup_success/'  # Replace with your URL or reverse().

    # def post(self, request, *args, **kwargs):
    #     print(f'=== post =============================')
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     files = request.FILES.getlist('file_field')
    #     if form.is_valid():
    #         for f in files:
    #             instance = Document(file_field=f)
    #             instance.title = form.cleaned_data['title']
    #             instance.file_field.name = f.name
    #             instance.user = request.user
    #             instance.save()

    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    # def form_valid(self, form):
    def form_valid(self, form):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = self.request.FILES.getlist('file_field')
        # 同じファイルが2度ほぞんされてしまう問題へself.request.headers.get() ==で対応
        # djangoでis_ajax()がなくなったことに対応
        if form.is_valid() and self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            for f in files:
                instance = Document(file_field=f)
                instance.title = form.cleaned_data['title']
                instance.file_field.name = f.name
                instance.user = self.request.user
                instance.file_name = self.request.upload_handlers[0].file_name
                instance.save()
                print(f'{self.request.upload_handlers[0].file_name=}')
                # print(f'=== form_valid1 {f=}')

        return redirect('index')
        # return super().form_valid(form)
        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(form)


def fup_success(request):
    str_out = "Success!<p />"
    str_out += "成功<p />"
    return HttpResponse(str_out)
