from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
class UserSerializer(serializers.ModelSerializer):
    '''
        name: after get_ we can specify any variable name we want just need to use in field
    '''

    _id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'full_name', 'is_admin']

    def get_name(self, obj):
        name = obj.first_name
        if not name:
            name = obj.email
        return name
    
    def get_full_name(self, obj):
        full_name = obj.first_name + " "+ obj.last_name
        if not full_name:
            full_name = obj.email
        return full_name
    
    def get__id(self, obj):
        _id = obj.id
        return _id
    
    def get_is_admin(self, obj):
        is_admin = obj.is_staff
        return is_admin

class userSerializerWithToken(UserSerializer):
    '''
    This class is inherited from above class to get token
    '''
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'full_name', 'is_admin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, obj):
        return f"{settings.BASE_URL}{obj.image.url}"
