from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from random import choice, randint, sample
from app.models import Profile, Tag, Question, Answers, Like

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        users = []
        for i in range(ratio + 1):
            username = f'User{i}'
            user = User(username=username, password='password')
            users.append(user)

        User.objects.bulk_create(users)
        profiles = [Profile(user=user) for user in users]
        Profile.objects.bulk_create(profiles)

        tags = [Tag(name=f'Tag{i}') for i in range(ratio)]
        Tag.objects.bulk_create(tags)

        questions = []
        for i in range(ratio * 10 + 1):
            text = f'Question {i}'
            profile = choice(profiles)
            question = Question(text=text, profile=profile)
            questions.append(question)

        Question.objects.bulk_create(questions)
        question_tag_mappings = []
        for question in questions:
            tags_to_add = sample(tags, k=randint(1, 5))
            for tag in tags_to_add:
                question_tag_mappings.append(Question.tag.through(question_id=question.id, tag_id=tag.id))
        
        Question.tag.through.objects.bulk_create(question_tag_mappings)

        answers = []
        for i in range(ratio * 100 + 1):
            text = f'Answer {i}'
            profile = choice(profiles)
            question = choice(questions)
            answer = Answers(text=text, profile=profile, question=question)
            answers.append(answer)

        Answers.objects.bulk_create(answers)

        likes_questions = []
        for i in range(ratio * 200 + 1):
            profile = choice(profiles)
            question = choice(questions)
            likes_questions.append(Like(profile=profile, question=question))

        Like.objects.bulk_create(likes_questions)