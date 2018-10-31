from django.db import models
from django.contrib.auth.models import UserManager


class QuestionManager(models.Manager):

    def get_hot(self):
      return  self.filter(is_active=True).order_by('-rating').prefetch_related()

    def get_by_tag(self, tag_name):
        return self.filter(is_active=True).filter(tags__title=tag_name).prefetch_related()

