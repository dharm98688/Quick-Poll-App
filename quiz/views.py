from django.shortcuts import render, HttpResponse, redirect
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from datetime import timedelta


# Create your views here.


def home(request):
    return render(request, "home.html")


def register(request):
    msg = None
    form = forms.RegisterUser
    if request.method == 'POST':
        form = forms.RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Data has been added'
    return render(request, "registration/register.html", {'form': form, 'msg': msg})


def all_category(request):
    catData = models.QuizCategory.objects.all()
    return render(request, 'all-category.html', {'data': catData})


@login_required()
def category_questions(request, cat_id):
    category = models.QuizCategory.objects.get(id=cat_id)
    question = models.QuizQuestions.objects.filter(category=category).order_by('id').first()
    # check current user then insert row

    lastAttempt = None
    futureTime = None
    hoursLimit = 24
    countAttempt = models.UserCategoryAttempts.objects.filter(user=request.user, category=category).count()
    # if no attempts then insert row

    if countAttempt == 0:
        models.UserCategoryAttempts.objects.create(user=request.user, category=category)
    else:
        lastAttempt = models.UserCategoryAttempts.objects.filter(user=request.user, category=category).order_by(
            '-id').first()
        futureTime = lastAttempt.attempt_time + timedelta(hours=hoursLimit)

        if lastAttempt and lastAttempt.attempt_time < futureTime:
            # insert another attempt
            return render(request, 'attempt-limit.html')
        else:
            models.UserCategoryAttempts.objects.create(user=request.user, category=category)

    return render(request, 'category-questions.html',
                  {'question': question, 'category': category, 'lastattempt': futureTime})


def submit_answer(request, cat_id, question_id):
    if request.method == 'POST':
        category = models.QuizCategory.objects.get(id=cat_id)
        question = models.QuizQuestions.objects.filter(category=category, id__gt=question_id).exclude(id=question_id). \
            order_by('id').first()
        if 'skip' in request.POST:
            if question:
                quest = models.QuizQuestions.objects.get(id=question_id)
                user = request.user
                answer = "Not Submitted"
                models.UserSubmittedAnswer.objects.create(user=user, question=quest, right_answer=answer)
                return render(request, 'category-questions.html', {'question': question, 'category': category})
        else:
            quest = models.QuizQuestions.objects.get(id=question_id)
            user = request.user
            answer = request.POST['answer']
            models.UserSubmittedAnswer.objects.create(user=user, question=quest, right_answer=answer)

        if question:
            return render(request, 'category-questions.html', {'question': question, 'category': category})
        else:
            result = models.UserSubmittedAnswer.objects.filter(user=request.user)
            skipped = models.UserSubmittedAnswer.objects.filter(user=request.user, right_answer='Not Submitted').count()
            attempted = models.UserSubmittedAnswer.objects.filter(user=request.user).exclude(
                right_answer='Not Submitted').count()
            rightAns = 0
            percentage = 0
            for row in result:
                if row.question.right_opt == row.right_answer:
                    rightAns += 1
            percentage = (rightAns * 100) / result.count()
            return render(request, 'result.html',
                          {'result': result, 'totalskipped': skipped, 'total_attempt': attempted, 'rightAns': rightAns,
                           'percentage': percentage})
    else:
        return HttpResponse("Method not Allowed")


@login_required()
def attempts(request, cat_id):
    category = models.QuizCategory.objects.get(id=cat_id)
    return render(request, 'attempt-limit.html', {'category': category})


@login_required()
def result(request):
    result = models.UserSubmittedAnswer.objects.filter(user=request.user)
    skipped = models.UserSubmittedAnswer.objects.filter(user=request.user, right_answer='Not Submitted').count()
    attempted = models.UserSubmittedAnswer.objects.filter(user=request.user).exclude(
        right_answer='Not Submitted').count()
    rightAns = 0
    percentage = 0
    for row in result:
        if row.question.right_opt == row.right_answer:
            rightAns += 1
    percentage = (rightAns * 100) / result.count()
    return render(request, 'result.html',
                  {'result': result, 'totalskipped': skipped, 'total_attempt': attempted, 'rightAns': rightAns,
                   'percentage': percentage})