import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, User, Review, Comment


class Command(BaseCommand):
    help = 'Loads data from CSV files to database'

    def handle(self, *args, **kwargs):
        data_dir = os.path.join(settings.BASE_DIR, 'static', 'data')

        self.load_category(data_dir)
        self.load_genre(data_dir)
        self.load_title(data_dir)
        self.load_user(data_dir)
        self.load_review(data_dir)
        self.load_comment(data_dir)

    def load_category(self, data_dir):
        with open(
            os.path.join(data_dir, 'category.csv'), encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(self.style.SUCCESS(
            'Successfully loaded Category from CSV'
        ))

    def load_genre(self, data_dir):
        with open(os.path.join(data_dir, 'genre.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(self.style.SUCCESS(
            'Successfully loaded Genre from CSV'
        ))

    def load_title(self, data_dir):
        with open(os.path.join(data_dir, 'titles.csv'), encoding='utf-8') as f:
            for row in csv.DictReader(f):
                category_id = int(row['category'])
                category = Category.objects.get(id=category_id)
                Title.objects.get_or_create(
                    id=int(row['id']),
                    name=row['name'],
                    year=row['year'],
                    category=category
                )
        self.stdout.write(self.style.SUCCESS(
            'Successfully loaded Title from CSV'
        ))

    def load_user(self, data_dir):
        with open(os.path.join(data_dir, 'users.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
        self.stdout.write(self.style.SUCCESS(
            'Successfully loaded User from CSV'
        ))

    def load_review(self, data_dir):
        with open(os.path.join(data_dir, 'review.csv'), encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    title = Title.objects.get(id=int(row['title_id']))
                    author = User.objects.get(id=int(row['author']))
                    Review.objects.get_or_create(
                        id=int(row['id']),
                        defaults={
                            'title': title,
                            'text': row['text'],
                            'author': author,
                            'score': int(row['score']),
                            'pub_date': row['pub_date']
                        }
                    )
                except (Title.DoesNotExist, User.DoesNotExist) as e:
                    self.stdout.write(self.style.ERROR(str(e)))

        self.stdout.write(self.style.SUCCESS(
            'Successfully loaded Review from CSV'
        ))

    def load_comment(self, data_dir):
        with open(
            os.path.join(data_dir, 'comments.csv'), encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    review = Review.objects.get(id=int(row['review_id']))
                    author = User.objects.get(id=int(row['author']))
                    Comment.objects.get_or_create(
                        id=int(row['id']),
                        defaults={
                            'review': review,
                            'text': row['text'],
                            'author': author,
                            'pub_date': row['pub_date']
                        }
                    )
                except (Review.DoesNotExist, User.DoesNotExist) as e:
                    self.stdout.write(self.style.ERROR(str(e)))

        self.stdout.write(self.style.SUCCESS(
            'Successfully loaded Comment from CSV'
        ))
