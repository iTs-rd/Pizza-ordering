from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import jwt
from config import Config
from .models import *
from .serializers import *

def get_id_from_token(token):
    jwtuser = jwt.decode(token,Config.JWT_SECRET_KEY, algorithms=['HS256'])
    return jwtuser["user_id"]

def check_for_super_user(token):
    jwtuser = jwt.decode(token,Config.JWT_SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(pk=jwtuser['user_id'])
    return user.is_superuser

def check_authorization(request, order_user_id):
    token = request.headers["Authorization"][7:]

    is_super = check_for_super_user(token)

    if is_super:
        return True

    user_id = get_id_from_token(token)
    return order_user_id == user_id


@api_view(['POST'])
def Signup(request):
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response = {
            'data' : serializer.data,
            "message" : "User created successfully",
            "success": True,
        }
        return Response(response,status=status.HTTP_201_CREATED)

    response = {
        'data' : serializer.errors,
        "message" : "User not created",
        "success": False,
    }
    return Response(response,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def PlaceOrder(request):
    if request.method == 'POST':
        request.data._mutable = True
        request.data['customer'] = get_id_from_token(request.headers["Authorization"][7:])
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'data' : {
                    'Order No.': serializer.data['id'],
                    'Order Quantity' : serializer.data['quantity'],
                    'Order Size' : serializer.data['size'],
                },
                "message" : "Thank You For Choosing Us",
                "success": True,
            }
            return Response(response,status=status.HTTP_201_CREATED)

        response = {
            'data' : serializer.errors,
            "message" : "Order not placed",
            "success": False,
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def OrderStatus(request):
    if request.method == 'GET':

        orderid = request.GET.get('orderid',None)

        if orderid is None:
            response = {
                "message" : "Please provide OrderID",
                "success": False,
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.get(pk=orderid)
        authorized = check_authorization(request, order.customer.id)
        
        if not authorized:
            response = {
                "message" : "You are not authorized to for this request",
                "success": False,
            }
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)
            
        
        response = {
            "data" : {
                "Order Status" : order.status,
            },
            "message" : "Retrieve order status successfully",
            "success": True,
        }
        return Response(response,status=status.HTTP_200_OK)


    if request.method == 'PUT':

        orderid = request.data.get('orderid', None)
        order_status = request.data.get('status',None)

        if orderid is None or order_status is None:
            response = {
                "message" : "Please provide OrderID and OrderStatus",
                "success": False,
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.get(pk=orderid)
        authorized = check_authorization(request, order.customer.id)

        if not authorized:
            response = {
                "message" : "You are not authorized to for this request",
                "success": False,
            }
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)

        order.status = order_status
        order.save()

        response = {
            "data" : {
                "Order No." : order.id,
                "Order Status" : order.status,
            },
            "message" : "Retrieve order status successfully",
            "success": True,
        }
        return Response(response,status=status.HTTP_200_OK)
