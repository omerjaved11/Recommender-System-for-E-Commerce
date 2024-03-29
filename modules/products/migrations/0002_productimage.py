# Generated by Django 2.0.5 on 2018-10-31 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('product_image_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_image', models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='static/products_images')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.Product')),
            ],
        ),
    ]
