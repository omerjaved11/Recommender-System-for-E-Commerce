# Generated by Django 2.0.5 on 2019-02-23 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='timestamp2',
        ),
    ]