from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view({
        'get': 'list',
        'post': 'create',
    })),
    
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view({
        'get': 'retrieve',
        'post': 'create',
        'put' : 'update',
        'patch' : 'partial_update',
        'delete' : 'destroy'
    })),
    
    path('cart/menu-items', views.CartView.as_view({
        'get': 'list',
        'post': 'create',
        'delete' : 'destroy'
    })),
    path('orders', views.OrderView.as_view({'get': 'list'})),
    path('orders/{orderId}', views.SingleOrderView.as_view({'get': 'retrieve'})),
]