from django.contrib import admin

from .models import Answer, Question, Quiz

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Answer)
admin.site.register(Question)
