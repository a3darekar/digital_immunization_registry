# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from .models import Parent, Baby, Clinitian

# Create your views here.
def index(request):
	return HttpResponse("<h2>Error 403.</h2> You are not authorised to access this page. For further details, please contact Site Administrator.")
