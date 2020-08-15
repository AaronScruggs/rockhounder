from django.urls import reverse_lazy
from django.views.generic import FormView

from mrds.forms import SiteSearchForm


class SiteSearchView(FormView):
    template_name = 'mrds/site_search.html'
    form_class = SiteSearchForm
    success_url = reverse_lazy('site_search')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        return super().form_valid(form)



