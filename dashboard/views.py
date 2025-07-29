from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from accounts.models import Profile
from attributes.models import Attribute


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
        attribute_descriptions = {attr.name.lower(): attr.description for attr in attributes}

        # Prepare data for the chart
        chart_data = {
            'openness': profile.openness,
            'conscientiousness': profile.conscientiousness,
            'extraversion': profile.extraversion,
            'agreeableness': profile.agreeableness,
            'neuroticism': profile.neuroticism,
        }
        result = []
        for name, score in chart_data.items():
            result.append({
                'name': name,
                'score': score,
                'description': attribute_descriptions.get(name.lower(), 'No description available')
                })

        # convert dict keys and values to lists for JavaScript
        context['data_labels'] = list(chart_data.keys())
        context['data_values'] = list(chart_data.values())

        context['result'] = result
        context['attribute_descriptions'] = attribute_descriptions
        return context
