from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from mrds.forms import SiteSearchForm
from mrds.models import Site


class SiteSearchView(FormView):
    template_name = 'mrds/site_search.html'
    form_class = SiteSearchForm
    success_url = reverse_lazy('site_search')
    results_limit = 50

    @staticmethod
    def get_filter_kwargs(cleaned_data):
        dep_id = cleaned_data.get('dep_id', '')
        site_name = cleaned_data.get('site_name', '')
        county = cleaned_data.get('county', '')
        state = cleaned_data.get('state', '')
        commodity_1 = cleaned_data.get('commodity_1')
        commodity_2 = cleaned_data.get('commodity_2')
        commodity_3 = cleaned_data.get('commodity_3')

        filter_kwargs = {}
        if dep_id:
            filter_kwargs['dep_id__icontains'] = dep_id

        if site_name:
            filter_kwargs['site_name__icontains'] = site_name

        if county:
            filter_kwargs['county'] = county

        if state:
            filter_kwargs['state'] = state

        if commodity_1:
            filter_kwargs['commodity_1'] = commodity_1

        if commodity_2:
            filter_kwargs['commodity_2'] = commodity_2

        if commodity_3:
            filter_kwargs['commodity_3'] = commodity_3

        return filter_kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['results_limit'] = self.results_limit

        cleaned_data = kwargs.pop('cleaned_data', {})
        if cleaned_data:
            filter_kwargs = self.get_filter_kwargs(cleaned_data)
            site_qs = Site.objects.filter(**filter_kwargs)

            results_count = site_qs.count()
            context_data['results_count'] = results_count
            context_data['site_qs'] = site_qs[:50].select_related(
                'state', 'county', 'commodity_1', 'commodity_2', 'commodity_3')

        return context_data

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        context_data = self.get_context_data(cleaned_data=cleaned_data)
        return render(self.request, context=context_data, template_name=self.template_name)



