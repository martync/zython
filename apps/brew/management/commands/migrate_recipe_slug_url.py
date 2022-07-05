from django.core.management.base import BaseCommand
from brew.models import Recipe


class Command(BaseCommand):
    def handle(self, *args, **options):
        for r in Recipe.objects.filter(slug_url__isnull=True):
            r.update_slug_url(force_update=False)
            print(r)
