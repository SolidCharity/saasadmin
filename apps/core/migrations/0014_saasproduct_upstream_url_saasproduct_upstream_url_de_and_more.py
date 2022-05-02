# Generated by Django 4.0.4 on 2022-05-02 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_saasproduct_description_saasproduct_description_de_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='saasproduct',
            name='upstream_url',
            field=models.CharField(default='https://example.org', max_length=250, verbose_name='Upstream_URL'),
        ),
        migrations.AddField(
            model_name='saasproduct',
            name='upstream_url_de',
            field=models.CharField(default='https://example.org', max_length=250, null=True, verbose_name='Upstream_URL'),
        ),
        migrations.AddField(
            model_name='saasproduct',
            name='upstream_url_en',
            field=models.CharField(default='https://example.org', max_length=250, null=True, verbose_name='Upstream_URL'),
        ),
    ]
