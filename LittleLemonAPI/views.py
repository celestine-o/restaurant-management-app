from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, permission_classes, throttle_classes
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import MenuItem, Category
from .serializers import MenuItemSerializers, CategorySerializers, CartSerializers

# Create your views here.
