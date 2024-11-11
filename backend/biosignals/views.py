from rest_framework import viewsets
from .models import BioSignals
from .serializers import BioSignalsSerializer

class BioSignalsViewSet(viewsets.ModelViewSet):
    queryset = BioSignals.objects.all()
    serializer_class = BioSignalsSerializer
