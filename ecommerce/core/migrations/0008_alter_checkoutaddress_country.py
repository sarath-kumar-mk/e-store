# Generated by Django 4.2.3 on 2024-02-03 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_checkoutaddress_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutaddress',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
