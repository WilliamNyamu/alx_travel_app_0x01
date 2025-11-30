from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from faker import Faker

User = get_user_model()

class Command(BaseCommand):
    help = "Seeding data to the user table"
    

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write("Starting to seed data for user")
        
        for i in range(50):
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                first_name = fake.first_name(),
                last_name=fake.last_name(),
                password=fake.password()
            )
            self.stdout.write(f"Writing {i + 1} to db...")
        
