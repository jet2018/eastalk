# Generated by Django 3.2.6 on 2021-08-24 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_bookmark_bookmarked_on'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscribers',
            options={'verbose_name': 'Subscriber', 'verbose_name_plural': 'Subscribers'},
        ),
    ]
