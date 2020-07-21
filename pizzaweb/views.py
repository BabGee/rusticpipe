from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Product, Category, Order, OrderProduct
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views import generic
from django.views.generic import View
from django.contrib import messages
from django.db.models import Q 
import random
import string

all_products = Product.objects.all()
all_categories = Category.objects.all()

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def index(request):
    context = {
        'offer_products': all_products.filter(rating=1),
        'rusticpipe_products': all_products.filter(restaurant=0, rating=0), 
        'lemonlounge_products': all_products.filter(restaurant=1, rating=0),
        'categories' : all_categories,
        'categoriess' : all_categories[1:],
        'new_product': all_products.first()
    }
    return render(request, 'pizzaweb/index.html', context)

def about(request):
    context = {
        'categories' : all_categories,
    }
    return render(request, 'pizzaweb/about.html', context)

class Product_list(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'pizzaweb/all_products.html'
    paginate_by = 3    

def product_detail(request, slug):
    product = all_products.get(slug=slug)
    category = product.category
    context = {
        'product': product,
        'related_prod': all_products.filter(category__name=category),
        'categories' : all_categories,
    }
    return render(request, 'pizzaweb/product.html', context)

def categorydetail(request,pk):
    cat = Category.objects.get(pk = pk)
    
    context = {
        'products_with_category': Product.objects.filter(category__name = cat),
        'category' : cat,
        'other_cats' : all_categories,
        'categories' : all_categories,
    }
    
    return render(request, 'pizzaweb/category.html', context)

def contact(request):
    context = {
        'offer_products' : all_products[:4],
        'prod' : all_products.first(),
        'categories' : all_categories,
    }
    return render(request, 'pizzaweb/contact.html', context) 

class SearchResultsView(View):
    def get(self, *args, **kwargs):
        qs =  Product.objects.all()
        query = self.request.GET.get('qproduct')        
        if query: 
            qs = qs.filter(Q(title__icontains=query))
            product_count = qs.count()
            if len(qs) == 0:
                messages.warning(self.request, f'No Product Named {query}')
                return redirect('/')
        elif query == '':
             messages.warning(self.request, 'No Product selected')
             return redirect('/')

        context = {
            'search_query_rslt' : qs,
            'categories' : all_categories,
            'product_count': product_count,
        }
        return render(self.request, 'pizzaweb/search_results.html', context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
                'categories' : all_categories,
            }
            return render(self.request, 'pizzaweb/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order')
            return redirect('/')

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, f'{order_product} quantity was updated.')
            return redirect('order-summary')
        else:
            order.products.add(order_product)
            messages.info(request, f'{order_product} was added to your cart.')
            return redirect('order-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date, ref_code=create_ref_code())
        order.products.add(order_product)
        messages.info(request, f'{order_product} was added to your cart.')
        return redirect('order-summary')

@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            messages.info(request, f'{order_product} quantity was updated.')
            return redirect('order-summary')
        else:
            messages.info(request, f'{order_product} was not in your cart')
            return redirect('product', slug=slug)
    else:
        messages.info(request, 'You do not have an active order')
        return redirect('product', slug=slug)


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            messages.info(request, f'{order_product} was removed from your cart.')
            return redirect('order-summary')
        else:
            messages.info(request, f'{order_product} was not in your cart')
            return redirect('product-detail', slug=slug)
    else:
        messages.info(request, 'You do not have an active order')
        return redirect('product-detail', slug=slug)

