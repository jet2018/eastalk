from authors.models import Author
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from blog.serializers import BlogSerializer
from blog.models import Blog
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics


# Create your views here.
class IndexView(TemplateView):
    template_name = "splash.html"


class BlogListCreateView(generics.ListCreateAPIView):
    """
        Get all articles or create one
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = Blog
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "author__user__username",
                     "category__category_name", "sub_category__sub_category_name"]
    filterset_fields = ["title", "author__user__username",
                        "category__category_name", "sub_category__sub_category_name"]



