from django.contrib import admin

from .models import Comment


def date(obj):
    ''' Used by list_display to properly format date. '''
    return obj.date.strftime('%-I:%M %P %B %d, %Y')  # 4:36 pm April 27, 2020


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ['user', 'ticket', date]
    list_filter = ['user', 'date']
