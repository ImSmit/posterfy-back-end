from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from base.models import User
from base.serializers import UserSerializer, userSerializerWithToken
from django.contrib.auth.hashers import make_password

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = userSerializerWithToken(user, many=False)
    return Response(serializer.data)


@api_view(["put"])
@permission_classes([IsAuthenticated])
def updateUsers(request):
    user = request.user
    serializer = userSerializerWithToken(user, many=False)
    data = request.data
    user.first_name = data['first_name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUsers(request):
    user_data = User.objects.all()
    serializer = UserSerializer(user_data, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['first_name'],
            username=data['username'],
            password=make_password(data["password"])
        )

        serializer = userSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response({"status": False, 'detail': "Email is already exists"}, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attr):
        data = super().validate(attr)
        serializer = userSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
