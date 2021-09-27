from rest_framework import serializers
from rest_framework.fields import ChoiceField
import os
from django.core.exceptions import ValidationError


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


def validate_img_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_image_size(fieldfile_obj):
    filesize = fieldfile_obj.image.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError(
            "Maximum supported file size is %sMB" % str(megabyte_limit))
