from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/{menuItem}', views.SingleMenuItemView.as_view()),
    path('cart/menu-items', views.CartView.as_view()),
    path('orders', views.OrderSerializers.as_view()),
    path('orders/{orderId}', views.SingleOrderView.as_view()),
]