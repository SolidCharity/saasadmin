from apps.core.models import SaasInstance
from django.contrib.auth.models import User
import random

class LogicInstances:
    def create_new_instance(self, hostname):
        # generate new password
        new_password = User.objects.make_random_password(length=16)

        # find new available identifier
        # TODO: get instance_id_start and instance_id_end from configuration settings
        instance_id_start = 10000
        instance_id_end = 20000
        new_id = random.randrange(instance_id_start, instance_id_end)

        while SaasInstance.objects.filter(identifier=str(new_id)).exists():
          new_id = random.randrange(instance_id_start, instance_id_end)

        # store to database
        instance = SaasInstance.objects.create(
          identifier = str(new_id),
          hostname = hostname,
          initial_password = new_password,
          status = 'in_preparation')

        # return the result
        return True, {'new_id': new_id, 'new_password': new_password, 'hostname': hostname};
