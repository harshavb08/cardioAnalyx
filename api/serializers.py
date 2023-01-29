from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

	password = serializers.CharField(
		write_only=True,
		required=False,
		help_text='Leave empty if no change needed',
		style={'input_type': 'password', 'placeholder': 'Password'}
	)

	class Meta:
		model = User
		fields = ['id', 'first_name', 'last_name',
				  'username', 'email', 'password', 'groups', 'url']

	def create(self, validated_data):
		validated_data['password'] = make_password(
			validated_data.get('password'))
		return super(UserSerializer, self).create(validated_data)

	def update(self, instance, validated_data):
		if 'password' in validated_data:
			validated_data['password'] = make_password(
				validated_data.get('password'))
		return super().update(instance, validated_data)



class permission_serializer(serializers.ModelSerializer):

	class Meta:
		model = Permission


class group_serializer(serializers.ModelSerializer):

	class Meta:
		model = Group
		exclude = ['permissions']



def getSerializer(_model):

	class PostSerializer(serializers.ModelSerializer):

		class Meta:
			model = _model
			exclude =[ 'user']

	class GetSerializer(serializers.ModelSerializer):

		class Meta:
			model = _model
			depth = 10
			fields = '__all__'

	return [GetSerializer, PostSerializer]






