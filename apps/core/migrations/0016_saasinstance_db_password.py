# Generated by Django 4.0 on 2021-12-22 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_saasinstance_product_saasplan_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='saasinstance',
            name='db_password',
            field=models.CharField(default='topsecret', max_length=64, verbose_name='DB Password'),
        ),
    ]