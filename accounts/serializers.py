from rest_framework import serializers

from accounts.models import Account


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
            'is_staff', 
            'is_active', 
            'date_joined'
        )
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
        


