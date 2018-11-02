from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from questions.managers import QuestionManager

class User(AbstractUser):
    upload = models.ImageField(blank=True,upload_to='uploads/%Y/%m/%d')

class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"Заголовок ярлыка")

    def __str__(self):
        return self.title


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(verbose_name=u"Полное описание вопроса")
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")
    tags = models.ManyToManyField(Tag, blank=True, related_name="questions")
    rating = models.IntegerField(default=0)
    objects = QuestionManager()

    def comments_count(self):
       return self.comment_set.count()

    # def likes_and_dislikes_count(self):
    #     dislike_count = self.questionvote_set.filter(is_like = False).count()
    #     like_count = self.questionvote_set.filter(is_like=True).count()
    #     return like_count - dislike_count

    def set_like(self,  user, is_like):
        try:
            vote = self.questionvote_set.get(author=user)
            if vote.is_like is not is_like:
                vote.is_like = is_like
        except QuestionVote.DoesNotExist:
            vote = QuestionVote.objects.create(author=user, is_like=is_like, question=self)
        self.rating += 1 if vote.is_like else -1
        vote.save()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    create_data = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания комментария")
    correct = models.BooleanField(default=False)
    text = models.TextField(blank=True ,verbose_name=u"Комментарий")
    rating = models.IntegerField(default=0)

    # def likes_and_dislikes_count(self):
    #     dislike_count = self.commentvote_set.filter(is_like=False).count()
    #     like_count = self.commentvote_set.filter(is_like=True).count()
    #     return like_count - dislike_count

    def set_like(self,  user, is_like):
        try:
            vote = self.commentvote_set.get(author=user)
            if vote.is_like is not is_like:
                vote.is_like = is_like
        except CommentVote.DoesNotExist:
            vote = CommentVote.objects.create(author=user, is_like=is_like, comment=self)
        self.rating += 1 if vote.is_like else -1
        vote.save()
        self.save()

    def __str__(self):
        return "{questions} {user}".format(questions=self.question, user=self.author)



class CommentVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)




class QuestionVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

