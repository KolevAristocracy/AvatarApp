from django.contrib import admin

from quiz_system.models import Question, Answer, UserAnswer, Feedback


# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'attribute']
    search_fields = ['text', 'attribute__name']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'score']
    list_filter = ['score']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['answer', 'question' , 'user' ,'submitted_at']
    list_filter = ['answer', 'question', 'user', 'submitted_at']
    ordering = ['-submitted_at', 'user','question']
    search_fields = ['user__username', 'answer__text', 'question__text']
    readonly_fields = ['user', 'question', 'answer', 'submitted_at']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['message', 'user_id', 'user']
    readonly_fields = ['message', 'user_id', 'user']

