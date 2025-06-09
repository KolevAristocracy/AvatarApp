from django.shortcuts import render, redirect

from quiz_system.models import Question


# Create your views here.

def start_quiz(request):
    questions = Question.objects.prefetch_related('answer_set').all()

    context = {
        'questions': questions,
    }

    if request.method == "POST":
        request.session['answers'] = request.POST
        return redirect('dashboard/result.html')

    return render(request, 'quiz/quiz.html', context)