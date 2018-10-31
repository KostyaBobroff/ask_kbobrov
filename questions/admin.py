from django.contrib import admin
from questions.models import User, Tag, Question, CommentVote, QuestionVote, Comment

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(QuestionVote)
admin.site.register(Comment)
admin.site.register(CommentVote)