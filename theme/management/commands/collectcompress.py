"""
 Command for running collectstatic and compress command simultaneously
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "It runs collectstatic and compress command simultaneously"
    output_transaction = True

    def handle(self, *args, **options):
        print("Running `collectstatic` now :)\n")
        call_command("collectstatic", "--noinput")
        self.stdout.write(
            self.style.SUCCESS(
                "Finished running `collectstatic` \n Now running `compress` :)"
            ))
        call_command("compress", "--force")
        self.stdout.write(self.style.SUCCESS("Finished...."))