from django.db import router
from api.views import PatientModelViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'patients', PatientModelViewSet)
