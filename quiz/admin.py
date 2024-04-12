from django.contrib import admin
from .models import QuizCategory, UserCategoryAttempts, QuizQuestions, UserSubmittedAnswer
# Register your models here.




class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'level']


class UserSubmittedAnswersAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'user', 'right_answer']


class UserCategoryAttemptsAdmin(admin.ModelAdmin):
    list_display = ['category', 'user', 'attempt_time']


admin.site.register(QuizCategory)
admin.site.register(QuizQuestions, QuizQuestionAdmin)
admin.site.register(UserSubmittedAnswer, UserSubmittedAnswersAdmin)
admin.site.register(UserCategoryAttempts, UserCategoryAttemptsAdmin)
