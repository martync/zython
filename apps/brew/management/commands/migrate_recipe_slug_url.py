from django.db import connection
from django.db.utils import OperationalError
from django.core.management.base import NoArgsCommand
from brew.models import Recipe


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        """
        I know django 1.8 can take care of migrations way way better than that.
        But I will have to migrate from .7 to .8 and I'm not doing this now.
        """
        cursor = connection.cursor()
        try:
            cursor.execute("ALTER TABLE `brew_recipe` ADD `slug_url` varchar(50);")
        except OperationalError:
            print("Problem while adding the column")

        for r in Recipe.objects.all():
            r.update_slug_url()
            print(r.id, ",", r.slug_url)

        cursor.execute("ALTER TABLE `brew_recipe` change `slug_url` `slug_url` varchar(50) NOT NULL;")
