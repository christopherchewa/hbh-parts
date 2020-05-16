from .models import PropertyEntry
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = PropertyEntry
        fields = ['property_type', 'price']

