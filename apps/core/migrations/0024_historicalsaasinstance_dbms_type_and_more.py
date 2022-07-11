# Generated by Django 4.0.5 on 2022-07-11 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_historicalsaasplan_descr_1_de_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsaasinstance',
            name='dbms_type',
            field=models.CharField(blank='mysql', choices=[('postgresql', 'PostgreSQL'), ('mysql', 'MySQL/MariaDB')], default='mysql', max_length=64, verbose_name='Database Type'),
        ),
        migrations.AddField(
            model_name='saasinstance',
            name='dbms_type',
            field=models.CharField(blank='mysql', choices=[('postgresql', 'PostgreSQL'), ('mysql', 'MySQL/MariaDB')], default='mysql', max_length=64, verbose_name='Database Type'),
        ),
        migrations.AddField(
            model_name='saasproduct',
            name='dbms_type',
            field=models.CharField(blank='mysql', choices=[('postgresql', 'PostgreSQL'), ('mysql', 'MySQL/MariaDB')], default='mysql', max_length=64, verbose_name='Database Type'),
        ),
    ]
