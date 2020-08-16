from django.forms import ModelForm

from mrds.models import Site


class SiteSearchForm(ModelForm):
    str_fields = ('dep_id', 'site_name')

    def clean(self):
        cleaned_data = super().clean()

        for str_field in self.str_fields:
            cleaned_data[str_field] = cleaned_data[str_field].lower()

        return cleaned_data

    class Meta:
        model = Site
        fields = ('dep_id', 'site_name', 'county', 'state', 'commodity_1', 'commodity_2', 'commodity_3')
        labels = {
            'commodity_1': 'Primary Commodity',
            'commodity_2': 'Secondary Commodity',
            'commodity_3': 'Tertiary Commodity',
        }
