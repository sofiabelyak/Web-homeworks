from sqlite3 import IntegrityError
from django.core.management.base import BaseCommand
from random import choice
from app.models import Profile, Question, Answers, LikeQuestion, LikeAnswer

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        
        profiles = list(Profile.objects.all())
        answers = list(Answers.objects.all())

        for _ in range(ratio * 200 + 1):
            profile = choice(profiles)
            answer = choice(answers)

            try:
                LikeAnswer.objects.get_or_create(profile=profile, answer=answer)
            except IntegrityError:
                pass

