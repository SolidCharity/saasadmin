# Generated by Django 4.1.1 on 2023-01-20 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_alter_saasproduct_login_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsaascustomer',
            name='organisation_name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='organisation_name'),
        ),
        migrations.AlterField(
            model_name='saascustomer',
            name='organisation_name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='organisation_name'),
        ),
    ]
