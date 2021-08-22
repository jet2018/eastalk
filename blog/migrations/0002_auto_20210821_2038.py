# Generated by Django 3.2.6 on 2021-08-21 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='sub_category',
            field=models.ManyToManyField(blank=True, null=True, to='blog.SubCategory', verbose_name='subCategory'),
        ),
        migrations.AlterField(
            model_name='category',
            name='sub_category',
            field=models.ManyToManyField(blank=True, null=True, to='blog.SubCategory'),
        ),
    ]
