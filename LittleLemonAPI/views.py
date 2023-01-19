from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import MenuItem, Cart, Order
from .serializers import MenuItemSerializers, CartSerializers, OrderSerializers

# Create your views here.
class MenuItemView(viewsets.ModelViewSet):
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
    
    def get_permissions(self):
        return [] if (self.request.method==['POST', 'PUT', 'PATCH', 'DELETE']) else [IsAuthenticated]
    
class CartItemsView(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle]
    queryset = Cart.objects.all()
    serializer_class = CartSerializers
    
class OrderView(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    ordering_fields = ['status', 'date', 'menuItem']
    
    def get_permissions(self):
        return [] if (self.request.method==['POST', 'PUT', 'PATCH', 'DELETE']) else [IsAuthenticated]

class SingleOrderView(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    
    def get_permissions(self):
        return [] if (self.request.method==['POST', 'PUT', 'PATCH', 'DELETE']) else [IsAuthenticated]