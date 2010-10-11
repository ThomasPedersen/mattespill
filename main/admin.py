from mattespill.main.models import Question, Room, Turn, Result

from django.contrib import admin

class QuestionAdmin(admin.ModelAdmin):
    fields = ['question', 'real_answer', 'room', 'author', 'points']
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result)
admin.site.register(Room)
admin.site.register(Turn)

