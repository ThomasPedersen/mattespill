from mattespill.main.models import Question, Room, Turn, Result, UserProfile, Hint

from django.contrib import admin

class QuestionAdmin(admin.ModelAdmin):
	'''
	Django class for deciding what fields to register in the admin panel
	'''
	fields = ['question', 'real_answer', 'room', 'author', 'points']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Room)
admin.site.register(UserProfile)
admin.site.register(Hint)

