from django.contrib import admin
from questions.models import User, Tag, Question

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Question)