from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import jwt
from django.contrib.auth.models import User
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
    serializer_class=UserSerializer
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response = {
            'data' : serializer.data,
            "message" : "User created successfully.",
            "success": True,
        }
        return Response(response,status=status.HTTP_201_CREATED)

    response = {
        'data' : serializer.errors,
        "message" : "User not created.",
        "success": False,
    }
    return Response(response,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Orders(request):
    if request.method == 'GET':
        user = get_id_from_token(request.headers["Authorization"][7:])
        orders = Order.objects.filter(customer=user).order_by('-placed_at')
        serializer=OrderSerializer(data=orders,many=True)
        serializer.is_valid()

        response = {
            'data' : serializer.data,
            "message" : "Your orders details.",
            "success": True,
        }
        return Response(response,status=status.HTTP_200_OK)

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
                "message" : "Thank You For Choosing Us.",
                "success": True,
            }
            return Response(response,status=status.HTTP_201_CREATED)

        response = {
            'data' : serializer.errors,
            "message" : "Order not placed.",
            "success": False,
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def OrderStatus(request):
    if request.method == 'GET':

        orderid = request.GET.get('orderid',None)

        if orderid is None:
            response = {
                "message" : "Please provide OrderID.",
                "success": False,
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.get(pk=orderid)
        authorized = check_authorization(request, order.customer.id)
        
        if not authorized:
            response = {
                "message" : "You are not authorized to for this request.",
                "success": False,
            }
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)
            
        
        response = {
            "data" : {
                "Order Status" : order.status,
            },
            "message" : "Retrieve order status successfully.",
            "success": True,
        }
        return Response(response,status=status.HTTP_200_OK)

    if request.method == 'PUT':

        orderid = request.data.get('orderid', None)
        order_status = request.data.get('status',None)

        if orderid is None or order_status is None:
            response = {
                "message" : "Please provide OrderID and OrderStatus.",
                "success": False,
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.get(pk=orderid)
        super = check_for_super_user(request.headers["Authorization"][7:])

        if not super:
            response = {
                "message" : "You are not authorized to for this request.",
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
            "message" : "Retrieve order status successfully.",
            "success": True,
        }
        return Response(response,status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def OrderDetailByID(request,order_id):
    if request.method == 'GET':
        order = Order.objects.get(pk=order_id)
        authorized = check_authorization(request, order.customer.id)
        if not authorized:
            response = {
                "message" : "You are not authorized to for this request.",
                "success": False,
            }
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)

        serializer=OrderSerializer(order)

        response = {
            'data' : serializer.data,
            "message" : "Your orders details.",
            "success": True,
        }
        return Response(response,status=status.HTTP_200_OK)

    if request.method == 'PUT':
        order = Order.objects.get(pk=order_id)
        authorized = check_authorization(request, order.customer.id)
        if not authorized:
            response = {
                "message" : "You are not authorized to for this request.",
                "success": False,
            }
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)


        if order.status not in ["Pending"]:
            response = {
                "message" : "You can't update your order details because your order is already %s." % (order.status),
                "success": False,
            }
            return Response(response,status=status.HTTP_403_FORBIDDEN)

        new_size = request.data.get('size',None)
        new_quantity = request.data.get('quantity',None)
        new_flavour = request.data.get('flavour',None)

        if new_size is None and new_quantity is None and new_flavour is None:
            response = {
                "message" : "Please provide Size or Quantity or flavour.",
                "success": False,
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        if new_size is not None:
            if not new_size in ["small", "medium", "large", "extraLarge"]:
                response = {
                    "data" : {
                        "size" : "Please provide proper size"
                    },
                    "message" : "Request not processed.",
                    "success": False,
                }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            order.size = new_size

        if new_quantity is not None:
            if len(new_quantity) == 0:
                response = {
                    "data" : {
                        "quantity" : "Please provide proper quantity"
                    },
                    "message" : "Request not processed.",
                    "success": False,
                }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            order.quantity = new_quantity
        
        if new_flavour is not None:
            order.flavour = new_flavour
        
        order.save()
        serializer=OrderMiniSerializer(order)

        response = {
            'data' : serializer.data,
            "message" : "Your orders update successfully.",
            "success": True,
        }
        return Response(response,status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        try:
            order = Order.objects.get(pk=order_id)
        except:
            response = {
                "message" : "No order exist with order no. %s." % (order_id),
                "success": False,
            }
            return Response(response,status=status.HTTP_404_NOT_FOUND)

        authorized = check_authorization(request, order.customer.id)
        if not authorized:
            response = {
                "message" : "You are not authorized to for this request.",
                "success": False,
            }
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)

        order.delete()

        response = {
            "message" : "Your order deleted successfully.",
            "success": True,
        }
        return Response(response,status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def GetAllOrdersDetails(request):
    if request.method == 'GET':
        get_status = request.GET.get('status',None)
        if get_status is not None:
            if not get_status in ["Pending", "Inprocess", "Prepared", "On_the_way", "Delevered"]:
                response = {
                    "message" : "Please provide proper status value.",
                    "success": False,
                }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.filter(status=get_status).order_by('-updated_at')
        else:
            order = Order.objects.all().order_by('-updated_at')
        serializer=OrderSerializer(data=order,many=True)
        serializer.is_valid()
        response = {
            "data" : serializer.data,
            "message" : "Orders details send successfully",
            "success": True,
        }
        return Response(response,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserInfo(request):
    if request.method == 'GET':
        user_id = get_id_from_token(request.headers["Authorization"][7:])
        # user = Order.objects.get(pk=2)
        user = User.objects.get(pk=user_id)
        print(user.username,"\n\n\n")
        serializer = UserSerializer1(data=user)
        serializer.is_valid()
        # print(serializer.is_valid())
        return Response(user_id,status=status.HTTP_400_BAD_REQUEST)
        
    pass