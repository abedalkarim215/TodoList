import django_filters
from .models import *
from django_filters import DateFilter,CharFilter

class Todo_Filter(django_filters.FilterSet) :
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    title = CharFilter(field_name='title', lookup_expr='icontains')
    description = CharFilter(field_name='description', lookup_expr='icontains')
    class Meta :
        model = Todo
        fields = ['title','description','is_important']
