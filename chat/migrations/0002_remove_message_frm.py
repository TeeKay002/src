# Generated by Django 5.0 on 2024-01-09 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='frm',
        ),
    ]
