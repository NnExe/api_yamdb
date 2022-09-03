import django_filters as filter

from categories.models import Title


class TitleFilter(filter.FilterSet):
    genre = filter.CharFilter(field_name='genre__slug')
    category = filter.CharFilter(field_name='category__slug')
    year = filter.NumberFilter(field_name='year')
    name = filter.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']
