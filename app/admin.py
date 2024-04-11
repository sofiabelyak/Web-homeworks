from django.contrib import admin

from app import models

# Register your models here.

admin.site.register(models.Answers)
admin.site.register(models.LikeQuestion)
admin.site.register(models.LikeAnswer)
admin.site.register(models.Question)
admin.site.register(models.Tag)
admin.site.register(models.Profile)
