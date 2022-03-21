
from django.urls import path

# from . import views
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('', views.index, name='index'),
    # path('', views.indexcopy, name='indexcopy'),
    path('confirm_details/', views.confirm_details, name='confirm_details'),
]