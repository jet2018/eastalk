# Generated by Django 3.2.6 on 2021-08-26 11:06

import django.core.validators
from django.db import migrations, models
import modules


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_blog_introductory_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='introductory_file',
            field=models.ImageField(blank=True, help_text='Cover image to introduce the rest of the blog', null=True, upload_to='blog_intros', validators=[django.core.validators.validate_image_file_extension, modules.validate_img_extension]),
        ),
    ]
