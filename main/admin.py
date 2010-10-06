from mattespill.main.models import Question

from django.contrib import admin

class QuestionAdmin(admin.ModelAdmin):
    fields = ['question', 'real_answer', 'room']
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Result)
#admin.site.register(Room)
#admin.site.register(Answer)

