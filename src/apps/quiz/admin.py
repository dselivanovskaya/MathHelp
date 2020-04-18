from django.contrib import admin

from .models import Quiz, Answer, Question

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Answer)
admin.site.register(Question)