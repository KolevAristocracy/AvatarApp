from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from accounts.forms import ContactForm


# Create your views here.

class IndexView(TemplateView):
    template_name = 'common/index.html'


class ContactFormView(FormView):
    template_name = 'common/contact-page.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact-page')

    def form_valid(self, form):
        messages.success(self.request, "Thank you for you message! We'll get back to you soon.")
        return super().form_valid(form)
