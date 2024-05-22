from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count



class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        primary_key=True,
    )
    avatar = models.ImageField(null= True, default='/static/img/catty.jpg',blank=True)


    def __str__(self):
        return str(self.user.get_username())


class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
class QuestionManager(models.Manager):
    def get_questions_by_tag(self, tag_name):
        return self.filter(tag__name=tag_name)

    def get_last_questions(self):
        return self.order_by("-created_at")
    
    def get_hot_questions(self):
        return self.annotate(num_likequestion=Count('likequestion')).order_by('-num_likequestion')
    
class Question(models.Model):
    text = models.TextField('Question Text')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def __str__(self):
        return str(f'Question: {self.text}')
    
class AnswersManager(models.Manager):
    def get_answers(self, question_id):
        return self.filter(question__pk = question_id)
    
class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField('Answer Text')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    objects = AnswersManager()

    def __str__(self):
        return str(f'Answer: {self.text}')



class LikeQuestion(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        unique_together = ("profile", "question")

    def __str__(self):
        return str(self.question)
    

class LikeAnswer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        unique_together = ("profile", "answer")

    def __str__(self):
        return str(self.answer)
    
