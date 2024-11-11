from rest_framework import serializers
from .models import BioSignals

class BioSignalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BioSignals
        fields = '__all__'  # 或列出具体字段
