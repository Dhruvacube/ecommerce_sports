"""
 It runs tailwind install and `npm install flowbite` command simultaneously
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess, os


class Command(BaseCommand):
    help = "It runs tailwind install and `npm install flowbite` command simultaneously"
    output_transaction = True

    def handle(self, *args, **options):
        print("Running `tailwind install` now :)\n")
        call_command("tailwind", "install")
        self.stdout.write(
            self.style.SUCCESS(
                "Finished running `tailwind install` \n Now running `npm install flowbite` :)"
            ))
        subprocess.run(["npm", "install", "flowbite"], cwd=(settings.BASE_DIR/os.path.join(settings.TAILWIND_APP_NAME,"static_src")), shell = True)
        self.stdout.write(self.style.SUCCESS("Finished...."))