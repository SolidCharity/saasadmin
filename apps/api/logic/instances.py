from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
import requests
from django.contrib.auth.models import User
from django.db import connection
from django.db import transaction
from django.conf import settings
from apps.core.models import SaasInstance, SaasProduct, SaasContract

class LogicInstances:
    def random_password(self, withSpecialChars):
        # add some lowercase characters
        pwd = User.objects.make_random_password(length=6, allowed_chars='abcdefghijklmnopqrstuvwxyz')
        # add some uppercase characters
        pwd += User.objects.make_random_password(length=6, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        # add some digits
        pwd += User.objects.make_random_password(length=2, allowed_chars='123456789')
        if withSpecialChars:
            # add some special characters
            pwd += User.objects.make_random_password(length=2, allowed_chars='!§$%&/=?:;.,_-<>{}[]()')
        # now shuffle
        list_pwd = list(pwd)
        random.shuffle(list_pwd)
        return ''.join(list_pwd)

    @transaction.atomic
    def create_new_instance(self, hostname, pacuser, product):
        # generate new password
        new_password = self.random_password(False)
        # generate the db password
        db_password = self.random_password(False)
        # the activation token that allows us to activate the instance
        activation_token = self.random_password(False)

        # find new available identifier
        instance_id_start = settings.INSTANCE_ID_START
        instance_id_end = settings.INSTANCE_ID_END
        startport = settings.PORT_START
        endport = settings.PORT_END
        new_id = random.randrange(instance_id_start, instance_id_end)
        while SaasInstance.objects.filter(identifier=str(new_id), product = product).exists():
          new_id = random.randrange(instance_id_start, instance_id_end)

        # find new available port on that host, independant of the product
        new_port = -1
        last_port = -1
        if product.number_of_ports > 0:
          if SaasInstance.objects.filter(hostname=hostname).exists():
            with connection.cursor() as cursor:
              sql = """SELECT MAX(last_port) FROM saas_instance WHERE hostname = %s"""
              cursor.execute(sql, [hostname,])
              port_result = cursor.fetchone()
              if port_result:
                new_port = port_result[0]
          if new_port < startport:
            new_port = startport
          last_port = new_port + product.number_of_ports - 1

        if new_port > endport:
          return False, {}

        # store to database
        instance = SaasInstance.objects.create(
          identifier = str(new_id),
          hostname = hostname,
          pacuser = pacuser,
          activation_token = activation_token,
          product = product,
          first_port = new_port,
          last_port = last_port,
          initial_password = new_password,
          db_password = db_password,
          status = SaasInstance().IN_PREPARATION)

        # return the result
        return True, {'new_id': new_id, 'new_password': new_password, 'db_password': db_password, 'hostname': hostname, 'port': new_port};

    def get_number_of_available_instances(self, product):
        return SaasInstance.objects.filter(product=product).filter(status=SaasInstance().AVAILABLE).count()

    def activate_instance(self, customer, product, instance):

        url = product.activation_url
        if not url:
            url = product.instance_url.replace("https://", "https://saas.") + "/saas_activate.php?SaasActivationPassword=#SaasActivationPassword&UserEmailAddress=#UserEmailAddress"

        PasswordResetToken = None
        if '#PasswordResetToken' in url:
            PasswordResetToken = User.objects.make_random_password(length=16)
            url = url.replace('#PasswordResetToken', PasswordResetToken)

        # for local tests
        if "example.org" in url:
            return [True, PasswordResetToken]

        if instance.activation_token:
            url = url.replace('#SaasActivationPassword', instance.activation_token)

        url = url. \
            replace('#Prefix', product.prefix). \
            replace('#Identifier', instance.identifier). \
            replace('#UserEmailAddress', customer.email_address)

        try:
            resp = requests.get(url=url)
            data = resp.json()
            if not data['success']:
                return [False, None]
        except Exception as ex:
            print('Exception in activate_instance: %s' % (ex,))
            return [False, None]

        return [True, PasswordResetToken]

    def deactivate_instance(self, product, instance):
        """call web request: deactivate_url"""
        url = product.deactivation_url

        if not url:
            url = product.instance_url.replace("https://", "https://saas.") + "/saas_deactivate.php?SaasActivationPassword=#SaasActivationPassword"

        # for local tests
        if "example.org" in url:
            return True

        if instance.activation_token:
            url = url.replace('#SaasActivationPassword', instance.activation_token)

        url = url. \
            replace('#Prefix', product.prefix). \
            replace('#Identifier', instance.identifier)

        try:
            resp = requests.get(url=url)
            data = resp.json()
            if not data['success']:
                return False
        except Exception as ex:
            print('Exception in deactivate_instance: %s' % (ex,))
            return False

        return True

    def deactivate_expired_instances(self):
        """ to be called by a cronjob each night """
        contracts = SaasContract.objects.filter(is_confirmed = True, \
            is_auto_renew = False, end_date__lt = datetime.today(), instance__status = SaasInstance().ASSIGNED)
        for contract in contracts:
            instance = contract.instance
            if self.deactivate_instance(instance.product, instance):
                instance.status = instance.EXPIRED
                instance.save()

    def mark_deactivated_instances_for_deletion(self):
        """ to be called by a cronjob each night """
        contracts = SaasContract.objects.filter(is_confirmed = True, \
            is_auto_renew = False, end_date__lt = datetime.today(), instance__status = SaasInstance().EXPIRED)
        for contract in contracts:
            days = 30
            if contract.plan.period_length_in_months == 0:
                if contract.plan.period_length_in_days == 1:
                    # for the one day test instance, remove it immediately
                    days = 0
                elif contract.plan.period_length_in_days > 0:
                    # for other test instances, remove it after 3 days
                    days = 3

            if contract.end_date + timedelta(days=days) < datetime.today().date():
                instance = contract.instance
                instance.status = instance.TO_BE_REMOVED
                instance.save()
