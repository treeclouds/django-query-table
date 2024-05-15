import django_tables2 as tables
import django_filters

class SQLResultsTable(tables.Table):
    class Meta:
        template_name = 'django_tables2/bootstrap.html'
