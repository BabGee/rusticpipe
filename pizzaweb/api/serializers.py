from rest_framework import serializers

from pizzaweb.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
                'image', 'title', 'description', 
                'category', 'price', 'discount_price'
                ]


