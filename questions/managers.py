from django.db import models
from django.contrib.auth.models import UserManager
from questions.models import *

class QuestionManager(models.Manager):

    def get_hot(self):
      return  self.filter(is_active=True).order_by('-rating').prefetch_related()

    def get_by_tag(self, tag_name):
        return self.filter(is_active=True).filter(tags__title=tag_name).prefetch_related()

    def get_new(self):
        return self.all().prefetch_related()

    def set_like(self, number_question, user, is_like):
        try:
            vote = self.get(pk=number_question).questionvote_set.get(author=user)
            if vote.is_like is not is_like:
                vote.is_like = is_like
        except vote.DoesNotExist:
            vote = QuestionVote.objects.create(author=user, is_like=is_like, question=self.get(pk=number_question))
        vote.save()


