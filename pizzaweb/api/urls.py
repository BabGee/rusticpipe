from django.urls import path

from .views import api_product_detail, api_update_product

app_name = 'pizzaweb'

urlpatterns = [
    path('<slug>/', api_product_detail, name='api-product-detail'),
    path('update/<slug>/', api_update_product, name='api-update'),
]