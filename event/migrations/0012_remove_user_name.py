# Generated by Django 4.1.7 on 2023-04-14 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_home'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]