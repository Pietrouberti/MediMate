from .models import User
from rest_framework import serializers


# serializer to transform User object into JSON for transmission to frontend
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')