# Generated by Django 2.0.5 on 2018-10-31 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20181031_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='product_image',
            field=models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='products_images'),
        ),
    ]