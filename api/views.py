from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if request.path.split("/")[-2] == "signup":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response = {
                "Message":"Method 'POST' not allowed.",
                "Status":"Decline"
            }
            return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        # edit
        if request.path.split("/")[-2] == "get_user_from_token":

            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            response = {
                "Message":"Method 'GET' not allowed.",
                "Status":"Decline"
            }
            return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)



    def retrieve(self, request, *args, **kwargs):
        response = {'message': 'You can\'t use GET method like this'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        response = {'message': 'You can\'t use PUT method like this'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'You can\'t use DELETE method like this'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

