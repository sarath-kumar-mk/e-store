# Generated by Django 5.0.1 on 2024-02-08 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_contact_sentmsg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutaddress',
            name='zip_code',
            field=models.CharField(max_length=6),
        ),
    ]
