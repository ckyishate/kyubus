import django_filters
from django_filters import CharFilter

from . models import *

class routeFilter(django_filters.FilterSet):
    source = CharFilter(field_name = 'source', lookup_expr ='icontains')
    
    destination = CharFilter(field_name = 'destination', lookup_expr ='icontains')
    class Meta:
        model = Routes
        fields =  "__all__"
        exclude = ['date', 'departure', 'fare', 'bus', 'bSeats']

