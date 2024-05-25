from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Ad, UserResponse


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
        fields = {'title': ['icontains']}


class UserResponseFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='response_time',
        lookup_expr='gte',
        widget=DateTimeInput(
            format='%y-%m-%dT',
            attrs={'type': 'datetime-local'},
        ))

    class Meta:
        model = UserResponse
        fields = {'ad'}

    def __init__(self, *args, **kwargs):
        super(UserResponseFilter, self).__init__(*args, **kwargs)
        self.filters['ad'].queryset = Ad.objects.filter(author__id=kwargs['request'])
