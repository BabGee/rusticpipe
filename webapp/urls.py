# webapp URL Configuration

from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

# From apps
from user import views as user_views
from pizzaweb.views import (
    product_detail,
    categorydetail,
    SearchResultsView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_product_from_cart,
)

urlpatterns = [
    path('', include('pizzaweb.urls')),

    # User Account urls
    path('register/', user_views.register, name='pizza-register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='pizza-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='pizza-logout'),

    #Pizzaweb urls
    path('product/<slug:slug>', product_detail, name='product-detail'),
    path('categorys/<int:pk>/', categorydetail, name='category-detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-product-from-cart/<slug:slug>/', remove_single_product_from_cart, name='remove-single-product-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),

    #Admin url
    path('admin/', admin.site.urls),

    #API_URLS
    path('api/pizzaweb/', include('pizzaweb.api.urls', 'api-pizzaweb')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
