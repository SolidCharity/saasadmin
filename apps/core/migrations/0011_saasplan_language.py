# Generated by Django 3.2.9 on 2021-11-23 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20211116_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='saasplan',
            name='language',
            field=models.CharField(default='DE', max_length=10, verbose_name='language'),
        ),
    ]
