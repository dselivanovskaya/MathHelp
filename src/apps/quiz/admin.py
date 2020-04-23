from django.contrib import admin

from .models import Quiz, Question, Answer, Result


models = (Quiz, Question, Answer, Result)
for model in models:
    admin.site.register(model)
