from django.contrib.admin import FieldListFilter
from django.utils.translation import gettext_lazy as _

class DateRangeFilter(FieldListFilter):
    title = _('Date range')
    parameter_name = 'date_range'

    def expected_parameters(self):
        return [f'{self.parameter_name}__gte', f'{self.parameter_name}__lte']

    def lookups(self, request, model_admin):
        return (
            ('custom', _('Custom')),
        )

    def queryset(self, request, queryset):
        from_date = request.GET.get(f'{self.parameter_name}__gte')
        to_date = request.GET.get(f'{self.parameter_name}__lte')

        if from_date:
            try:
                queryset = queryset.filter(date__gte=from_date)
            except ValueError:
                pass  # Ignore invalid values

        if to_date:
            try:
                queryset = queryset.filter(date__lte=to_date)
            except ValueError:
                pass  # Ignore invalid values

        return queryset

    def choices(self, changelist):
        selected_value = changelist.get_filters_params().get(self.parameter_name)
        yield {
            'selected': not selected_value,
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
            'display': _('All'),
        }
        yield {
            'selected': selected_value == 'custom',
            'query_string': changelist.get_query_string({self.parameter_name: 'custom'}),
            'display': _('Custom range'),
        }

