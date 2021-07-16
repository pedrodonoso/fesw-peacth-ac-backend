from django.db import router
from api.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'patients', PatientModelViewSet)
router.register(r'clinical_control', ClinicalControlViewSet)
router.register(r'LogWTDparameters', LogWTDparametersViewSet)
#router.register(r'frequency_distribution', DistributionVizualitation.as_view())
