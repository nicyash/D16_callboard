from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Ad


class AdFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='ad_time',
        lookup_expr='gte',
        widget=DateTimeInput(
            format='%y-%m-%dT',
            attrs={'type': 'datetime-local'},
        ))


    class Meta:
        model = Ad
        fields = {'title': ['icontains'],
                  'category__category': ['icontains'],
                  }
