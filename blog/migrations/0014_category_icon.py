# Generated by Django 3.2.6 on 2021-08-26 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_blog_introductory_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.CharField(default='pi pi-fw pi-angle-double-right', max_length=30),
        ),
    ]