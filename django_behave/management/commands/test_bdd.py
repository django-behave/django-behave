from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<app  ...>'
    help = 'Runs the BDD tests on the specified apps'

    def handle(self, *args, **options):
        for app in args:
            self.stdout.write('TODO: Run BDD test on app "%s"\n' % app)

# eof            
