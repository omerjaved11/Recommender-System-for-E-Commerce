# Generated by Django 2.0.5 on 2018-11-01 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20181101_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='product_image',
            field=models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='products_images'),
        ),
    ]