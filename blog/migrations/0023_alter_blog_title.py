# Generated by Django 3.2.6 on 2021-11-10 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20211106_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(blank=True, help_text='Unique, catchy topic of the article', max_length=250, null=True),
        ),
    ]
