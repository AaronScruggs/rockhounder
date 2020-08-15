from django.forms import ModelForm

from mrds.models import Site


class SiteSearchForm(ModelForm):

    class Meta:
        model = Site
        fields = ('dep_id', 'site_name')
