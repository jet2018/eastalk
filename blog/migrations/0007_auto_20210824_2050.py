# Generated by Django 3.2.6 on 2021-08-24 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_subscribers_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribers',
            name='subscriber_type',
            field=models.CharField(choices=[('one', 'Singular'), ('two', 'Category'), ('three', 'Everything')], default='three', max_length=15),
        ),
        migrations.AlterField(
            model_name='subscribers',
            name='subscription_length',
            field=models.CharField(choices=[('one', 'One month'), ('two', 'Six months'), ('three', 'One year'), ('four', 'Life time')], default='four', max_length=15),
        ),
    ]
