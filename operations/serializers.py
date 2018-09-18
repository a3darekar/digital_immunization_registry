from rest_framework import serializers, viewsets
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet

router = DefaultRouter()



router.register(r'devices', FCMDeviceViewSet)
router.register(r'authdevices', FCMDeviceAuthorizedViewSet)