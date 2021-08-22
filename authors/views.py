from authors.serializers import AuthorSerializer
from authors.models import Author
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import render
from rest_framework import generics


class AuthorCreateView(generics.ListCreateAPIView):
    model = Author
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
