from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = User.objects.filter(recipe__id__isnull=True)\
            .exclude(is_staff=True)\
            .exclude(id=settings.ANONYMOUS_USER_ID)
        users.delete()
