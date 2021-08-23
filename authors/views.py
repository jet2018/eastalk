from blog.models import Subscribers
from authors.serializers import AuthorSerializer
from authors.models import Author
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.response import Response


@api_view(['POST'])
def Subscribe(request):
    """
        Subscribe to a category, for a while or everything

        Args:
            duration(optional): If provided, will be set as the timeframe for subscription
            type(optional): If provided, will be set as the topic being subscribed on
            email(required): Email subscribing
    """
    subscription_length = request.post.get(
        'duration') if request.post.get('duration') else None
    subscriber_type = request.post.get(
        'type') if request.post.get('type') else None
    if request.post.get('email'):
        email = request.post.get('email')
    else:
        return JsonResponse({"error": "Email is required to subscribe"})

    subscribe = Subscribers(
        email=email, subscriber_type=subscriber_type, subscription_length=subscription_length)
    subscribe.save()
    return Response({"success": "{} subscribed successfully".format(email)})


class AuthorCreateView(generics.ListCreateAPIView):
    model = Author
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
