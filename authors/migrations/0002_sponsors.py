# Generated by Django 3.2.6 on 2021-08-21 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_name', models.CharField(max_length=100)),
                ('sponsor_logo', models.ImageField(upload_to='Sponsors')),
                ('amount', models.FloatField()),
                ('short_bio', models.TextField(max_length=400)),
                ('sponsor_from', models.DateTimeField(auto_now=True)),
                ('renewal', models.CharField(choices=[('month', 'Per month'), ('yearly', 'Per year')], max_length=20)),
            ],
        ),
    ]