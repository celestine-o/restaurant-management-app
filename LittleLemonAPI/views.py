from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import MenuItem, Cart, Order
from .serializers import MenuItemSerializers, CartSerializers, OrderSerializers, CartPostSerializer, CartGetSerializer

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
    # serializer_class = CartSerializers
    
    #def get_queryset(self):
    #    user = self.request.user
    #    return Cart.objects.filter(user=user)
    
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
    serializer_class = OrderSerializers
    ordering_fields = ['status', 'date', 'menuItem']
    

class SingleOrderView(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    
    def get_permissions(self):
        return [] if (self.request.method==['POST', 'PUT', 'PATCH', 'DELETE']) else [IsAuthenticated]