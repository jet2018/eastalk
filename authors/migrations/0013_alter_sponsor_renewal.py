# Generated by Django 3.2.6 on 2021-08-26 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0012_alter_author_dp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='renewal',
            field=models.CharField(choices=[('none', 'Not Applicable'), ('month', 'Per month'), ('yearly', 'Per year')], max_length=20),
        ),
    ]
