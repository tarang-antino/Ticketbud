# Generated by Django 4.1.7 on 2023-04-14 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0013_user_name_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages='Enter a vaild Username', max_length=20, unique=True),
        ),
    ]
