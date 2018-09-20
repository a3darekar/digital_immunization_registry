# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializers import BabySerializer, ParentSerializer, ClinitianSerializer
from django.contrib.auth.models import User

from .models import Parent, Baby, Clinitian

# Create your views here.
def index(request):
	return HttpResponse("<h2>Error 403.</h2> You are not authorised to access this page. For further details, please contact Site Administrator.")

class ParentList(generics.ListAPIView):
	serializer_class = ParentSerializer

	def get_queryset(self):
		"""
		This view should return a list of all the purchases
		for the currently authenticated user.
		"""
		user = self.request.user
		return Parent.objects.filter(user=user)

class ClinitianList(generics.ListAPIView):
	serializer_class = ClinitianSerializer

	def get_queryset(self):
		"""
		This view should return a list of all the purchases
		for the currently authenticated user.
		"""
		user = self.request.user
		return Clinitian.objects.filter(user=user)

class BabyList(generics.RetrieveAPIView):
	serializer_class = BabySerializer

	def get_queryset(self):
		"""
		This view should return a list of all the purchases for
		the user as determined by the pk portion of the URL.
		"""
		pk = self.kwargs['pk']
		baby = Baby.objects.filter(pk = pk)
		return baby

class BabyTagList(generics.ListAPIView):
	serializer_class = BabySerializer

	def get_queryset(self):
		queryset 	= Baby.objects.none()
		tag 		= self.request.query_params.get('tag', None)
		parent 		= self.request.query_params.get('parent', None)
		name 		= self.request.query_params.get('name', None)
		aadhaar 	= self.request.query_params.get('aadhaar', None)
		if tag is not None:
			queryset = Baby.objects.filter(tag=tag)
		elif name is not None:
			queryset = Baby.objects.filter(first_name__contains = name) | Baby.objects.filter(last_name__contains = name) 
		elif parent is not None:
			queryset = Baby.objects.filter(parent = parent)
		elif aadhaar is not None:
			parent = Parent.objects.filter(unique_id = aadhaar)
			print parent
			queryset = Baby.objects.filter(parent = parent)
		return queryset