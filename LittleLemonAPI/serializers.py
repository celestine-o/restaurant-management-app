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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Cart
        fields = ('id', 'user', 'menuItem', 'quantity')
        
    def validate(self, data):
        quantity = data.get('quantity')
        menuItem = data.get('menuItem')
        user = data.get('user', None)
        
        def validate(self, data):
            quantity = data.get('quantity')
            menuItem = data.get('menuItem')
            user = data.get('user', None)
            
            # Check if a cart with the same menuItem exists
            try:
                cart = Cart.objects.get(menuItem=menuItem, user=user)
                cart.quantity += quantity
                cart.price = cart.unit_price * cart.quantity
                cart.save()
                raise serializers.ValidationError(f"Added {quantity} {menuItem.title} to cart")
            except Cart.DoesNotExist:
                pass
            return data

class CartGetSerializer(serializers.ModelSerializer):
    menuItem_name = serializers.CharField(source='menuItem.title', read_only=True)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Cart
        fields = ('id', 'user', 'menuItem', 'menuItem_name', 'quantity', 'unit_price', 'price')
    
class CartSerializers(serializers.ModelSerializer):
    # menuItem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    # To display menuItem's title use the MenuItemSerializer
    menuItem = MenuItemSerializers()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
     
    class Meta:
        model = Cart
        fields = ('id', 'user', 'menuItem', 'quantity', 'unit_price', 'price')

    def validate(self, data):
        quantity = data.get('quantity')
        menuItem = data.get('menuItem')
        user = data.get('user', None)

        # Check if a cart with the same menuItem exists
        #try:
        #    cart = Cart.objects.get(menuItem=menuItem, user=user)
        #    cart.quantity += quantity
        #    cart.price = cart.unit_price * cart.quantity
        #    cart.save()
        #   #raise serializers.ValidationError(f"Added {quantity} {menuItem.title} to cart")
        #except Cart.DoesNotExist:
        #    pass

        # Create new cart
        if quantity and menuItem:
            data['price'] = quantity * menuItem.price
            data['unit_price'] = menuItem.price
        if menuItem in data:
            quantity =+ quantity
        print(data)
        return data

    
class OrderSerializers(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        
        
class OderItemSerializers(serializers.HyperlinkedModelSerializer):
    quantity = serializers.SerializerMethodField(method_name='menuItem_count')  
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price']
        
    def menuItem_count(self, product:MenuItem):
        return product.count()