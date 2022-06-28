from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from account.models import Account


class Command(BaseCommand):
    help = "Create missing account for user"

    def handle(self, *args, **options):
        users = User.objects.filter(account__id__isnull=True)
        for u in users:
            Account.create(user=u)

