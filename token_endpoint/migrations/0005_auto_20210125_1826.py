# Generated by Django 3.1.5 on 2021-01-25 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('token_endpoint', '0004_remove_airplanecollector_jwt_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airplanecollector',
            name='password',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='airplanecollector',
            name='username',
            field=models.CharField(max_length=500),
        ),
    ]
