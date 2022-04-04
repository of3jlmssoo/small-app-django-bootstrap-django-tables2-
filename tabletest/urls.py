
from django.urls import path

# from . import views
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('index', views.index, name='index'),
    path('', views.bootstrap4, name='bootstrap4'),
    path('confirm_details/', views.confirm_details, name='confirm_details'),
    path("bootstrap4/", views.bootstrap4, name="bootstrap4"),
    path("productorder_detail/<int:pk>/", views.productorder_detail, name="productorder_detail"),
]
