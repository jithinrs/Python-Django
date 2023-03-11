"""
1. Suppose you have two model with name user and customer. And customer are related to user with one to one relationship. You have to create a rest api view for create a customer.
Field of user are:- 
a) first_name
b) last_name
c) email
d) mobile no.
And field of customer are:-
a) profile number
Note:- email and mobile number are unique.


"""


#Models

from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    email = models.CharField(max_length=127)
    mobile_number = models.IntegerField()

class Customer(models.Model):
    profile_number = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user_relation')



#Serializers

from .models import User, Customer

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset=User.objects.all())])
    mobile_number = serializers.IntegerField(required = True, validators = [UniqueValidator(queryset=User.objects.all())])
    
    class Meta:
        model = User
        fields = '__all__'



#views.py

from .models import User, Customer
from .serializers import UserSerializer

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status


class CreateNew(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_id = serializer.data.get('id')
            user = User.objects.get(id = user_id)
            Customer.objects.create(
                profile_number = user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data = 'Something Went wrong', status=status.HTTP_400_BAD_REQUEST)