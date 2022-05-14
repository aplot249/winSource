# Generated by Django 3.2 on 2022-05-07 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20220506_1321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('PartNo',), 'verbose_name': '产品信息', 'verbose_name_plural': '产品信息'},
        ),
        migrations.AlterField(
            model_name='product',
            name='ProductionPDFLink',
            field=models.URLField(blank=True, db_column='item_availablity_pdf', default=None, max_length=512, verbose_name='产品详情PDF链接'),
        ),
    ]