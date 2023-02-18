from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import MenuItem, Cart, Order
from .serializers import *

# Create your views here.
class MenuItemsView(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializers
    ordering_fields=['featured', 'category', 'price']
    search_fields=['title', 'category__title']
    
    def get_permissions(self):
        return [] if (self.request.method==['POST', 'PUT', 'PATCH', 'DELETE']) else [IsAuthenticated()]
    
class SingleMenuItemView(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializers
    
    #def get_permissions(self):
    #    return [] if (self.request.method==['POST', 'PUT', 'PATCH', 'DELETE']) else [IsAuthenticated]
    
class CartView(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle]
    queryset = Cart.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartGetSerializer
        else:
            return CartPostSerializer

    def perform_destroy(self, instance):
        instance.delete()
    
    
class OrderView(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle]
    queryset = Order.objects.all()
    ordering_fields = ['status', 'date', 'menuItem']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderGetSerializer
        else:
            return OrderPostSerializer
        
    # mehtod to delete orders
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    

class SingleOrderView(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle]
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer
    
    def get_permissions(self):
        return [] if (self.request.method==['POST', 'PUT', 'PATCH', 'DELETE']) else [IsAuthenticated]