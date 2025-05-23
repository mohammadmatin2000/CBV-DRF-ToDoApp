from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User,Profile
from app.models import ToDoApp

#=======================================================================================================================

class Command(BaseCommand):
    help = "Creates and inserts test users into the database"
    def __init__(self):
        super(Command, self).__init__()
        self.fake = Faker()

    def handle(self, *args, **options):
        user=User.objects.create_user(email=self.fake.email(),password='m1387m2008m')
        profile=Profile.objects.create(user=user)
        profile.first_name=self.fake.first_name()
        profile.last_name=self.fake.last_name()
        profile.description=self.fake.paragraph(nb_sentences=1)
        profile.save()
        self.stdout.write(self.style.SUCCESS('Data inserted successfully!'))

        for _ in range(5):
            ToDoApp.objects.create(
                author=user,
                content=self.fake.paragraph(nb_sentences=1),
            )
#=======================================================================================================================