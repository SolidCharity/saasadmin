# Generated by Django 4.0.4 on 2022-05-05 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_saasproduct_upstream_url_saasproduct_upstream_url_de_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='saasconfiguration',
            name='name_de',
            field=models.CharField(max_length=64, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='saasconfiguration',
            name='name_en',
            field=models.CharField(max_length=64, null=True, verbose_name='name'),
        ),
    ]
