from django.urls import path

from .views import *

urlpatterns = [
    path('signup/', Signup),
    path('orders/', Orders),
    path('order_status/<int:orderid>/', OrderStatus),
    path('orders/<int:order_id>/', OrderDetailByID),
    path('all_orders_details/', GetAllOrdersDetails),
    path('user/', UserInfo),
]
