from rest_framework import serializers
import bleach
from .models import MenuItem, Category, Order, OrderItem, Cart
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
from datetime import date


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']
        
        
class MenuItemSerializers(serializers.ModelSerializer):
    def validate(self, attrs):
        if(attrs['price']<0.01):
            # Using bleach for sanitization
            attrs['title'] = bleach.clean(attrs['title'])
            raise serializers.ValidationError('Price should not be less than 0.01')
        return super().validate(attrs)
    class Meta:
        model = MenuItem
        fields = ['id','title', 'price', 'featured', 'category']
        
        
class CartSerializers(serializers.ModelSerializer):
    menuItem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
     
    class Meta:
        model = Cart
        fields = ('id', 'user', 'menuItem', 'quantity', 'unit_price', 'price')

    def validate(self, data):
        quantity = data.get('quantity')
        menuItem = data.get('menuItem')
        if quantity and menuItem:
            data['price'] = quantity * menuItem.price
            data['unit_price'] = menuItem.price
        return data

    
class OrderSerializers(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        
        
class OderItemSerializers(serializers.HyperlinkedModelSerializer):
    quantity = serializers.SerializerMethodField(method_name='menuItem_count')
    
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default = serializers.CurrentUserDefault,
    )
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price']
        
    def menuItem_count(self, product:MenuItem):
        return product.count()