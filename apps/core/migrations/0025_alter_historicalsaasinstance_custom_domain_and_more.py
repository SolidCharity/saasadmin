# Generated by Django 4.0.6 on 2022-08-19 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_historicalsaasinstance_dbms_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsaasinstance',
            name='custom_domain',
            field=models.CharField(default='', max_length=250, null=True, verbose_name='Custom Domain'),
        ),
        migrations.AlterField(
            model_name='saasinstance',
            name='custom_domain',
            field=models.CharField(default='', max_length=250, null=True, verbose_name='Custom Domain'),
        ),
    ]
