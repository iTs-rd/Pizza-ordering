from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import *


router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('signup/', Signup),
    path('orders/', Orders),
    path('order_status/', OrderStatus),
    path('orders/<int:order_id>/', OrderDetailByID),
    path('all_orders_details/', GetAllOrdersDetails),
    path('user/', UserInfo),
]



# docs  ->  all user  ->  Docs


# user detail  ->  user specific  ->  GetUserInfo


# vier all panding order  ->  superuser  ->  GetAllOrdersDetails
# view all complete order  ->  superuser  ->  GetAllOrdersDetails
# view all order group by state  ->  superuser  ->  GetAllOrdersDetails
# delete order  ->  user specific   ->  OrderDetailByID
# edit order details  ->  user specific  ->  OrderDetailByID
# get a perticular order details  ->  user specific  ->  OrderDetailByID
# create order  ->  all user  ->  Orders
# get all order by user (sorted)  ->  user specific  ->  Orders
# get order statte of perticular order  ->  user specific  ->  OrderStatus
# update-status of order  ->  superuser  ->  OrderStatus