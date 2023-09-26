from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        except_fields = ["follow,"]


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = '__all__'
        read_only_fields = ["are_created",]


class UserdetailSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(read_only=True, many=True)

    class Meta:
        model = User
        exclude = ["groups", "is_superuser",
                   "is_staff", "user_permissions", "first_name", "last_name"]
        
class UserkeywordSerializer(serializers.ModelSerializer):
    select = serializers.CharField(read_only=True)
    # deposit_count = serializers.IntegerField(
    #     source='product_lst.count', read_only=True)
    # saving_count = serializers.IntegerField(
    #     source='product_lst_saving.count', read_only=True)

    class Meta:
        model = User
        fields = ["age", "gender", "select",]
