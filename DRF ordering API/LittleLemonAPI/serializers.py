from rest_framework import serializers
from .models import MenuItem, Category, Order, Cart, OrderItem, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title']


class MenuItemsSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']


class OrderItemSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(source='menuitem')

    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'unit_price', 'title']


class CartSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(source='menuitem')

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price', 'title']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']
