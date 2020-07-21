from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pizza-index'),
    path('about/', views.about, name='pizza-about'),
    path('full_menu/', views.Product_list.as_view(), name='pizza-menu'),
    path('contact', views.contact, name='contact'),
]