import email
import os
import json

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.dispatch import receiver
from django.conf import settings

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response as RestReponse

from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .utils import *
from .serializers import *

from django.db import transaction


class UserViewSet(viewsets.ModelViewSet):
	has_user_field = True
	has_state = True
	filter_backends = [DjangoFilterBackend]
	queryset = User.objects.filter(is_active=True).order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAdminUser]
	has_user_field = False
	has_state = False
	filterset_fields = ["groups"]

class GroupViewSet(viewsets.ModelViewSet):
	has_user_field = True
	has_state = True
	filter_backends = [DjangoFilterBackend]
	queryset = Group.objects.all()
	serializer_class = group_serializer
	permission_classes = [permissions.IsAdminUser]
	has_user_field = False
	has_state = False



class AnnonceViewSet(viewsets.ModelViewSet):
	filter_backends = [DjangoFilterBackend]
	permission_classes = [permissions.IsAdminUser]
	queryset = Annonce.objects.all()
	pagination_class = None
	serializers = getSerializer(Annonce)
	serializer_class = serializers[0]
	filterset_fields = ["tag","lieux","photo","author","categorie"]
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return self.serializers[1]
		else:
			return self.serializers[0]


class TagViewSet(viewsets.ModelViewSet):
	filter_backends = [DjangoFilterBackend]
	permission_classes = [permissions.IsAdminUser]
	queryset = Tag.objects.all()
	pagination_class = None
	serializers = getSerializer(Tag)
	serializer_class = serializers[0]
	filterset_fields = ["parent"]
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
	def get_serializer_class(self):
		if self.request.method == 'POST':
			return self.serializers[1]
		else:
			return self.serializers[0]

class CategorieViewSet(viewsets.ModelViewSet):
	filter_backends = [DjangoFilterBackend]
	permission_classes = [permissions.IsAdminUser]
	queryset = Categorie.objects.all()
	pagination_class = None
	serializers = getSerializer(Categorie)
	serializer_class = serializers[0]
	filterset_fields = ["parent"]
	
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return self.serializers[1]
		else:
			return self.serializers[0]

def getViewSet(_model):
	class GetViewSet(viewsets.ModelViewSet):
		filter_backends = [DjangoFilterBackend]
		permission_classes = [permissions.IsAdminUser]
		queryset = _model.objects.all()
		#pagination_class = None
		serializers = getSerializer(_model)
		serializer_class = serializers[0]
		filterset_fields = ["parent"]
		
		def perform_create(self, serializer):
			serializer.save(user=self.request.user)
		def get_serializer_class(self):
			if self.request.method == 'POST':
				return self.serializers[1]
			else:
				return self.serializers[0]
	return GetViewSet

def getViewSet2(_model):
	class GetViewSet(viewsets.ModelViewSet):
		filter_backends = [DjangoFilterBackend]
		permission_classes = [permissions.IsAdminUser]
		queryset = _model.objects.all()
		#pagination_class = None
		serializers = getSerializer(_model)
		serializer_class = serializers[0]
		def perform_create(self, serializer):
			serializer.save(user=self.request.user)

		def get_serializer_class(self):
			if self.request.method == 'POST':
				return self.serializers[1]
			else:
				return self.serializers[0]
	return GetViewSet


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)