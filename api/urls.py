from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import *


router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('signup/', Signup),
    path('orders/', NewOrders),
]


# create order  ->  all user  ->  PlaceOrder
# get order statte of perticular order  ->  user specific  ->  GetOrderStatus
# get all order by user (sorted)  ->  user specific  ->  GetOrdersDetails
# get a perticular order details  ->  user specific  ->  OrderDetailByID
# edit order details  ->  user specific  ->  OrderDetailByID
# vier all panding order  ->  superuser  ->  GetAllOrdersDetails
# view all complete order  ->  superuser  ->  GetAllOrdersDetails
# view all order group by state  ->  superuser  ->  GetAllOrdersDetails
# update-status of order  ->  superuser  ->  UpdateOrderStatus
# delete order  ->  user specific   ->  OrderDetailByID
# docs  ->  all user  ->  Docs
# user detail  ->  user specific  ->  GetUserInfo

