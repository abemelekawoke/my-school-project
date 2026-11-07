# yourproject/admin_site.py
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count, Q
from django.template.response import TemplateResponse


class CustomAdminSite(AdminSite):
    site_header = "Custom Admin"
    site_title = "Custom Admin Portal"
    index_title = "Dashboard"

    # -------- ordering of the app list --------
    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request, app_label)
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())
        for app in app_list:
            app["models"].sort(key=lambda x: x["name"])
        return app_list

    # -------- dashboard index --------
    def index(self, request, extra_context=None):
        app_list = self.get_app_list(request)
        total_models = sum(len(app["models"]) for app in app_list)

        context = {
            **self.each_context(request),
            "title": self.index_title,
            "app_list": app_list,
            "total_models": total_models,
            **(extra_context or {}),
            **self._build_dashboard_context(request),
        }
        return TemplateResponse(request, "admin/index.html", context)

    # -------- dashboard data --------
    def _build_dashboard_context(self, request):
        # lazy imports to avoid AppRegistryNotReady
        from student.models import StudentProfile
        from humanresource.models import StaffProfile

        ctx = {}

        # ---------- students ----------
        students = StudentProfile.objects.all()
        student_count = students.count()
        male_count = students.filter(Gender="Male").count()
        female_count = students.filter(Gender="Female").count()
        male_percent = round(male_count * 100 / student_count, 1) if student_count else 0
        female_percent = round(female_count * 100 / student_count, 1) if student_count else 0

        ctx.update({
            "student_count": student_count,
            "male_count": male_count,
            "female_count": female_count,
            "male_percent": male_percent,
            "female_percent": female_percent,
            "genders": {"Male": "ወንድ", "Female": "ሴት"},
        })

        # gender by grade (for chart)
        grade_rows = (
            students.values("New_grade")          # NOTE: FK field is New_grade
                    .annotate(
                        males=Count("id", filter=Q(Gender="Male")),
                        females=Count("id", filter=Q(Gender="Female")),
                    )
                    .order_by("New_grade")
        )
        ctx.update({
            "grade_chart_labels": [str(r["New_grade"]) for r in grade_rows],
            "grade_male_data": [r["males"] for r in grade_rows],
            "grade_female_data": [r["females"] for r in grade_rows],
        })

        # pivot grid: school × gender
        pivot_rows = (
            students.values("school")
                    .annotate(
                        males=Count("id", filter=Q(Gender="Male")),
                        females=Count("id", filter=Q(Gender="Female")),
                    )
                    .order_by("school")
        )
        ctx["pivot_display"] = [
            {
                "school_label": r["school"] or "—",
                "gender_counts": {"Male": r["males"], "Female": r["females"]},
                "total": r["males"] + r["females"],
            }
            for r in pivot_rows
        ]

        # ---------- employees ----------
        # employee_status is a CharField with choices, so filter by value 'active'
        employees = StaffProfile.objects.filter(employee_status="active")
        employee_count = employees.count()
        emp_m = employees.filter(gender="M").count()
        emp_f = employees.filter(gender="F").count()
        ctx.update({
            "employee_count": employee_count,
            "male_count_e": emp_m,
            "female_count_e": emp_f,
            "male_percent_e": round(emp_m * 100 / employee_count, 1) if employee_count else 0,
            "female_percent_e": round(emp_f * 100 / employee_count, 1) if employee_count else 0,
        })

        # separated / inactive — anything that is not 'active'
        separated = StaffProfile.objects.exclude(employee_status="active")
        sep_count = separated.count()
        sep_m = separated.filter(gender="M").count()
        sep_f = separated.filter(gender="F").count()
        ctx.update({
            "separated_count": sep_count,
            "separated_male_count": sep_m,
            "separated_female_count": sep_f,
            "separated_male_percent": round(sep_m * 100 / sep_count, 1) if sep_count else 0,
            "separated_female_percent": round(sep_f * 100 / sep_count, 1) if sep_count else 0,
        })

        # extra buckets based on your EMPLOYEE_STATUS_CHOICES
        buckets = {
            "training": StaffProfile.objects.filter(employee_status="inactive"),
            "returned": StaffProfile.objects.filter(employee_status="retired"),
            "not_returned": StaffProfile.objects.filter(employee_status="terminated"),
            "opportunity": StaffProfile.objects.exclude(specialization=""),
            "official": StaffProfile.objects.exclude(educational_level=""),
        }
        for key, qs in buckets.items():
            total = qs.count()
            m = qs.filter(gender="M").count()
            f = qs.filter(gender="F").count()
            ctx[f"{key}_count"] = total
            ctx[f"{key}_male_count"] = m
            ctx[f"{key}_female_count"] = f
            ctx[f"{key}_male_percent"] = round(m * 100 / total, 1) if total else 0
            ctx[f"{key}_female_percent"] = round(f * 100 / total, 1) if total else 0

        # template's "official" card uses different variable names
        ctx.update({
            "official_count": ctx.get("official_count", 0),
            "maleo_count": ctx.get("official_male_count", 0),
            "femaleo_count": ctx.get("official_female_count", 0),
            "maleo_percent": ctx.get("official_male_percent", 0),
            "femaleo_percent": ctx.get("official_female_percent", 0),
        })

        # pivot chart data
        ctx["chart_labels"] = [r["school_label"] for r in ctx["pivot_display"]]
        ctx["male_data"] = [r["gender_counts"]["Male"] for r in ctx["pivot_display"]]
        ctx["female_data"] = [r["gender_counts"]["Female"] for r in ctx["pivot_display"]]

        return ctx


custom_admin_site = CustomAdminSite(name="custom_admin")