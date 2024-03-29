# Generated by Django 4.0.5 on 2022-06-20 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0021_saasinstance_additional_storage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalSaasPlan',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('slug', models.CharField(max_length=16, verbose_name='slug')),
                ('name', models.CharField(max_length=16, verbose_name='name')),
                ('priority', models.IntegerField(default=0, verbose_name='Sorting Order')),
                ('is_favourite', models.BooleanField(default=False, verbose_name='is favourite')),
                ('is_public', models.BooleanField(default=True, verbose_name='is public')),
                ('period_length_in_months', models.IntegerField(default=0, verbose_name='Period Length in Months')),
                ('period_length_in_days', models.IntegerField(default=0, verbose_name='Period Length in Days')),
                ('currency_code', models.CharField(default='EUR', max_length=3, verbose_name='Currency')),
                ('cost_per_period', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cost per Period')),
                ('notice_period_in_days', models.IntegerField(verbose_name='Notice Period in Days')),
                ('descr_target', models.CharField(default='TODO', max_length=200, verbose_name='Description Target')),
                ('descr_caption', models.CharField(default='TODO', max_length=200, verbose_name='Description Caption')),
                ('descr_1', models.CharField(default='TODO', max_length=200, verbose_name='Description 1')),
                ('descr_2', models.CharField(default='TODO', max_length=200, verbose_name='Description 2')),
                ('descr_3', models.CharField(default='TODO', max_length=200, verbose_name='Description 3')),
                ('descr_4', models.CharField(default='TODO', max_length=200, verbose_name='Description 4')),
                ('quota_storage', models.CharField(default='0M', max_length=20, verbose_name='Quota for Storage')),
                ('quota_app', models.CharField(default='500M', max_length=20, verbose_name='Quota for Application')),
                ('cost_for_storage', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cost for Storage')),
                ('additional_storage_size', models.CharField(default='', max_length=10, verbose_name='Additional Storage Size')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.saasproduct')),
            ],
            options={
                'verbose_name': 'historical saas plan',
                'verbose_name_plural': 'historical saas plans',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSaasInstance',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('identifier', models.CharField(max_length=16, verbose_name='identifier')),
                ('hostname', models.CharField(default='localhost', max_length=128, verbose_name='Hostname')),
                ('pacuser', models.CharField(default='xyz00', max_length=128, verbose_name='Packet User')),
                ('channel', models.CharField(default='stable', max_length=128, verbose_name='Channel')),
                ('first_port', models.IntegerField(default=-1, verbose_name='First Port')),
                ('last_port', models.IntegerField(default=-1, verbose_name='Last Port')),
                ('activation_token', models.CharField(max_length=64, null=True)),
                ('custom_domain', models.CharField(default='', max_length=250, verbose_name='Custom Domain')),
                ('additional_storage', models.IntegerField(default=0, verbose_name='Additional Storage')),
                ('status', models.CharField(default='in_preparation', max_length=16, verbose_name='Status')),
                ('db_password', models.CharField(default='topsecret', max_length=64, verbose_name='DB Password')),
                ('initial_password', models.CharField(default='topsecret', max_length=64, verbose_name='Initial Password')),
                ('password1', models.CharField(default='topsecret', max_length=64, verbose_name='Password1')),
                ('password2', models.CharField(default='topsecret', max_length=64, verbose_name='Password2')),
                ('django_secret_key', models.CharField(default='topsecret', max_length=64, verbose_name='Django Secret Key')),
                ('last_interaction', models.DateTimeField(null=True, verbose_name='Last Interaction')),
                ('reserved_token', models.CharField(max_length=64, null=True, verbose_name='Reserved Token')),
                ('reserved_until', models.DateTimeField(null=True, verbose_name='Reserved Until')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.saasproduct')),
                ('reserved_for_user', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical saas instance',
                'verbose_name_plural': 'historical saas instances',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSaasCustomer',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_newsletter_subscribed', models.BooleanField(default=False, verbose_name='Subscribed to newsletter')),
                ('newsletter_subscribed_on', models.DateTimeField(null=True, verbose_name='newsletter_subscribed_on')),
                ('newsletter_cancelled', models.DateTimeField(null=True, verbose_name='newsletter_cancelled')),
                ('language_code', models.CharField(default='de', max_length=16, verbose_name='language_code')),
                ('organisation_name', models.CharField(max_length=64, null=True, verbose_name='organisation_name')),
                ('title', models.CharField(blank=True, choices=[('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Mr Dr', 'Mr Dr'), ('Mrs Dr', 'Mrs Dr')], max_length=64, verbose_name='Title')),
                ('first_name', models.CharField(default='', max_length=64, verbose_name='First Name')),
                ('last_name', models.CharField(default='', max_length=64, verbose_name='Last Name')),
                ('street', models.CharField(default='', max_length=64, verbose_name='Street and housenumber')),
                ('post_code', models.CharField(default='', max_length=10, verbose_name='Post Code')),
                ('city', models.CharField(default='', max_length=16, verbose_name='City')),
                ('country_code', django_countries.fields.CountryField(default='DE', max_length=2, verbose_name='Country')),
                ('email_address', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical saas customer',
                'verbose_name_plural': 'historical saas customers',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSaasContract',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('start_date', models.DateField(null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(null=True, verbose_name='End Date')),
                ('latest_cancel_date', models.DateField(null=True, verbose_name='Latest Cancel Date')),
                ('is_auto_renew', models.BooleanField(default=True, verbose_name='Is Renewing Automatically')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='Is Confirmed')),
                ('payment_method', models.CharField(default='SEPA_TRANSFER', max_length=20, verbose_name='Payment Method')),
                ('account_owner', models.CharField(default='', max_length=200, null=True, verbose_name='Account Owner')),
                ('account_iban', models.CharField(default='', max_length=64, null=True, verbose_name='Account IBAN')),
                ('sepa_mandate', models.CharField(default='', max_length=64, null=True, verbose_name='SEPA Mandate')),
                ('sepa_mandate_date', models.DateField(null=True, verbose_name='Date of SEPA Mandate')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('customer', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.saascustomer')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('plan', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.saasplan')),
            ],
            options={
                'verbose_name': 'historical saas contract',
                'verbose_name_plural': 'historical saas contracts',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
