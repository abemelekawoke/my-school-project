from import_export.widgets import ForeignKeyWidget
from setups.models import Weight


class WeightWidget(ForeignKeyWidget):
    def get_queryset(self, value, row, **kwargs):
        raw = (row.get("weight") or "").strip()
        assessment_name = raw.split(" (")[0].strip()
        return Weight.objects.filter(
            assessment_formula__subject__name=row["subject"],
            assessment_formula__grade_level__code=row["grade"],
            assessment_formula__academic_year__year=row["academic_year"],
            name__name=assessment_name,
        )

    def clean(self, value, row=None, **kwargs):
        qs = self.get_queryset(value, row, **kwargs)
        count = qs.count()
        if count == 0:
            raise ValueError(
                f"No Weight for subject={row.get('subject')!r}, "
                f"grade={row.get('grade')!r}, "
                f"academic_year={row.get('academic_year')!r}, "
                f"weight={row.get('weight')!r}."
            )
        if count > 1:
            raise ValueError(
                f"Ambiguous Weight for subject={row.get('subject')!r}, "
                f"grade={row.get('grade')!r}, "
                f"academic_year={row.get('academic_year')!r}, "
                f"weight={row.get('weight')!r}: {count} matches."
            )
        return qs.first()