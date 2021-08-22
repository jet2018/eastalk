from blog.models import Blog
from django.core.exceptions import ValidationError
from rest_framework.fields import ChoiceField, ReadOnlyField
from django.db.models.base import Model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from django.contrib.auth.models import User


class BlogSerializer(serializers.ModelSerializer):
    """ 
        Blog serializers
    """
    class Meta:
        model = Blog  # the model we working on
        fields = '__all__'  # including all fields at ago
        # these fields will be read, but a user can't add anything on them.
        read_only_fields = [
            'slug',
            'posted_on'
        ]
