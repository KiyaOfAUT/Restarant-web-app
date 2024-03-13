from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from datetime import datetime
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import MenuItemsSerializer, OrderSerializer, CategorySerializer, CartSerializer, OrderItemSerializer, UserSerializer
from .models import MenuItem, Order, Category, Cart, OrderItem
from .permissions import MenuItemsAccess, MenuItemAccess, CategoryAccess, CustomerOnly, OrderAccess, AdminOnly, ManagerOnly
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
from django.contrib.auth.models import Group, User
# Create your views here.


class MenuItemsView(ListCreateAPIView):
    serializer_class = MenuItemsSerializer
    queryset = MenuItem.objects.all()
    permission_classes = [MenuItemsAccess]
    ordering_fields = ['price']
    search_fields = ['category__title', 'category__id']
    paginate_by = 2

class MenuItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemsSerializer
    queryset = MenuItem.objects.all()
    permission_classes = [MenuItemAccess]


class CategoryView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [CategoryAccess]


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders_view(request):
    if request.method == 'GET':
        if request.user.groups.filter(name='Admin').exists():
            queries = Order.objects.all()
            serialized = OrderSerializer(queries, many=True)
            return Response(serialized.data, HTTP_200_OK)
        elif request.user.groups.filter(name='Manager').exists():
            queries = Order.objects.all()
            serialized = OrderSerializer(queries, many=True)
            return Response(serialized.data, HTTP_200_OK)
        elif request.user.groups.filter(name='Delivery').exists():
            queries = Order.objects.all()
            delivery_id = request.user.pk
            queries = queries.filter(delivery_crew=delivery_id)
            serialized = OrderSerializer(queries, many=True)
            return Response(serialized.data, HTTP_200_OK)
        else:
            queries = Order.objects.all()
            CustId = request.user.pk
            queries = queries.filter(user_id=CustId)
            serialized = OrderSerializer(queries, many=True)
            return Response(serialized.data, HTTP_200_OK)
    else:
        if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery').exists():
            return Response({'message': "403 forbidden"}, HTTP_403_FORBIDDEN)
        else:
            queries = Cart.objects.filter(user_id=request.user.pk)
            if queries:
                total = 0
                for i in queries:
                    total = total + i.price
                date = datetime.now()
                order = {"user": request.user.pk, "total": total, "date": date.date()}
                serializer = OrderSerializer(data=order)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                cust_orders = Order.objects.filter(user_id=request.user.pk)
                record = cust_orders.order_by("id").last()
                new_id = record.id
                for i in queries:
                    order_item = {'order': record.id, 'menuitem': i.menuitem_id, 'quantity': i.quantity, 'unit_price': i.unit_price}
                    order_item_serializer = OrderItemSerializer(data=order_item)
                    order_item_serializer.is_valid(raise_exception=True)
                    order_item_serializer.save()
                Cart.objects.filter(user_id=request.user.pk).delete()
                return Response(serializer.data, HTTP_201_CREATED)
            else:
                return Response({'message': "404 Not Found!: no Cart exists"}, HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'Delete'])
@permission_classes([CustomerOnly])
def cart_view(request):
    if request.method == 'GET':
        queries = Cart.objects.filter(user_id=request.user.pk)
        serialized = CartSerializer(queries, many=True)
        return Response(serialized.data, HTTP_200_OK)
    elif request.method == 'POST':
        cart = request.data.copy()
        user = {'user': request.user.pk}
        cart.update(user)
        serialized = CartSerializer(data=cart)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, HTTP_201_CREATED)
    elif request.method == 'DELETE':
        Cart.objects.filter(user_id=request.user.pk).delete()
        return Response({'message': 'deleted!'}, HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH', 'POST', 'Delete'])
@permission_classes([OrderAccess])
def order_item_view(request, pk):
    try:
        record = Order.objects.get(id=pk)
        if request.method == 'GET':
            if request.user.groups.filter(name='Manager').exists():
                serialized = OrderSerializer(record)
                return Response(serialized.data, HTTP_200_OK)
            elif request.user.groups.filter(name='Delivery').exists():
                if record.delivery_crew_id == request.user.pk:
                    serialized = OrderSerializer(record)
                    return Response(serialized.data, HTTP_200_OK)
                else:
                    raise PermissionDenied
            else:
                if record.user_id == request.user.pk:
                    queries = OrderItem.objects.filter(order_id=pk)
                    serialized = OrderItemSerializer(queries, many=True)
                    return Response(serialized.data, HTTP_200_OK)
                else:
                    raise PermissionDenied
        elif request.method == 'PUT':
            serialized = OrderSerializer(data=request.data)
            serialized.is_valid(raise_exception=True)
            serialized.save()
            return Response(serialized.data, HTTP_200_OK)
        elif request.method == 'PATCH':
            if request.user.groups.filter(name='Delivery').exists():
                if record.delivery_crew_id == request.user.pk:
                    user = request.data.get('status', None)
                    if user is None:
                        raise ValueError
                    hold = request.data.get('id', None)
                    if hold is not None:
                        raise PermissionError
                    hold = request.data.get('user', None)
                    if hold is not None:
                        raise PermissionError
                    hold = request.data.get('delivery_crew', None)
                    if hold is not None:
                        raise PermissionError
                    hold = request.data.get('total', None)
                    if hold is not None:
                        raise PermissionError
                    hold = request.data.get('date', None)
                    if hold is not None:
                        raise PermissionError
                    partially_updated = OrderSerializer(record, data={'status': user}, partial=True)
                    partially_updated.is_valid(raise_exception=True)
                    partially_updated.save()
                    return Response(partially_updated.data, HTTP_200_OK)
                else:
                    raise PermissionDenied
            else:
                delivery = request.data.get('delivery_crew', None)
                if delivery is not None:
                    try:
                        crew = User.objects.get(id=delivery)
                    except ObjectDoesNotExist:
                        return Response({'message': 'user does not exist!'}, HTTP_404_NOT_FOUND)
                    if crew.groups.filter(name='Delivery').exists():
                        partially_updated = OrderSerializer(record, data=request.data, partial=True)
                        partially_updated.is_valid(raise_exception=True)
                        partially_updated.save()
                        return Response(partially_updated.data, HTTP_200_OK)
                    else:
                        return Response({'message': 'Your chosen user is not a Delivery crew'}, HTTP_400_BAD_REQUEST)
        else:
            Order.objects.get(id=pk).delete()
            OrderItem.objects.filter(order_id=pk).delete()
            return Response({'message': 'deleted!'}, HTTP_200_OK)
    except ValueError:
        return Response({'message': 'Field <status> does not exist'}, HTTP_400_BAD_REQUEST)
    except PermissionError:
        return Response({'message': '403 - forbidden! you are only allowed to change <status> field'}, HTTP_403_FORBIDDEN)
    except ObjectDoesNotExist:
        return Response({'message': 'order does not exist!'}, HTTP_404_NOT_FOUND)
    except PermissionDenied:
        return Response({'message': '403 forbidden!'}, HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST'])
@permission_classes([AdminOnly])
def manager_view(request):
    try:
        group = Group.objects.get(name='Manager')
        if request.method == 'GET':
            queries = User.objects.filter(groups__name='Manager')
            serialized = UserSerializer(queries, many=True)
            return Response(serialized.data, HTTP_200_OK)
        else:
            user_pk = request.data.get('user_id', None)
            if user_pk is None:
                raise ValueError
            else:
                user = User.objects.get(pk=user_pk)
                if user.groups.filter(name='Manager').exists():
                    return Response({'message': 'user is already a Manager!'}, HTTP_400_BAD_REQUEST)
                user.groups.add(group)
                return Response({"message": "added successfully!"}, HTTP_200_OK)
    except ValueError:
        return Response({'message': 'expected <user_id> field!'}, HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({'message': 'user does not exist!'}, HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([AdminOnly])
def manager_delete_view(request, pk):
    try:
        group = Group.objects.get(name='Manager')
        user = User.objects.get(pk=pk)
        if user.groups.filter(name='Manager').exists():
            user.groups.add(group)
            return Response({"message": "added successfully!"}, HTTP_200_OK)
        else:
            raise ValueError
    except ValueError:
        return Response({'message': 'expected <user_id> field!'}, HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({'message': 'user does not exist!'}, HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([ManagerOnly])
def delivery_view(request):
    try:
        group = Group.objects.get(name='Delivery')
        if request.method == 'GET':
            queries = User.objects.filter(groups__name='Delivery')
            serialized = UserSerializer(queries, many=True)
            return Response(serialized.data, HTTP_200_OK)
        else:
            user_pk = request.data.get('user_id', None)
            if user_pk is None:
                raise ValueError
            else:
                user = User.objects.get(pk=user_pk)
                if user.groups.filter(name='Delivery').exists():
                    return Response({'message': 'user is already a Delivery crew!'}, HTTP_400_BAD_REQUEST)
                user.groups.add(group)
                return Response({"message": "added successfully!"}, HTTP_200_OK)
    except ValueError:
        return Response({'message': 'expected <user_id> field!'}, HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([ManagerOnly])
def delivery_delete_view(request, pk):
    try:
        group = Group.objects.get(name='Delivery')
        user = User.objects.get(pk=pk)
        if user.groups.filter(name='Delivery').exists():
            user.groups.remove(group)
            return Response({"message": "Removed successfully!"}, HTTP_200_OK)
        else:
            raise ValueError
    except ValueError:
        return Response({'message': 'User is not a delivery crew!!'}, HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({'message': 'User does not exist'})
