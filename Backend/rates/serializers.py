from rest_framework import serializers
from .models import *


class RateChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratechange
        fields = '__all__'
        read_only_fields = ['dataDate',]
