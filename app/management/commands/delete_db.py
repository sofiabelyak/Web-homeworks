from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answers, Like

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Profile.objects.all().delete()
        User.objects.all().delete()
        Tag.objects.all().delete()
        Question.objects.all().delete()
        Answers.objects.all().delete()
        Like.objects.all().delete()
