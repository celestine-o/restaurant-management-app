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
    #unit_price = serializers.ReadOnlyField(source='menuItem.price')
    price = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    
    def validate(self, data):
        menuItem = data.get('menuItem')
        unit_price = menuItem.price
        quantity = data.get('quantity')
        data['menuItem'] = menuItem
        data['price'] = unit_price * quantity
        return data

    class Meta:
        model = Cart
        fields = ('id', 'user', 'menuItem', 'quantity', 'unit_price', 'price')
        
    def get_price(self, obj):
        print(MenuItem.price)
        return round(obj.unit_price * obj.quantity, 2)    
    
class OrderSerializers(serializers.HyperlinkedModelSerializer):
    date = date
    
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default = serializers.CurrentUserDefault,
    )
    
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