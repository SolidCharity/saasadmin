from django.core.management.base import BaseCommand, CommandError
from apps.api.logic.contracts import LogicContracts
from apps.api.logic.instances import LogicInstances

class Command(BaseCommand):
    help = 'Runs the cronjob for disabling and deleting instances'

    def handle(self, *args, **options):
        LogicContracts().update_dates_of_contracts()
        LogicInstances().deactivate_expired_instances()
        LogicInstances().mark_deactivated_instances_for_deletion()
