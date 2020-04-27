from django.contrib import admin

from .models import Quiz, Question, Answer, Result


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz_id', 'text']
    list_filter = ['quiz_id']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'text', 'is_correct']
    list_filter = ['question_id']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'percent']
    list_filter = ['user', 'percent']
