
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

from django.utils.html import format_html, mark_safe
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime

from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from django.http import HttpResponse
import csv
import datetime
from django.forms import CheckboxSelectMultiple

from django import forms
from django.shortcuts import get_object_or_404
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType
from django.template.response import TemplateResponse
from django.urls import path
from .forms import SubjectForm
from django.utils.html import format_html, format_html_join

# start
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from django.contrib.auth.models import User
from django.contrib import admin
# end
# any_app/admin.py
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from import_export.admin import ImportExportModelAdmin
from .resources import UserResource
from django.db.models import Count
from django.db.models import Q
# Unregister the default User admin
admin.site.unregister(User)

# Re-register with import/export
@admin.register(User)
class UserAdmin(ImportExportModelAdmin, DefaultUserAdmin):
    resource_class = UserResource

# # Register default models with custom admin
# custom_admin_site.register(Group, GroupAdmin)
# custom_admin_site.register(User, UserAdmin)
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count, Q
from django.template.response import TemplateResponse


# -------- patch the DEFAULT admin site in place --------
_original_index = AdminSite.index


def _custom_index(self, request, extra_context=None):
    # Build app_list the normal way, but we let Django's default
    # get_app_list do its job (it respects perms + admin registry).
    app_list = self.get_app_list(request)
    total_models = sum(len(app["models"]) for app in app_list)

    context = {
        **self.each_context(request),
        "title": self.index_title or "Dashboard",
        "subtitle": None,
        "app_list": app_list,
        "total_models": total_models,
        **(extra_context or {}),
        **(_build_dashboard_context(request)),
    }
    request.current_app = self.name
    return TemplateResponse(request, "admin/index.html", context)


def _patched_get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())
    for app in app_list:
        app["models"].sort(key=lambda x: x["name"])
    return app_list


def _build_dashboard_context(request):
    from student.models import StudentProfile
    from humanresource.models import StaffProfile

    ctx = {}

    students = StudentProfile.objects.all()
    student_count = students.count()
    male_count = students.filter(Gender="Male").count()
    female_count = students.filter(Gender="Female").count()

    ctx.update({
        "student_count": student_count,
        "male_count": male_count,
        "female_count": female_count,
        "male_percent": round(male_count * 100 / student_count, 1) if student_count else 0,
        "female_percent": round(female_count * 100 / student_count, 1) if student_count else 0,
        "genders": {"Male": "ወንድ", "Female": "ሴት"},
    })

    grade_rows = (
        students.values("Grade")
        .annotate(
            males=Count("id", filter=Q(Gender="Male")),
            females=Count("id", filter=Q(Gender="Female")),
        )
        .order_by("Grade")
    )
    ctx.update({
        "grade_chart_labels": [str(r["Grade"]) for r in grade_rows],
        "grade_male_data": [r["males"] for r in grade_rows],
        "grade_female_data": [r["females"] for r in grade_rows],
    })

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

    # employees
    employees = StaffProfile.objects.filter(employee_status=True)
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

    separated = StaffProfile.objects.filter(employee_status=False)
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

    for key, qs in {
        "training": StaffProfile.objects.filter(employee_status="training"),
        "returned": StaffProfile.objects.filter(employee_status="returned"),
        "not_returned": StaffProfile.objects.filter(employee_status="training_returned_pending"),
        "opportunity": StaffProfile.objects.filter(specialization=True),
        "official": StaffProfile.objects.filter(educational_level=True),
    }.items():
        total = qs.count()
        m = qs.filter(gender="M").count()
        f = qs.filter(gender="F").count()
        ctx[f"{key}_count"] = total
        ctx[f"{key}_male_count"] = m
        ctx[f"{key}_female_count"] = f
        ctx[f"{key}_male_percent"] = round(m * 100 / total, 1) if total else 0
        ctx[f"{key}_female_percent"] = round(f * 100 / total, 1) if total else 0

    ctx.update({
        "official_count": ctx.get("official_count", 0),
        "maleo_count": ctx.get("official_male_count", 0),
        "femaleo_count": ctx.get("official_female_count", 0),
        "maleo_percent": ctx.get("official_male_percent", 0),
        "femaleo_percent": ctx.get("official_female_percent", 0),
    })

    ctx["chart_labels"] = [r["school_label"] for r in ctx["pivot_display"]]
    ctx["male_data"] = [r["gender_counts"]["Male"] for r in ctx["pivot_display"]]
    ctx["female_data"] = [r["gender_counts"]["Female"] for r in ctx["pivot_display"]]

    return ctx


# Apply the patch
admin.site.index = _custom_index.__get__(admin.site, AdminSite)
admin.site.get_app_list = _patched_get_app_list.__get__(admin.site, AdminSite)
# # Register Session model without admin class
# class SessionAdmin(admin.ModelAdmin):
#     list_display = ['session_key', 'expire_date']
#     readonly_fields = ['session_key', 'session_data', 'expire_date']
#     ordering = ['-expire_date']

# custom_admin_site.register(Session, SessionAdmin)

# # Register ContentType model without admin class
# class ContentTypeAdmin(admin.ModelAdmin):
#     list_display = ['app_label', 'model']
#     search_fields = ['app_label', 'model']

# custom_admin_site.register(ContentType, ContentTypeAdmin)

# # Also register LogEntry if needed
# from django.contrib.admin.models import LogEntry

# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
#     list_filter = ['action_time', 'user', 'content_type', 'action_flag']
#     search_fields = ['object_repr', 'change_message']
#     readonly_fields = ['action_time', 'user', 'content_type', 'object_id', 
#                        'object_repr', 'action_flag', 'change_message']

# custom_admin_site.register(LogEntry, LogEntryAdmin)

from django.contrib import admin
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from .models import ReportHeader, Year


@admin.register(ReportHeader)
class ReportHeaderAdmin(ImportExportModelAdmin):
    """
    Admin for ReportHeader.

    Business rule: at most one *active* ReportHeader may exist per
    academic year. Activating one silently deactivates the others.
    """

    # ── List view ────────────────────────────────────────────────────
    list_display = (
        "school_name",
        "academic_year",
        "archive_officer_display",
        "school_director_display",
        "active_badge",
        "created_at",
    )
    list_display_links = ("school_name",)
    list_filter = ("academic_year", "is_active")
    list_select_related = ("archive_officer", "school_director")
    list_per_page = 50
    ordering = ("-academic_year", "-created_at")

    search_fields = (
        "school_name",
        "academic_year",
        "archive_officer__full_name_en",
        "archive_officer__full_name_am",
        "school_director__full_name_en",
        "school_director__full_name_am",
    )

    # ── Form view ────────────────────────────────────────────────────
    autocomplete_fields = ("archive_officer", "school_director")
    readonly_fields = ("created_at",)
    save_on_top = True

    # Tuples inside "fields" = one row. "wide" = multi-column row.
    fieldsets = (
        (
            _("የት/ት ቤት መረጃ"),
            {
                "fields": (
                    ("school_name", "academic_year"),
                    ("education_bureau", "city_admin"),
                ),
                "classes": ("wide",),
            },
        ),
        (
            _("የኃላፊዎች መረጃ"),
            {
                "fields": (
                    ("archive_officer", "school_director"),
                ),
                "classes": ("wide",),
            },
        ),
        (
            _("ሁኔታ"),
            {
                "fields": (
                    ("is_active", "created_at"),
                ),
                "classes": ("wide", "collapse"),
            },
        ),
    )

    # ── Display helpers ──────────────────────────────────────────────
    @admin.display(
        description=_("Archive officer"),
        ordering="archive_officer__full_name_en",
    )
    def archive_officer_display(self, obj):
        return obj.archive_officer or "—"

    @admin.display(
        description=_("School director"),
        ordering="school_director__full_name_en",
    )
    def school_director_display(self, obj):
        return obj.school_director or "—"

    @admin.display(description=_("Active"), boolean=True, ordering="is_active")
    def active_badge(self, obj):
        return obj.is_active

    # ── Persistence hooks ────────────────────────────────────────────
    @transaction.atomic
    def save_model(self, request, obj, form, change):
        """Guarantee a single active ReportHeader per academic year."""
        if obj.is_active:
            (
                ReportHeader.objects
                .filter(academic_year=obj.academic_year, is_active=True)
                .exclude(pk=obj.pk)
                .update(is_active=False)
            )
        super().save_model(request, obj, form, change)

    def get_changeform_initial_data(self, request):
        """Default the academic year to the currently active Year."""
        initial = super().get_changeform_initial_data(request)
        active_year = Year.objects.filter(status="Active").first()
        if active_year:
            initial["academic_year"] = active_year
        return initial

    # ── Queryset tuning ──────────────────────────────────────────────
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("archive_officer", "school_director")
        )
    
class GradeAdmin(ImportExportModelAdmin):
    # pass
    fields = [('code', 'name'), 'description']
    list_display = ['id', 'code', 'name', 'description']
    search_fields = ['name', 'code', 'description']
    list_filter = ['name']
    list_display_links = ['id', 'code', 'name', 'description']
    save_on_top = True
    # readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    class Meta:
        model = Grade

admin.site.register(Grade, GradeAdmin)

class SectionAdmin(ImportExportModelAdmin):
    # pass
    fields = [('name', 'description')]
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['name']
    list_display_links = ['name', 'description']
    save_on_top = True
    # readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    class Meta:
        model = Section
        
admin.site.register(Section, SectionAdmin)

# Optional: Admin for the through model
# @admin.register(SubjectGrade)
# class SubjectGradeAdmin(admin.ModelAdmin):
#     list_display = ('subject', 'grade', 'created_at')
#     list_filter = ('subject', 'grade')
#     search_fields = ('subject__name', 'subject__code', 'grade__name')
#     list_select_related = ('subject', 'grade')
#     ordering = ('subject__name', 'grade__name')
@admin.register(Stream)
class StreamAdmin(ImportExportModelAdmin):
    fields = [('name', 'status')]
    list_display = ('id', 'colored_name', 'status')   # Show colored labels instead of plain text
    list_filter = ('name',)            # Sidebar filter
    search_fields = ('name',)          # Search box
    save_on_top = True

    def colored_name(self, obj):
        """
        Display stream name with a nice color badge.
        """
        colors = {
            'regular': '#3498db',  # Blue
            'natural': '#27ae60',  # Green
            'social': '#e67e22',   # Orange
        }

        color = colors.get(obj.name, '#7f8c8d')  # Default gray

        return format_html(
            '<span style="padding:4px 8px; border-radius:4px; '
            'background-color:{}; color:white; font-weight:bold;">{}</span>',
            color,
            obj.get_name_display()
        )

    colored_name.short_description = "Stream"
    colored_name.admin_order_field = "name"   # Allow sorting by name
    
@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    # Main table view
    list_display = ("id", "name", "code", "colored_stream", "is_active", "display_grades")
    list_display_links = ("id", "name", "code")
    list_editable = ("is_active",)

    # Filters
    list_filter = ("is_active", "stream", "grade_levels")

    # Search
    search_fields = ("name", "code")

    # Ordering
    ordering = ("name",)

    # Better ManyToMany UI
    filter_horizontal = ("grade_levels",)

    # Form layout
    fieldsets = (
        ("Subject Information", {
            "fields": (("name", "code"), ("stream", "description"))
        }),
        ("Grade Assignment", {
            "fields": ("grade_levels",),
            "description": "Select grade levels where this subject is taught"
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
    )

    save_on_top = True
    list_per_page = 25
    empty_value_display = "—"

    def colored_stream(self, obj):
        """
        Display stream with a colored badge.
        """
        if not obj.stream:
            return format_html('<span style="color:#999;">—</span>')

        colors = {
            'regular': '#3498db',   # Blue
            'natural': '#27ae60',   # Green
            'social': '#e67e22',    # Orange
        }

        color = colors.get(obj.stream.name, '#7f8c8d')

        return format_html(
            '<span style="padding:3px 10px; border-radius:12px; '
            'background-color:{}; color:white; font-weight:600; '
            'font-size:12px;">{}</span>',
            color,
            obj.stream.get_name_display()
        )

    colored_stream.short_description = "Stream"
    colored_stream.admin_order_field = "stream"


    def display_grades(self, obj):
        """
        Display selected grades as badges.
        """
        grades = obj.grade_levels.all().order_by('name')

        if not grades.exists():
            return format_html(
                '<span style="color:#999;">{}</span>',
                '— No grades —'
            )

        return format_html_join(
            '',
            '<span style="display:inline-block; margin:1px 4px 1px 0; '
            'padding:2px 8px; border-radius:10px; '
            'background:#ecf0f1; color:#2c3e50; font-size:11px; '
            'font-weight:600;">{}</span>',
            ((grade.name,) for grade in grades)
        )

    display_grades.short_description = "Grades"


    def save_model(self, request, obj, form, change):
        """
        Enforce uppercase subject codes.
        """
        if obj.code:
            obj.code = obj.code.upper().strip()
        super().save_model(request, obj, form, change)
        
class TeacherAssignmentDetailInline(admin.TabularInline):
    model = TeacherAssignmentDetail
    extra = 0

    fields = (
        'subject',
        'grade',
        'section',
        'status',
    )

    autocomplete_fields = (
        'subject',
        'grade',
        'section',
    )

    # show_change_link = True
    
@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(ImportExportModelAdmin):
    list_display = (
        'teacher',
        'is_section_head',
        'academic_year',
        'assigned_date',
        'number_of_sessions',
        'total_assignments',
    )

    list_filter = (
        'academic_year',
        'is_section_head',
        'details__grade',
        'details__section',
        'details__subject',
    )

    search_fields = (
        'teacher__full_name_en',
        'assigned_to__username',
        'number_of_sessions',
    )

    autocomplete_fields = (
        'teacher',
        'assigned_to',
        'academic_year',
        'grade',
        'section',
    )

    readonly_fields = ('assigned_date',)

    inlines = [TeacherAssignmentDetailInline]

    save_on_top = True

    fieldsets = (
        ('Teacher Assignment', {
            'fields': (
                ('teacher',
                'academic_year'),
                'is_section_head',
                ('grade',
                'section'),
                ('number_of_sessions',
                'assigned_to'),
            )
        }),
        ('System Information', {
            'fields': ('assigned_date',),
            'classes': ('collapse',),
        }),
    )

    ordering = ('teacher',)

    def total_assignments(self, obj):
        return obj.details.count()

    total_assignments.short_description = 'Assignments'
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        active_year = Year.objects.filter(status="Active").first()
        if active_year:
            initial["academic_year"] = active_year
        return initial
    
@admin.register(AssessmentName)
class AssessmentNameAdmin(ImportExportModelAdmin):
    # Show key fields in the list view
    list_display = (
        "name",
        "category",
        "is_active",
        "description_short",
    )
    list_filter = ("category", "is_active")  # Sidebar filters
    search_fields = ("name", "description")  # Quick search
    ordering = ("category", "name")  # Sorted nicely

    # Editable fields directly in list view
    list_editable = ("is_active",)
    save_on_top = True

    # Field grouping for clarity
    fieldsets = (
        ("Basic Info", {
            "fields": (("name", "category"), "description")
        }),
        ("Defaults & Status", {
            "fields": ("is_active",)
        }),
    )

    # Custom helper to shorten description in list view
    def description_short(self, obj):
        return (obj.description[:50] + "...") if obj.description and len(obj.description) > 50 else obj.description
    description_short.short_description = "Description"

# class WeightInline(admin.TabularInline):
#     model = Weight
#     extra = 0
#     # min_num = 1
#     ordering = ['order']
    
#     fields = ['name', 'weight', 'order', 'is_required']
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html


class BaseWeightInlineFormSet(BaseInlineFormSet):
    """
    Custom formset to validate that the sum of all weight percentages 
    equals 100% before saving the inline formset.
    """
    def clean(self):
        super().clean()
        
        total_weight = 0
        for form in self.forms:
            # Ignore deleted forms or empty forms
            if not form.cleaned_data or form.cleaned_data.get('DELETE', False):
                continue
            
            weight = form.cleaned_data.get('weight')
            if weight is not None:
                total_weight += weight

        # Optional: Enforce that active components must sum to 100%
        # (Remove or adjust this check if your business logic allows partial weights)
        if self.forms and total_weight != 100:
            raise ValidationError(
                f"The total weight percentage must equal 100%. "
                f"Current total is {total_weight}%."
            )

class WeightInline(admin.TabularInline):  # Changed to Tabular for a compact, spreadsheet-like view
    model = Weight
    formset = BaseWeightInlineFormSet
    extra = 0
    ordering = ['order', 'id']
    fields = ('name', 'weight', 'order', 'is_required', 'weight_bar')
    readonly_fields = ('weight_bar',)
    verbose_name_plural = "Weight Components"

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if formfield is not None:
            if db_field.name == 'weight':
                formfield.widget.attrs.update({
                    'style': 'width:70px;text-align:center;font-weight:600;',
                    'min': 0,
                    'max': 100,
                })
            elif db_field.name == 'order':
                formfield.widget.attrs.update({
                    'style': 'width:60px;text-align:center;',
                    'min': 0,
                })
        return formfield

    @admin.display(description="Distribution")
    def weight_bar(self, obj):
        if obj is None or obj.weight is None:
            return "—"
        pct = max(0, min(100, obj.weight))
        # Color coding: Green for low, Orange for mid, Red for high weights
        color = "#28a745" if pct < 60 else "#ffc107" if pct < 90 else "#dc3545"
        return format_html(
            '<div style="background:#e9ecef;border-radius:4px;height:16px;'
            'width:120px;position:relative;overflow:hidden;display:inline-block;vertical-align:middle;">'
            '<div style="background:{};width:{}%;height:100%;"></div>'
            '<span style="position:absolute;left:6px;top:-1px;font-size:11px;'
            'font-weight:600;color:#212529;">{}%</span>'
            '</div>',
            color, pct, pct,
        )
    
@admin.register(AssessmentFormula)
class AssessmentFormulaAdmin(ImportExportModelAdmin):
    list_display = (
        'name',
        'academic_year',
        'grade_level',
        'subject',
        'weights_summary',
        'max_score',
        'passing_score',
        'is_active'
    )
    
    list_filter = (
        'academic_year',
        'grade_level',
        'subject',
        'is_active'
    )
    
    search_fields = ('name', 'description')
    
    autocomplete_fields = ('academic_year', 'grade_level', 'subject')

    save_on_top = True
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('name',
                'academic_year'), 'is_active',
                ('grade_level', 'subject')
            )
        }),
        ('Scoring Configuration', {
            'fields': (
                ('max_score',
                'passing_score'),
            ),
            "classes": ('collapse', 'collapsed'),  # collapsible section
        }),       
    )
    
    inlines = [WeightInline]
    
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        active_year = Year.objects.filter(status="Active").first()
        if active_year:
            initial["academic_year"] = active_year
        return initial
    
    def weights_summary(self, obj):
        weights = obj.weights.all().order_by('order')
        if not weights.exists():
            return "No weights"
        
        weight_strings = [f"{weight.weight}%" for weight in weights]
        return "-".join(weight_strings)
    weights_summary.short_description = 'Weights'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        
@admin.register(Term)
class TermAdmin(ImportExportModelAdmin):
    # Main table view
    list_display = (
        "name",
        "academic_year",
        "start_date",
        "end_date",
        "is_active",
        "colored_status",
    )
    list_display_links = ("name",)
    list_editable = ("start_date", "end_date", "is_active")

    # Filters
    list_filter = (
        "academic_year",
        "is_active",
        "start_date",
    )

    # Search
    search_fields = (
        "name",
        "academic_year__name",
    )

    # Ordering
    ordering = ("academic_year", "name")

    # Autocomplete for foreign keys
    autocomplete_fields = ("academic_year",)

    # Form layout
    fieldsets = (
        ("Term Information", {
            "fields": (
                ("name",
                "academic_year"),
            )
        }),
        ("Schedule", {
            "fields": (
                ("start_date",
                "end_date"),
                "is_active",
            ),
            "classes": ("collapse",),  # collapsible section
        }),
    )

    save_on_top = True
    list_per_page = 25
    empty_value_display = "—"
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        active_year = Year.objects.filter(status="Active").first()
        if active_year:
            initial["academic_year"] = active_year
        return initial

    # Colored status indicator
    def colored_status(self, obj):
        color = "green" if obj.is_active else "red"
        label = "Active" if obj.is_active else "Inactive"
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color,
            label
        )
    colored_status.short_description = "Status"

class YearAdmin(ImportExportModelAdmin):
    # pass
    fields = [('id', 'year'), ('description', 'status')]
    list_display = ['id', 'year', 'description', 'status']
    search_fields = ['id', 'year', 'description', 'status']
    list_filter = ['year']
    list_display_links = ['id', 'year', 'description', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True
    save_on_top = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Year

admin.site.register(Year, YearAdmin)
