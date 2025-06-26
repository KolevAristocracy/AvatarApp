from django.shortcuts import render
from django.views.generic import TemplateView

from attributes.models import Attribute
from quiz_system.models import UserAnswer


# Create your views here.


def dashboard_view(request):
    attributes = Attribute.objects.all()  # Getting all attributes (skills)
    user_answers = UserAnswer.objects.filter(user=request.user)  # get answers for the user who request them

    data = {}

    for attr in attributes:
        total = sum(ua.answer.score for ua in user_answers if ua.answer.attribute == attr)
        data[attr.name] = total

    return render(request, 'dashboard/dashboard.html', {'data': data})
