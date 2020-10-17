from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from mrds.forms import SiteSearchForm
from mrds.models import Site, Commodity


class SiteSearchView(FormView):
    template_name = 'mrds/site_search.html'
    form_class = SiteSearchForm
    success_url = reverse_lazy('site_search')

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

    def get_search_results(self, cleaned_data):
        filter_kwargs = self.get_filter_kwargs(cleaned_data)
        site_qs = Site.objects.filter(**filter_kwargs).select_related(
            'state', 'county', 'commodity_1', 'commodity_2', 'commodity_3')

        return site_qs.order_by('site_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commodity_names = Commodity.objects.exclude(name__contains=',').exclude(name='').values_list('name', flat=True)
        commodity_choices = [{'text': commodity} for commodity in commodity_names]
        context['commodity_choices'] = commodity_choices
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        site_qs = self.get_search_results(cleaned_data)

        site_data = [
            x.to_search_result()
            for x in site_qs
        ]
        data = {
            'site_data': site_data,
            'site_count': site_qs.count()
        }

        return JsonResponse(data, safe=False)

    def form_invalid(self, form):
        resp = super().form_invalid(form)
        return resp


class CommodityAjaxView(FormView):

    def get(self, request, *args, **kwargs):
        # data = [{"text": "first", "tiClasses": [ "ti-valid"]}, {"text": "wat", "tiClasses": ["ti-valid"]}]
        data = [
            {'text': 'Gold'},
            {'text': 'Silver'}
        ]
        return JsonResponse(data=data, safe=False)
