from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

import random

from .serializers import AccountSerializer, CustomTokenObtainPairSerializer, VerifyAccountSerializer
from .models import Account
from .utils import Util


@permission_classes((AllowAny,))
class RegisterView(APIView):
    def post(self, request):   
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()

        account = serializer.instance        

        otp = random.randint(100000, 999999)
        data = {
            'to': account.email,
            'subject': 'Verify your email address',
            'body': f'Hi {account.name} !! \n Your otp is: \n\n {otp}'
        }        
        # Util.send_email(data)
        Util.send_otp_vai_email(data)
        account.otp = otp
        account.save()

        
        return Response(serializer.data, status=201)


class SendVerificationOTP(APIView):
    def get(self, request):
        email = request.GET.get('email')
        print(email)
        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({'error':"Account does not exist"},status=400)
            
        if account.is_active:
            return Response({'error':'Account is already active'},status=400)

        otp = random.randint(100000, 999999)
        data = {
            'to': account.email,
            'subject': 'Verify your email address',
            'body': f'Hi {account.name} !! \n Your otp is: \n\n {otp}'
        }        
        # Util.send_email(data)
        Util.send_otp_vai_email(data)
        account.otp = otp
        account.save()
        return Response({"message":"Successfully Verification OTP sent."},status=200)


class VerifyOTP(APIView):
    def post(self, request):
        data = request.data
        serializer = VerifyAccountSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({'error':'Account does not exist'},status=400)

        if account.is_active:
            return Response({'error':"Account already verified"},status=400)
            
        if account.otp == otp:
            account.is_active = True
            account.save()
            return Response({
                'message':'Account verified successfully',
                'token':str(RefreshToken.for_user(account).access_token),
                'username':account.username,
                'name':account.name,
                'email':account.email,
            },status=200)

        return Response({'error':'Invalid OTP'},status=400)
              
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer