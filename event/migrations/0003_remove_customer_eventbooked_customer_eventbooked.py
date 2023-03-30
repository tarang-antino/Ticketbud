# Generated by Django 4.1.7 on 2023-03-23 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_customer_eventbooked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='eventBooked',
        ),
        migrations.AddField(
            model_name='customer',
            name='eventBooked',
            field=models.ManyToManyField(blank=True, null=True, to='event.event'),
        ),
    ]
