# Generated by Django 4.1.3 on 2022-11-11 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='secret_key',
            field=models.CharField(max_length=6, null=True, verbose_name='phone verification key'),
        ),
    ]
