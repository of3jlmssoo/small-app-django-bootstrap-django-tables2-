from django.urls import path, re_path

# from . import views
from . import views
from .views import FileFieldFormView, FileShowDeleteFormView

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('index', views.index, name='index'),
    path('', views.bootstrap4, name='bootstrap4'),
    path('confirm_details/', views.confirm_details, name='confirm_details'),
    path("bootstrap4/", views.bootstrap4, name="bootstrap4"),
    path("productorder_detail/<int:pk>/", views.productorder_detail, name="productorder_detail"),
    # path('file_upload/', FileFieldFormView.as_view(), name='file_upload'),
    path('modal_file_upload/', FileFieldFormView.as_view(), name='modal_file_upload'),
    path('fup_success/', views.fup_success, name='fup_success'),
    # re_path(r'modal_file_showdelete/', FileShowDeleteFormView.as_view(), name='modal_file_showdelete'),
    # re_path(r'^modal_file_showdelete/(?P<orderid>[0-9]+)/$', FileShowDeleteFormView.as_view(), name='modal_file_showdelete'),
    path(
        'modal_file_showdelete/<int:orderid>/',
        FileShowDeleteFormView.as_view(),
        name='modal_file_showdelete'),
    # , kwargs={'orderid': 0}),
]
