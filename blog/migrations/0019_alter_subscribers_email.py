# Generated by Django 3.2.6 on 2021-09-07 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_blog_blog_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribers',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
