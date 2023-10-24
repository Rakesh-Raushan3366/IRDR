import django_filters
from django_filters import ChoiceFilter
from django_filters import DateFromToRangeFilter
from django_filters.widgets import *

from .models import *



class EventFilter(django_filters.FilterSet):
    date_of_sample_collection = DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    sample_source = ChoiceFilter(choices=source_sel)

    # date_of_testing = DateFromToRangeFilter(widget=DateInput(attrs={'placeholder': 'epicker'}))
    class Meta:
        model = Testing
        fields = ['date_of_sample_collection']
        widgets = {

            'date_of_sample_collection': DateInput(attrs={'class': 'datepicker'}),

        }

        exclude = []
