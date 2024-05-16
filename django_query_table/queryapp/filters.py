import django_filters

def create_filter_class(column_names):
    filter_fields = {column: django_filters.CharFilter(lookup_expr='icontains') for column in column_names}

    class DynamicFilter(django_filters.FilterSet):
        class Meta:
            fields = filter_fields
    
    return DynamicFilter
