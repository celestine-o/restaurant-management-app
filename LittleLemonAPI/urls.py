from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view({'get': 'list'})),
    path('menu-items/{menuItem}', views.SingleMenuItemView.as_view({'get': 'retrieve'})),
    path('cart/menu-items', views.CartView.as_view({'get': 'list'})),
    path('orders', views.OrderView.as_view({'get': 'list'})),
    path('orders/{orderId}', views.SingleOrderView.as_view({'get': 'retrieve'})),
]