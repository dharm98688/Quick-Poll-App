from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("submit-answer/<int:cat_id>//<int:question_id>/", views.submit_answer, name="submit-answer"),
    path("register", views.register, name="register"),
    path("all-categories", views.all_category, name="all_category"),
    path("category-question/<int:cat_id>/", views.category_questions, name="categoryquestions"),
    path("attempts/<int:cat_id>/", views.attempts, name="attempts"),
    path("result", views.result, name='result')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
