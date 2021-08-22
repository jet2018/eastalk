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
    model = Blog
    serializer_class = BlogSerializer
