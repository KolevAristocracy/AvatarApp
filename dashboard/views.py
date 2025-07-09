from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from accounts.models import Profile
from attributes.models import Attribute
from quiz_system.models import UserAnswer


# Create your views here.

class DashboardView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'profile'


    def get_object(self, queryset = ...):
        # Ensure I get the profile for currently logged user
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object() # get the profile object
        attributes = Attribute.objects.all() # get all attributes

        # Prepare data for the chart
        chart_data = {
            'openness': profile.openness,
            'conscientiousness': profile.conscientiousness,
            'extraversion': profile.extraversion,
            'agreeableness': profile.agreeableness,
            'neuroticism': profile.neuroticism,
        }
        attr_level = {}

        # convert dict keys and values to lists for JavaScript
        context['data_labels'] = list(chart_data.keys())
        context['data_values'] = list(chart_data.values())

        context['data'] = chart_data
        context['total_points'] = sum(chart_data.values())
        context['attributes'] = attributes
        context['attr_level'] = attr_level
        return context

# @login_required
# def dashboard_view(request):
#     # get answers for the user who request them
#     user_answers = UserAnswer.objects.filter(user=request.user).select_related('question__attribute', 'answer')
#
#     context = {}
#
#     for ua in user_answers:
#         attr = ua.question.attribute.name
#         context[attr] = context.get(attr, 0) + ua.answer.score
#
#
#     context['total_points'] = sum(ua.answer.score for ua in user_answers)
#     return render(request, 'dashboard/dashboard.html', {'data': context})
