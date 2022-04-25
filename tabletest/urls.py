from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

# from . import views
from . import views
from .views import FileFieldFormView, FileShowDeleteFormView,FileShowOnlyFormView

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('index', views.index, name='index'),
    path('', views.bootstrap4, name='bootstrap4'),
    path('confirm_details/', views.confirm_details, name='confirm_details'),
    path('recconfirm/<int:pk>/', views.reconfirm, name='reconfirm'),
    path("bootstrap4/", views.bootstrap4, name="bootstrap4"),
    path("productorder_detail/<int:pk>/", views.productorder_detail, name="productorder_detail"),
    # path('file_upload/', FileFieldFormView.as_view(), name='file_upload'),
    path('modal_file_upload/<int:orderid>/', FileFieldFormView.as_view(), name='modal_file_upload'),
    path('fup_success/', views.fup_success, name='fup_success'),
    # re_path(r'modal_file_showdelete/', FileShowDeleteFormView.as_view(), name='modal_file_showdelete'),
    # re_path(r'^modal_file_showdelete/(?P<orderid>[0-9]+)/$', FileShowDeleteFormView.as_view(), name='modal_file_showdelete'),
    path('modal_file_showdelete/<int:orderid>/', FileShowDeleteFormView.as_view(), name='modal_file_showdelete'),  # , kwargs={'orderid': 0}),
    path('modal_file_showonly/<int:orderid>/', FileShowOnlyFormView.as_view(), name='modal_file_showonly'),  # , kwargs={'orderid': 0}),
    path('delete/<int:pk>/', views.DocumentDeleteView.as_view(), name='delete_book'),
# ] 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
