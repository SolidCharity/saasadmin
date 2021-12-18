# Generated by Django 4.0 on 2021-12-18 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0014_saasproduct_saasproductlanguage'),
    ]

    operations = [
        migrations.AddField(
            model_name='saasinstance',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saasproduct'),
        ),
        migrations.AddField(
            model_name='saasplan',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saasproduct'),
        ),
        migrations.AlterField(
            model_name='saascontract',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saascustomer'),
        ),
        migrations.AlterField(
            model_name='saascontract',
            name='instance',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saasinstance'),
        ),
        migrations.AlterField(
            model_name='saascontract',
            name='plan',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saasplan'),
        ),
        migrations.AlterField(
            model_name='saasinstance',
            name='reserved_for_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='saasproductlanguage',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saasproduct'),
        ),
        migrations.AlterModelTable(
            name='saasproduct',
            table='saas_product',
        ),
        migrations.AlterModelTable(
            name='saasproductlanguage',
            table='saas_product_language',
        ),
    ]
