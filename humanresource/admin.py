from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.shortcuts import redirect
from django.db import connection
from django.http import HttpResponse
from django.utils import timezone
import datetime
from datetime import datetime
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse
from import_export.admin import ExportMixin

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .models import StaffProfile, AdminStaffProfile, Experience


class ExperienceInlineAdmin(admin.TabularInline):
    model = Experience
    extra = 0
    readonly_fields = ['id', 'net_duration']


# =====================================================================
# StaffAdmin  (Academic Staff)
# =====================================================================
class StaffAdmin(ImportExportModelAdmin):
    inlines = [ExperienceInlineAdmin]

    list_display = (
        "full_name_am", "full_name_en", 'gender',
        "print_employee_experience", "position", "colored_status", "hired_date"
    )
    list_filter = (
        "school", "work_cycles", "employee_status", "marital_status",
        "position", "gender", "educational_level"
    )
    list_display_links = (
        "full_name_am", "full_name_en", 'gender',
        "print_employee_experience", "position", "colored_status", "hired_date"
    )
    search_fields = ("full_name_am", "full_name_en", "position", "contact_number")
    ordering = ("-registered_at",)
    save_on_top = True

    readonly_fields = (
        "registered_at", "updated_at", "updated_by", "registered_by",
        "student_image_preview_on_form",
        "signature_preview",
    )

    fieldsets = (
        ("Personal Information", {
            "fields": (
                ("full_name_am", "full_name_en"),                    # 2 per row
                ("gender", "date_of_birth", "marital_status"),       # 3 per row
                ("nationality", "contact_number", "email"),          # 3 per row
            ),
            "classes": ("wide",),
        }),
        ("Employment Details", {
            "fields": (
                ("hired_date", "school", "work_cycles"),             # 3 per row
                ("career_growth", "previous_growth_hired"),          # 2 per row
                ("job_grade", "position", "employee_status"),        # 3 per row
                "salary",                                            # 1 per row
            ),
        }),
        ("Education", {
            "fields": (
                ("teaching_certificate", "specialization", "educational_level"),  # 3 per row
            ),
            "classes": ("collapse",),
        }),
        ("Tracking Information", {
            "fields": (
                ("registered_at", "updated_at"),                     # 2 per row
                ("registered_by", "updated_by"),                     # 2 per row
            ),
            "classes": ("collapse",),
        }),
        ("Staff Images", {
            "fields": (
                ("profile_picture", "signature"),                    # 2 per row
            ),
        }),
        ("Image Preview", {
            "fields": (
                ("student_image_preview_on_form", "signature_preview"),   # 2 per row
            ),
        }),
    )

    # ── previews ─────────────────────────────────────────────────────
    def student_image_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="height: 50px;"/></a>',
                obj.profile_picture.url,
                obj.profile_picture.url,
            )
        return "No Image"
    student_image_preview.short_description = "Student Image"

    def student_image_preview_on_form(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 300px;"/>',
                obj.profile_picture.url,
            )
        return "No Image"
    student_image_preview_on_form.short_description = "Image Preview"

    @admin.display(description='Signature')
    def signature_preview(self, obj):
        if obj.signature:
            return format_html(
                '<img src="{}" style="max-height:120px;max-width:300px;'
                'border:1px solid #ccc;padding:4px;background:#fff;" />',
                obj.signature.url,
            )
        return '—'

    # ── misc ─────────────────────────────────────────────────────────
    def print_employee_experience(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Print</a>',
            reverse('print_employee_experience', args=[obj.pk]),
        )
    print_employee_experience.short_description = "Print"

    def colored_status(self, obj):
        colors = {
            "active": "green",
            "inactive": "gray",
            "terminated": "red",
            "retired": "blue",
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.employee_status, "black"),
            obj.employee_status,
        )
    colored_status.admin_order_field = "employee_status"
    colored_status.short_description = "Status"

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.registered_by = request.user
        obj.save()


admin.site.register(StaffProfile, StaffAdmin)


# =====================================================================
# AdminStaffProfileAdmin  (Admin Staff)
# =====================================================================
class AdminStaffProfileAdmin(ImportExportModelAdmin):
    inlines = [ExperienceInlineAdmin]

    list_display = (
        'full_name_am',
        'full_name_en',
        'print_admin_experience',
        'gender',
        'date_of_birth',
        'marital_status',
        'nationality',
        'school',
        'job_title',
        'job_grade',
        'rank',
        'salary',
        'employee_status',
        'hired_date',
    )

    list_display_links = (
        'full_name_am',
        'full_name_en',
        'print_admin_experience',
        'gender',
        'date_of_birth',
        'marital_status',
        'nationality',
        'school',
        'job_title',
        'job_grade',
        'rank',
        'salary',
        'employee_status',
        'hired_date',
    )

    list_filter = (
        'gender', 'school', 'employee_status',
        'marital_status', 'educational_level', 'job_grade',
    )

    search_fields = ('full_name_am', 'full_name_en', 'job_title', 'email', 'contact_number')

    readonly_fields = (
        'registered_at',
        'updated_at',
        'student_image_preview_on_form',
        'signature_preview',
    )

    save_on_top = True

    fieldsets = (
        ('Personal Information', {
            'fields': (
                ('full_name_am', 'full_name_en'),                    # 2 per row
                ('gender', 'date_of_birth', 'marital_status'),       # 3 per row
                ('nationality', 'contact_number', 'email'),          # 3 per row
            ),
        }),
        ('Employment Information', {
            'fields': (
                ('school', 'job_title', 'new_job_code'),             # 3 per row
                ('job_grade', 'rank', 'educational_level'),          # 3 per row
                ('position', 'salary', 'employee_status'),           # 3 per row
                'hired_date',                                        # 1 per row
            ),
            "classes": ("collapse",),
        }),
        ('Audit Trail', {
            'fields': (
                ('registered_at', 'updated_at'),                     # 2 per row
                ('registered_by', 'updated_by'),                     # 2 per row
            ),
            "classes": ("collapse",),
        }),
        ('Staff Images', {
            'fields': (
                ('profile_picture', 'signature'),                    # 2 per row
            ),
        }),
        ('Image Preview', {
            'fields': (
                ('student_image_preview_on_form', 'signature_preview'),  # 2 per row
            ),
        }),
    )

    # ── previews ─────────────────────────────────────────────────────
    def student_image_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="height: 50px;"/></a>',
                obj.profile_picture.url,
                obj.profile_picture.url,
            )
        return "No Image"
    student_image_preview.short_description = "Student Image"

    def student_image_preview_on_form(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 300px;"/>',
                obj.profile_picture.url,
            )
        return "No Image"
    student_image_preview_on_form.short_description = "Image Preview"

    @admin.display(description='Signature')
    def signature_preview(self, obj):
        if obj.signature:
            return format_html(
                '<img src="{}" style="max-height:120px;max-width:300px;'
                'border:1px solid #ccc;padding:4px;background:#fff;" />',
                obj.signature.url,
            )
        return '—'

    # ── misc ─────────────────────────────────────────────────────────
    def print_admin_experience(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Print</a>',
            reverse('print_admin_experience', args=[obj.pk]),
        )
    print_admin_experience.short_description = "Print"

    def colored_status(self, obj):
        colors = {
            "active": "green",
            "inactive": "gray",
            "terminated": "red",
            "retired": "blue",
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.employee_status, "black"),
            obj.employee_status,
        )
    colored_status.admin_order_field = "employee_status"
    colored_status.short_description = "Status"

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.registered_by = request.user
        obj.save()


admin.site.register(AdminStaffProfile, AdminStaffProfileAdmin)

class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'print_leave_request', 'start_date', 'end_date', 'status', 'created_at', 'updated_at')
    list_filter = ('leave_type', 'status', 'created_at')
    search_fields = ('employee__First_name', 'employee__Last_name', 'leave_type', 'reason')
    list_display_links = ['employee', 'leave_type', 'print_leave_request', 'start_date', 'end_date', 'status']
    ordering = ('-created_at',)  # Order by created_at descending
    autocomplete_fields = ['employee']
    readonly_fields = ('created_at', 'updated_at')
    save_on_top = True  # Show save buttons at the top of the form
    
    def print_leave_request(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Print</a>',
            reverse('print_leave_request', args=[obj.pk])
        )

    print_leave_request.short_description = "Print"

    def has_change_permission(self, request, obj=None):
        # Custom permission logic if needed
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Custom permission logic if needed
        return super().has_delete_permission(request, obj)

# Register the model with the admin site
admin.site.register(LeaveRequest, LeaveRequestAdmin)

class OpenPositionAdmin(admin.ModelAdmin):
    list_display = (
        'job_title',
        'new_job_code',
        'current_rank',
        'new_rank',
        'rank',
        'salary',
        'status',
        'created_at',
    )
    list_filter = (
        'status',
        'current_rank',
        'new_rank',
        'created_at',
    )
    search_fields = (
        'job_title',
        'new_job_code',
    )
    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at')
    # autocomplete_fields = ['current_rank', 'new_rank']
    save_on_top = True  # Show save buttons at the top of the form
    fieldsets = (
        ('Job Information', {
            'fields': ('job_title', 'new_job_code', 'status')
        }),
        ('Rank and Payment', {
            'fields': ('current_rank', 'new_rank', 'rank', 'salary')
        }),
        ('Additional Notes', {
            'fields': ('notes',)
        }),
        ('Record Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return True  # Optional: You can customize this

    def has_change_permission(self, request, obj=None):
        return True  # Optional

    def has_delete_permission(self, request, obj=None):
        return True  # Optional
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.registered_by = request.user
        obj.save()  
        
admin.site.register(OpenPosition, OpenPositionAdmin)


