from blog.models import Blog
from django.contrib.auth import models
from django.core.exceptions import ValidationError
from rest_framework.fields import ChoiceField, ReadOnlyField
from django.db.models.base import Model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from django.contrib.auth.models import User


class DisplayNameWritableField(serializers.ChoiceField):
    """
        Class that returs the display text on the choices\n
        ex.\n
        roles = [('te', 'Teacher)], returns 'Teacher' instead of the default behaviour of 'te'\n
        ##NOTE: not to be tempered with.
    """

    def __init__(self, **kwargs):
        self.html_cutoff = kwargs.pop('html_cutoff', self.html_cutoff)
        self.html_cutoff_text = kwargs.pop(
            'html_cutoff_text', self.html_cutoff_text)

        self.allow_blank = kwargs.pop('allow_blank', False)
        super(ChoiceField, self).__init__(**kwargs)

    def to_representation(self, value):
        return self.choices.get(value, value)

    def bind(self, field_name, parent):
        super().bind(field_name, parent)
        self.choices = parent.Meta.model._meta.get_field(field_name).choices


class BlogSerializer(serializers.ModelSerializer):
    """ 
        Blog serializers
    """
    class Meta:
        model = Blog  # the model we working on
        fields = '__all__'  # including all fields at ago
        # these fields will be read, but a user can add anything on them.
        # read_only_fields = [
        #     'slug',
        #     'added_on'
        # ]
