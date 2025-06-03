from django.core.management.base import BaseCommand
from faker import Faker
from mainapp.models import User, Pet, Post, Comment, Like, Message
import random
from django.utils import timezone
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Seed database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = []
        self.stdout.write('Creating users and pets...')

        for _ in range(1000):
            while True:
                username = f"{fake.user_name()}{random.randint(1, 10000)}"
                if not User.objects.filter(username=username).exists():
                    try:
                        user = User.objects.create_user(
                            username=username,
                            email=fake.email(),
                            password='password123',
                            city=fake.city(),
                            user_type=random.choice(['PetOwner', 'Veterinarian'])
                        )
                        users.append(user)
                        break
                    except IntegrityError:
                        
                        continue

        for user in users:
            for _ in range(random.randint(1, 3)):
                Pet.objects.create(
                    name=fake.first_name(),
                    species=random.choice(['Dog', 'Cat', 'Rabbit']),
                    breed=fake.word(),
                    age=random.randint(1, 15),
                    gender=random.choice(['Male', 'Female']),
                    owner=user,
                    registration_date=fake.date_this_decade()
                )

        self.stdout.write('Creating posts...')
        posts = []
        for user in users:
            for _ in range(random.randint(1, 5)):
                post = Post.objects.create(
                    content=fake.text(max_nb_chars=200),
                    user=user,
                    created_at=fake.date_time_this_year(tzinfo=timezone.get_current_timezone())
                )
                posts.append(post)

        self.stdout.write('Creating comments...')
        for post in posts:
            for _ in range(random.randint(0, 5)):
                commenter = random.choice(users)
                Comment.objects.create(
                    content=fake.sentence(),
                    user=commenter,
                    post=post,
                    created_at=fake.date_time_this_year(tzinfo=timezone.get_current_timezone())
                )

        self.stdout.write('Creating likes...')
        for post in posts:
            likers = random.sample(users, k=random.randint(0, 10))
            for liker in likers:
                Like.objects.get_or_create(
                    user=liker,
                    post=post,
                    liked_at=fake.date_time_this_year(tzinfo=timezone.get_current_timezone())
                )

        self.stdout.write('Creating messages...')
        for _ in range(1000):
            sender = random.choice(users)
            receiver = random.choice(users)
            if sender != receiver:
                Message.objects.create(
                    sender=sender,
                    receiver=receiver,
                    content=fake.sentence(),
                    sent_at=fake.date_time_this_year(tzinfo=timezone.get_current_timezone())
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
