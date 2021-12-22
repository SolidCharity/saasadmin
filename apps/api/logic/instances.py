from apps.core.models import SaasInstance
from django.contrib.auth.models import User
from django.db import connection
import random
from django.db import transaction

class LogicInstances:
    @transaction.atomic
    def create_new_instance(self, hostname, product):
        # generate new password
        new_password = User.objects.make_random_password(length=16)
        # generate the db password
        db_password = User.objects.make_random_password(length=16)

        # find new available identifier
        # TODO: get instance_id_start and instance_id_end from configuration settings
        # TODO: get startport from configuration settings
        instance_id_start = 10000
        instance_id_end = 20000
        startport = 7000
        new_id = random.randrange(instance_id_start, instance_id_end)
        while SaasInstance.objects.filter(identifier=str(new_id), product = product).exists():
          new_id = random.randrange(instance_id_start, instance_id_end)

        # find new available port on that host
        new_port = -1
        if SaasInstance.objects.filter(hostname=hostname, product = product).exists():
          with connection.cursor() as cursor:
            sql = """SELECT MAX(port) FROM `saas_instance` WHERE hostname = %s AND product_id = %s"""
            cursor.execute(sql, [hostname,product.id,])
            port_result = cursor.fetchone()
            if port_result:
              new_port = port_result[0] + 1
        if new_port < startport:
          new_port = startport

        # store to database
        instance = SaasInstance.objects.create(
          identifier = str(new_id),
          hostname = hostname,
          product = product,
          port = new_port,
          initial_password = new_password,
          db_password = db_password,
          status = 'in_preparation')

        # return the result
        return True, {'new_id': new_id, 'new_password': new_password, 'db_password': db_password, 'hostname': hostname, 'port': new_port};
