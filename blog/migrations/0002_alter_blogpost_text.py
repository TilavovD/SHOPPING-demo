# Generated by Django 4.1.3 on 2022-11-10 11:09

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]