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



def get_id_from_token(token):
    user = jwt.decode(token,Config.JWT_SECRET_KEY, algorithms=['HS256'])
    return user["user_id"]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def NewOrders(request):
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



