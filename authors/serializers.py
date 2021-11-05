from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings

from blog.models import Subscribers
from .models import Sponsor, Author


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        Overriding the initial serializers of jwt token obtain
        Adds more fields, hopefully needed for the frontend
    """

    @classmethod
    def get_token(cls, user):
        is_author = False

        try:
            get_user = Author.objects.get(user=user)
            if get_user:
                is_author = True
            else:
                is_author = False
        except Author.DoesNotExist:
            is_author = False

        token = super().get_token(user)
        if settings.DEBUG:
            url = "http://localhost:8000/static/img/img_avatar.png"
            url_short = "http://localhost:8000"
        else:
            url = settings.STATIC_URL_CUSTOM+"img/img_avatar.png"
            url_short = ""

        if is_author:
            image = url_short+user.author.dp.url if user.author.dp else url
        else:
            image = url
        # Add custom claims
        token['username'] = user.username
        token['image'] = image
        token['email'] = user.email
        token['is_author'] = is_author
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token


class AuthorSerializer(serializers.ModelSerializer):
    """ 
        Blog serializers
    """
    current_user = serializers.SerializerMethodField()
    profile_pik = serializers.SerializerMethodField()
    total_followers = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'followers': {'required': False},
        }
        read_only_fields = [
            'slug',
            'registered_on',
            'verified_user',
            'current_user',
        ]

    def get_current_user(self, obj):
        return obj.user.first_name + " " + obj.user.last_name+"("+obj.user.username+")"

    def get_profile_pik(self, obj):
        if settings.DEBUG:
            url = "http://localhost:8000/static/img/img_avatar.png"
            url_short = "http://localhost:8000"
        else:
            url = settings.STATIC_URL_CUSTOM+"img/img_avatar.png"
            url_short = ""

        return url_short+obj.dp.url if obj.dp else url


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    profile_pik = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'profile_pik',
                  'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
            'profile_pik': {'read_only': True, 'required': False},
        }

    def get_profile_pik(self, obj):
        if settings.DEBUG:
            url = "http://localhost:8000/static/img/img_avatar.png"
            url_short = "http://localhost:8000"
        else:
            url = settings.STATIC_URL_CUSTOM+"img/img_avatar.png"
            url_short = ""

        # find_user_in_authors
        try:
            auth = Author.objects.get(user=obj)
        except Author.DoesNotExist:
            return url

        return url_short+obj.author.dp.url if auth.dp else url

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        sent_email = ""
        if self.validated_data['email']:
            sent_email = self.validated_data['email']
        else:
            return JsonResponse({"error": "Email is required"})
        try:
            User.objects.get(email=sent_email)
            return JsonResponse({"error": "Email already belongs to another account."})
        except User.DoesNotExist:
            user = User(
                email=self.validated_data['email'],
                username=self.validated_data['username'],
                first_name=self.validated_data['first_name'],
                last_name=self.validated_data['last_name'],
            )
            if password != password2:
                return JsonResponse({'error': 'Passwords are not matching'})

            user.set_password(password)
            user.save()
        return user


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribers
        fields = "__all__"
