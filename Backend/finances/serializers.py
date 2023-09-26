from rest_framework import serializers
from .models import *

# 정기 예금
class DOSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd',)

class DPSerializer(serializers.ModelSerializer):
    depositoptions_set = DOSerializer(many=True, read_only=True)
    class Meta:
        model = DepositProducts
        fields = '__all__'

# 정기 적금
class SOSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd',)

class SPSerializer(serializers.ModelSerializer):
    savingoptions_set = SOSerializer(many=True, read_only=True)
    class Meta:
        model = SavingProducts
        fields = '__all__'


        