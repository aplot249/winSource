# Generated by Django 3.2 on 2022-05-05 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Manufacture',
            field=models.CharField(db_column='item_detail_manufacturer_title', max_length=128, verbose_name='制造商'),
        ),
    ]
