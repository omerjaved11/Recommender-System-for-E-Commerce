# Generated by Django 2.0.5 on 2019-06-30 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_remove_product_product_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerproductreview',
            name='product_review_text',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='customerproductreview',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='customerproductreview',
            name='product_review_id',
        ),
        migrations.DeleteModel(
            name='ProductReview',
        ),
    ]