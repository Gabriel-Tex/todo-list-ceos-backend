from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
 
from .serializers import RegisterUserSerializer, UserSerializer
 
 
class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer
 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)
 

 
 
class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
 
    def post(self, request, *args, **kwargs):
        return Response(
            {'message': 'Logout realizado com sucesso.'},
            status=status.HTTP_200_OK,
        )
    
        

