# Generated by Django 3.1.5 on 2021-01-25 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('token_endpoint', '0005_auto_20210125_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airplanecollector',
            name='password',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='airplanecollector',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]
