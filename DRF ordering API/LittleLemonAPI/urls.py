from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.MenuItemView.as_view()),
    path('orders', views.orders_view),
    path('orders/<int:pk>', views.order_item_view),
    path('cart/menu-items', views.cart_view),
    path('categories', views.CategoryView.as_view()),
    path('groups/delivery-crew/users', views.delivery_view),
    path('groups/delivery-crew/users/<int:pk>', views.delivery_delete_view),
    path('groups/manager/users', views.manager_view),
    path('groups/manager/users/<int:pk>', views.manager_delete_view),
]
