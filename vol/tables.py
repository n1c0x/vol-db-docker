import django_tables2 as tables
from .models import Vol

class VolTable(tables.Table):
    class Meta:
        model = Vol
        template_name = 'django_tables2/bootstrap.html'