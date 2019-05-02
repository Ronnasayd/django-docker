from rest_framework import serializers
from .models import DDUser


class DDUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DDUser
        fields =  '__all__' 