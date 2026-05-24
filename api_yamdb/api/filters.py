from django_filters import rest_framework as filters
from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """
    Фильтрация произведения по жанру, категории, году и названию.
    """

    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='iexact'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = filters.NumberFilter(
        field_name='year'
    )

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')
