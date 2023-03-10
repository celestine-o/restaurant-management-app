from rest_framework import serializers
import bleach
import contextlib
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
        
    
class CartPostSerializer(serializers.ModelSerializer):
    menuItem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Cart
        fields = ('id', 'user', 'menuItem', 'unit_price', 'price', 'quantity')
        
    def create(self, validated_data):
        menuItem = validated_data.get('menuItem')
        quantity = validated_data.get('quantity')
        user = self.context['request'].user   

        try:
            cart_item = Cart.objects.get(user=user, menuItem=menuItem)
            cart_item.quantity += quantity
            cart_item.price = cart_item.unit_price * cart_item.quantity
            cart_item.save()
        except Cart.DoesNotExist:
           cart_item = Cart.objects.create(
               user=user,
               menuItem=menuItem,
               quantity=quantity,
               unit_price=menuItem.price,
               price=quantity * menuItem.price
           )
        return cart_item

class CartGetSerializer(serializers.ModelSerializer):
    menuItem = serializers.CharField(source='menuItem.title', read_only=True)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Cart
        fields = ('id', 'user', 'menuItem', 'quantity', 'unit_price', 'price')

    
class OrderSerializer(serializers.ModelSerializer):
    #date = serializers.DateTimeField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #total = serializers.SerializerMethodField(method_name='calculate_total')
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
    
        
        
class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'