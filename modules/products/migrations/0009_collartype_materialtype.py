# Generated by Django 2.0.5 on 2018-11-01 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20181101_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollarType',
            fields=[
                ('collar_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('collar_type_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialType',
            fields=[
                ('material_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('material_type_name', models.CharField(max_length=50)),
            ],
        ),
    ]
