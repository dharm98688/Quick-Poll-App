from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class QuizCategory(models.Model):
    title = models.CharField(max_length=100)
    details = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cats_img/')

    class Meta:
        verbose_name_plural = "Quiz Categories"

    def __str__(self):
        return self.title


class QuizQuestions(models.Model):
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    question = models.TextField()
    opt_1 = models.CharField(max_length=100)
    opt_2 = models.CharField(max_length=100)
    opt_3 = models.CharField(max_length=100)
    opt_4 = models.CharField(max_length=100)
    level = models.CharField(max_length=100, null=True)
    time_limit = models.IntegerField(null=True)
    right_opt = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Quiz Questions"  # for name change

    def __str__(self):
        return self.question


class UserSubmittedAnswer(models.Model):
    question = models.ForeignKey(QuizQuestions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    right_answer = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "User Submitted Answers"


class UserCategoryAttempts(models.Model):
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE,default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "User Attempt Category"
