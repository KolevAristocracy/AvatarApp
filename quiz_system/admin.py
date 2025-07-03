from django.contrib import admin

from quiz_system.models import Question, Answer


# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    ...


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    ...

