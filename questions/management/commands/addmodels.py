from django.core.management.base import  BaseCommand, CommandError
from faker import Faker
import random
from questions.models import *

COUNT_USERS = 10001
COUNT_TAGS = 10001
COUNT_QUESTIONS = 100001
COUNT_COMMENTS = 1000001
COUNT_LIKES = 2000001


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = self.add_users()
        tags = self.add_tags()
        questions = self.add_questions(users, tags)
        comments = self.add_comments(users, questions)
        self.add_votes_for_questions_and_comments(questions, comments, users)
        self.stdout.write(self.style.SUCCESS('Successfully add '))

    def add_users(self):
        users_list = []
        faker = Faker()
        for i in range(COUNT_USERS):
            user = User.objects.create_user(username="User_{}".format(i), password='askme{}'.format(i))
            user.first_name = faker.first_name()
            user.last_name = faker.last_name()
            user.email = faker.email()
            user.save()
            users_list.append(user)

        return users_list

    def add_tags(self):
        tags_list = []
        faker = Faker()
        for _ in range(COUNT_TAGS):
            tag = Tag.objects.create(title=faker.word())
            tag.save()
            tags_list.append(tag)

        return tags_list

    def add_questions(self, users, tags):
        faker = Faker()
        questions_list = []
        for _ in range(COUNT_QUESTIONS):
            tags_for_questions = []
            for _ in range(random.randint(1,5)):
                tag = random.choice(tags)
                if tag not in tags_for_questions:
                    tags_for_questions.append(tag)
            user = random.choice(users)

            question = Question.objects.create(title=faker.sentence()[:random.randint(15,50)],
                                               text=faker.text(), author=user)

            question.tags.add(*tags_for_questions)
            question.save()
            questions_list.append(question)

        return questions_list

    def add_comments(self, users, questions):
        faker = Faker()
        comments_list = []
        for _ in range(COUNT_COMMENTS):
            question = random.choice(questions)
            user = random.choice(users)
            comment = Comment(author=user, question=question, text=faker.text())
            comment.save()
            comments_list.append(comment)
        return comments_list


    def add_votes_for_questions_and_comments(self, questions, comments, users):
        for _ in range(int(COUNT_LIKES/2)):
            is_like = random.choice([True, False])
            user = random.choice(users)
            question = random.choice(questions)
            question.set_like(is_like=is_like, user=user)

        for _ in range(int(COUNT_LIKES/2)):
            is_like = random.choice([True, False])
            user = random.choice(users)
            comment = random.choice(comments)
            comment.set_like(is_like=is_like, user=user)

        # for question in questions:
        #     for _ in range(random.randint(3,6)):
        #         is_like = random.choice([True, False])
        #         user = random.choice(users)
        #         question.set_like(is_like=is_like, user=user)
        #
        # for comment in comments:
        #     for _ in range(random.randint(3,6)):
        #         is_like = random.choice([True, False])
        #         user = random.choice(users)
        #         comment.set_like(is_like=is_like, user=user)
        #
