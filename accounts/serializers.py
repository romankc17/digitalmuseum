from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Account


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attr):
        data = super().validate(attr)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['name'] = self.user.name
        data['email'] = self.user.email

        return data

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Account
        fields = (
            'id', 
            'username', 
            'email', 
            'password', 
            'name', 
            'phone',
            'date_joined'
        )
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.is_active = False
        instance.save()
        return instance


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    
        


