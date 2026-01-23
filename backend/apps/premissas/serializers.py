from rest_framework import serializers
from .models import Premissa

class PremissaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premissa
        fields = '__all__'
