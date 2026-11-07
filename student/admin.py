from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportMixin
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.db import connection
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
# import csv
from django.utils import timezone
import datetime
from datetime import datetime
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from decimal import Decimal
from .models import *
from .forms import GenerateAssessmentForm
from django.utils.html import format_html

from django.utils.html import escape
from django.db.models import Q
# new
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image
from reportlab import lib
# new end

# New graph start
from django.contrib.admin import AdminSite
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
# from .forms import GenerateAssessmentForm

from .models import StudentResultJSONView
import json
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
# New graph end
import os
from django.conf import settings

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader  # <-- important
from reportlab.lib.enums import TA_CENTER

from django.template.response import TemplateResponse
from django.http import HttpResponse

import os
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django.contrib import admin, messages

from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# import settings
# ============================================================
# ===== REGISTER NYALA FONT (MUST BE AT MODULE LEVEL) =======
# ============================================================
NYALA_FONT_PATH = os.path.join(settings.BASE_DIR, "fonts", "Nyala.ttf")

if not os.path.exists(NYALA_FONT_PATH):
    raise FileNotFoundError(f"Nyala.ttf not found at {NYALA_FONT_PATH}")

pdfmetrics.registerFont(TTFont("Nyala", NYALA_FONT_PATH))


# ============================================================
# ===== HTML -> PDF helper ==================================
# ============================================================
def _html_to_pdf(html: str) -> bytes:
    result = BytesIO()
    status = pisa.CreatePDF(src=html, dest=result, encoding="utf-8")
    if status.err:
        raise RuntimeError("PDF generation failed")
    return result.getvalue()

class FullNameFilter(admin.SimpleListFilter):
    title = "Full Name (Amharic)"
    parameter_name = "full_name"

    def lookups(self, request, model_admin):
        return ()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Full_name__icontains=self.value())
        return queryset


class FullNameEnFilter(admin.SimpleListFilter):
    title = "Full Name (English)"
    parameter_name = "full_name_en"

    def lookups(self, request, model_admin):
        return ()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Full_name_en__icontains=self.value())
        return queryset
from django.contrib import admin, messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path, reverse

from .models import StudentProfile
from .forms import ClearanceForm

class StudentProfileAdmin(ImportExportMixin, admin.ModelAdmin):
    # Displayed fields in the list view of the admin interface
    list_display = [
        'id', 'student_image_preview', 'Full_name', 'Full_name_en', 'Gender', 'New_grade', 'New_section', 'status'
    ]
    list_display_links = ['student_image_preview', 'Full_name', 'Full_name_en', 'Gender']
    # list_editable = ['Date_of_birth']
    # Fields to filter by in the admin interface
    list_filter = (FullNameFilter, FullNameEnFilter, 'Gender', 'New_grade', 'New_section', 'status', 'admit_year')
    
    # Search functionality to search by Full name, Grade, Section, and Parent contact
    search_fields = ('id', 'Full_name', 'Full_name_en', 'New_grade__name', 'New_section__name', 'parent_contact')
    list_editable = ('status',)
    # Organizing the fields into collapsible sections using fieldsets for better clarity
    fieldsets = (
        (None, {
            'fields': (('Full_name', 'Full_name_en'), ('Gender', 'Date_of_birth'), ('admit_year', 'parent_contact'))
        }),
        ('Academic Information', { 
            'fields': (('academic_year', 'cycle'), ('New_grade', 'New_section'), ('Grade', 'Section'), ('status', 'school'))
        }),
        ('Student Images', {
            'fields': (('student_image', 'student_image1'), ('student_image2', 'student_image3'), ('discipline', 'Remark'))
        }),
        ('Image Preview', {
            'fields': ('student_image_preview_on_form',)
        }),
        
    )
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)
    list_per_page = 150
    ordering = ('-Full_name_en',)  # Order by English name descending
    autocomplete_fields = ['Grade', 'Section']
    save_on_top = True  # Show save buttons at the top of the form
    list_select_related = True  # Optimize database queries by selecting related objects
    
    save_on_top = True
    save_as = True
    actions = ["generate_academic_history", "print_clearance"]

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom = [
            path(
                "clearance-form/",
                self.admin_site.admin_view(self.clearance_form),
                name="student_studentprofile_clearance_form",
            ),
            path(
                "clearance-download/",
                self.admin_site.admin_view(self.clearance_download),
                name="student_studentprofile_clearance_download",
            ),
        ]
        return custom + urls

    # ── 1. ACTION: redirects to intermediate form ─────────────
    @admin.action(description="Get Clearance (መሸኛ) as PDF")
    def print_clearance(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "Please select exactly ONE student to download the clearance.",
                messages.WARNING,
            )
            return None
        student_id = queryset.first().id
        return HttpResponseRedirect(
            reverse("admin:student_clearance_form", args=[student_id])
        )

    # ── 2. REGISTER CUSTOM URLS ───────────────────────────────
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "clearance-form/<int:student_id>/",
                self.admin_site.admin_view(self.clearance_form_view),
                name="student_clearance_form",
            ),
        ]
        return custom + urls

    # ── 3. INTERMEDIATE VIEW: show modal + handle POST ────────
    def clearance_form_view(self, request, student_id):
        student = get_object_or_404(StudentProfile, pk=student_id)

        if request.method == "POST":
            form = ClearanceForm(request.POST)
            if form.is_valid():
                # (Optional) persist the values on the student record
                # Uncomment the next 5 lines if you added the fields
                # to StudentProfile in Step 5.
                #
                # student.leave_reason    = form.cleaned_data["reason"]
                # student.leave_date      = form.cleaned_data["leave_date"]
                # student.property_status = form.cleaned_data["property_status"]
                # student.result_status   = form.cleaned_data["result_status"]
                # student.save()

                # Call the PDF generator with submitted values
                return self._generate_clearance_pdf(
                    request,
                    student,
                    form.cleaned_data["reason"],
                    form.cleaned_data["leave_date"],
                    form.cleaned_data["property_status"],
                    form.cleaned_data["result_status"],
                )
        else:
            # GET → pre-fill the form with defaults
            form = ClearanceForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "Clearance",
            "form": form,
            "student": student,
            "opts": self.model._meta,
        }
        return TemplateResponse(
            request, "admin/clearance_modal.html", context
        )

    # ── 4. PDF GENERATOR (your original code, unchanged) ──────
    def _generate_clearance_pdf(
        self, request, student,
        reason, leave_date, property_status, result_status,
    ):
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.pdfgen import canvas
        from reportlab.platypus import Table, TableStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.lib.utils import ImageReader
        import json, os

        # ---------------- fetch from the view ----------------
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM STUDENT_RESULT_JSON_VIEW WHERE student_id = %s "
                "ORDER BY semester",
                [student.id],
            )
            cols = [c[0].lower() for c in cursor.description]
            rows = [dict(zip(cols, r)) for r in cursor.fetchall()]

        if not rows:
            self.message_user(
                request,
                "No result data found for this student.",
                messages.WARNING,
            )
            return HttpResponseRedirect(
                reverse("admin:student_clearance_form", args=[student.id])
            )

        for r in rows:
            raw = r.get("subjects") or "{}"
            try:
                r["subjects_dict"] = json.loads(raw) if isinstance(raw, str) else raw
            except Exception:
                r["subjects_dict"] = {}

        # ---------------- helpers ----------------
        SUBJECT_LABELS = {"Amharic": "አማርኛ", "English": "English"}
        ROW_TERM_MAP = {"s1": ["Term one"], "s2": ["Term two"]}

        def to_num(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return None

        def avg_num(vals):
            nums = [to_num(v) for v in vals if to_num(v) is not None]
            return round(sum(nums) / len(nums), 2) if nums else None

        def avg_dict(dicts):
            acc, counts = {}, {}
            for d in dicts:
                if not d:
                    continue
                for k, v in d.items():
                    n = to_num(v)
                    if n is None:
                        continue
                    acc[k] = acc.get(k, 0.0) + n
                    counts[k] = counts.get(k, 0) + 1
            return {k: round(acc[k] / counts[k], 2) for k in acc}

        def fmt2(v):
            f = to_num(v)
            return f"{f:.2f}" if f is not None else ""

        # ---------------- organize terms ----------------
        terms = {}
        for r in rows:
            sem = (r.get("semester") or "").strip()
            if sem:
                terms[sem] = r

        anchor = next(iter(terms.values()), None)
        if anchor is None:
            self.message_user(request, "Missing term data.", messages.ERROR)
            return HttpResponseRedirect(
                reverse("admin:student_clearance_form", args=[student.id])
            )

        def resolve_slot(slot):
            dicts, totals, avgs, ranks = [], [], [], []
            for term_name in ROW_TERM_MAP[slot]:
                t = terms.get(term_name)
                if t:
                    dicts.append(t["subjects_dict"])
                    totals.append(t.get("total"))
                    avgs.append(t.get("average"))
                    ranks.append(t.get("rank"))
            return (
                avg_dict(dicts),
                avg_num(totals),
                avg_num(avgs),
                (ranks[0] if ranks else None),
            )

        s1_subj, s1_total, s1_avg, s1_rank = resolve_slot("s1")
        s2_subj, s2_total, s2_avg, s2_rank = resolve_slot("s2")
        av_subj  = avg_dict([s1_subj, s2_subj])
        av_total = avg_num([s1_total, s2_total])
        av_avg   = avg_num([s1_avg, s2_avg])
        av_rank  = anchor.get("yearly_rank") or anchor.get("rank") or ""

        PREFERRED_SUBJECT_ORDER = [
            "Amharic", "English", "Maths", "Mathematics", "Science",
            "Social Studies", "Civics", "Geography", "History",
            "Biology", "Chemistry", "Physics", "Computer", "ICT",
        ]
        discovered = set()
        for d in (s1_subj, s2_subj, av_subj):
            discovered.update(d.keys())
        ordered_subjects = [s for s in PREFERRED_SUBJECT_ORDER if s in discovered]
        ordered_subjects += sorted(s for s in discovered if s not in ordered_subjects)
        subject_headers = [SUBJECT_LABELS.get(s, s) for s in ordered_subjects]

        # ---------------- header values ----------------
        head = anchor
        report_title    = head.get("report_title") or "—"
        archive_officer = head.get("archive_officer_name") or "—"
        school_director = head.get("school_director_name") or "—"
        student_name    = head.get("student_name") or student.Full_name
        gender          = head.get("gender") or student.Gender
        age             = head.get("age") or ""
        grade           = head.get("grade") or ""
        section         = head.get("section") or ""
        academic_year   = head.get("academic_year") or ""
        discipline      = head.get("discipline") or "A"

        gender_disp = {
            "Male": "ወንድ (Male)",
            "Female": "ሴት (Female)",
        }.get(gender, gender)

        # ---------------- response ----------------
        response = HttpResponse(content_type="application/pdf")
        safe_name = (student.Full_name_en or "student").replace(" ", "_")
        response["Content-Disposition"] = (
            f'attachment; filename="clearance_{student.id}_{safe_name}.pdf"'
        )

        c = canvas.Canvas(response, pagesize=landscape(A4))
        width, height = landscape(A4)

        LEFT_MARGIN = 0.7 * cm
        RIGHT_MARGIN = 0.7 * cm
        available_width = width - LEFT_MARGIN - RIGHT_MARGIN

        photo_w, photo_h = 2.5 * cm, 3.0 * cm
        photo_x = width - RIGHT_MARGIN - photo_w
        y_qutr = height - 0.8 * cm
        y_qen  = height - 1.3 * cm
        y_photo_top = height - 1.9 * cm
        photo_y = y_photo_top - photo_h

        c.setFont("Nyala", 8.5)
        c.drawRightString(width - RIGHT_MARGIN, y_qutr, f"ቁጥር: {'_'*30}")
        c.drawRightString(width - RIGHT_MARGIN, y_qen,  f"ቀን: {'_'*31}")

        if student.student_image:
            img_path = None
            try:
                img_path = student.student_image.path
            except Exception:
                pass
            if img_path and os.path.exists(img_path):
                try:
                    img = ImageReader(img_path)
                    iw, ih = img.getSize()
                    scale = min(photo_w / iw, photo_h / ih)
                    dw, dh = iw * scale, ih * scale
                    dx = photo_x + (photo_w - dw) / 2
                    dy = photo_y + (photo_h - dh) / 2
                    c.drawImage(img, dx, dy, width=dw, height=dh, mask="auto")
                except Exception:
                    pass
            c.setStrokeColor(colors.grey)
            c.rect(photo_x, photo_y, photo_w, photo_h, stroke=1, fill=0)

        # ---------------- HEADER ----------------
        y = height - 1.5 * cm
        max_title_w = width - LEFT_MARGIN - (photo_w + 0.5 * cm) - 1.5 * cm
        font_size = 10
        title_text = report_title
        while c.stringWidth(title_text, "Nyala", font_size) > max_title_w and font_size > 6:
            font_size -= 0.5
        c.setFont("Nyala", font_size)
        c.drawString(LEFT_MARGIN, y, title_text)
        y -= 0.6 * cm

        c.setFont("Nyala", 9)
        c.drawString(LEFT_MARGIN, y, "ለሚመለከተው ሁሉ")
        y -= 0.55 * cm

        # ---------------- METADATA (underlined labels) ----------
        meta_lines = [
            ("የተማሪው ሙሉ ስም፡", f"{student_name}"),
            ("ጾታ፡", f"{gender_disp}   |   እድሜ: {age}   |   የት/ዘመን፡ {academic_year}"),
            ("የሚማርበት ክፍል፡", f"{grade}   |   ሴክሽን፡ {section}"),
            ("ት/ቤቱን የለቀቀበት ምክንያት፡", f"{reason}"),
            ("ት/ቤቱን የለቀቀበት ቀን፡", f"{leave_date}"),
            ("የት/ቤቱ ንብረት፡", f"{property_status}"),
            ("የተሰጠው ት/ት ውጤት፡", f"{result_status}"),
        ]
        c.setFont("Nyala", 8.5)
        line_h = 0.42 * cm

        def draw_underlined_label(x, y, label, size=8.5):
            c.setFont("Nyala", size)
            c.drawString(x, y, label)
            w = c.stringWidth(label, "Nyala", size)
            c.setLineWidth(0.4)
            c.line(x, y - 1.5, x + w, y - 1.5)

        for label, value in meta_lines:
            draw_underlined_label(LEFT_MARGIN, y, label)
            label_w = c.stringWidth(label, "Nyala", 8.5)
            c.drawString(LEFT_MARGIN + label_w + 4, y, value)
            y -= line_h

        y -= 0.3 * cm

        # ---------------- RESULTS TABLE ----------------
        header_row = ["ወከ", "ትምህርት"] + subject_headers + [
            "አማካኝ", "ደረጃ", "አባይ", "ምርመራ", "ውጤት",
        ]

        def data_row(num, label, subj_dict, avg_v, rnk, disc, remark, first):
            row = [str(num) if first else "", label]
            for s in ordered_subjects:
                v = subj_dict.get(s)
                row.append(fmt2(v) if v is not None else "-")
            row.extend([
                fmt2(avg_v) if avg_v is not None else "-",
                str(rnk or ""),
                disc,
                remark,
                result_status if first else "",
            ])
            return row

        table_data = [header_row]
        table_data.append(data_row(1, "1ኛ ሰሚስተር", s1_subj, s1_avg, s1_rank, discipline, "", True))
        table_data.append(data_row(2, "2ኛ ሰሚስተር", s2_subj, s2_avg, s2_rank, discipline, "", False))
        table_data.append(data_row("", "አማካኝ", av_subj, av_avg, av_rank, discipline, "", False))

        n_cols = len(header_row)
        base = available_width / (n_cols + 4 * 0.6)
        col_widths = []
        for h in header_row:
            if h == "ወከ":
                col_widths.append(base * 0.5)
            elif h == "ትምህርት":
                col_widths.append(base * 1.6)
            elif h in ("ደረጃ", "አባይ", "ምርመራ"):
                col_widths.append(base * 0.8)
            elif h == "ውጤት":
                col_widths.append(base * 1.2)
            else:
                col_widths.append(base)
        total_w = sum(col_widths)
        if total_w > available_width:
            k = available_width / total_w
            col_widths = [w * k for w in col_widths]

        results_table = Table(table_data, colWidths=col_widths, repeatRows=1)

        style = [
            ("FONTNAME", (0, 0), (-1, -1), "Nyala"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
            ("TOPPADDING", (0, 0), (-1, -1), 1.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 1),
            ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
        ]
        last_col = n_cols - 1
        style.append(("SPAN", (last_col, 1), (last_col, 3)))
        style.append(("VALIGN", (last_col, 1), (last_col, 3), "MIDDLE"))
        style.append(("BACKGROUND", (0, 3), (-1, 3), colors.whitesmoke))

        results_table.setStyle(TableStyle(style))
        w, h = results_table.wrapOn(c, width, y)
        results_table.drawOn(c, LEFT_MARGIN, y - h)
        y -= h + 0.6 * cm

        # ---------------- SIGNATURES ----------------
        sig_left_label  = "የሪከርድና ማህደር ኃላፊ፡"
        sig_right_label = "የት/ቤቱ ርዕስ መምህር፡"
        half = available_width / 2

        draw_underlined_label(LEFT_MARGIN, y, sig_left_label)
        draw_underlined_label(LEFT_MARGIN + half, y, sig_right_label)
        y -= 0.5 * cm

        c.setFont("Nyala", 8.5)
        c.drawString(LEFT_MARGIN, y, f"ስም/Name: {archive_officer}")
        c.drawString(LEFT_MARGIN + half, y, f"ስም/Name: {school_director}")
        y -= 0.6 * cm

        c.drawString(LEFT_MARGIN, y, "ፊርማ/Signature: ____________________")
        c.drawString(LEFT_MARGIN + half, y, "ፊርማ/Signature: ____________________")

        c.showPage()
        c.save()
        return response
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        active_year = Year.objects.filter(status="Active").first()
        if active_year:
            initial["academic_year"] = active_year
        return initial
    
    def generate_academic_history(self, request, queryset):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('SP_FILL_ACADEMIC_HISTORY')

            self.message_user(
                request,
                "Academic history generated successfully.",
                messages.SUCCESS
            )

        except Exception as e:
            self.message_user(
                request,
                f"Error: {e}",
                messages.ERROR
            )

    generate_academic_history.short_description = (
        "Generate Academic History"
    )
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'student_image':
            formfield.widget.attrs['style'] = 'max-width: 200px;'
            formfield.widget.attrs['class'] = 'vImageField'  # For styling
        return formfield

    # Custom method to show the image as a link in the list view
    def student_image_preview(self, obj):
        if obj.student_image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="height: 50px;"/></a>',
                obj.student_image.url,  # Full image link
                obj.student_image.url   # Thumbnail preview
            )
        return "No Image"
    student_image_preview.short_description = "Student Image"

    # Add an image preview to the change form page (readonly)
    def student_image_preview_on_form(self, obj):
        if obj.student_image:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 300px;"/>',
                obj.student_image.url
            )
        return "No Image"
    student_image_preview_on_form.short_description = "Image Preview"

    # Add the student_image_preview_on_form method to readonly_fields to display in the form
    readonly_fields = ('student_image_preview_on_form',)

    # Display the academic status in a more readable way (optional)
    def get_status_display(self, obj):
        return dict(StudentProfile.ACADEMIC_STATUS_CHOICES).get(obj.status, obj.status)
    get_status_display.short_description = 'Academic Status'
    
    def save_model(self, request, obj, form, change):
        """
        Automatically set the `created_by` and `modified_by` fields to the current user.
        """
        if not obj.pk:  # If the object is being created
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

# Register the StudentProfile model with the custom admin class
admin.site.register(StudentProfile, StudentProfileAdmin)

@admin.register(AcademicHistory)
class AcademicHistoryAdmin(admin.ModelAdmin):
    # 📌 Main list view
    list_display = (
        'student_name',
        'academic_year',
        'grade',
        'section',
        'status_badge',
        'created_at',
    )

    list_filter = (
        'academic_year',
        'grade',
        'status',
    )

    search_fields = (
        'student__full_name',
        'student__student_id',
        'academic_year',
    )
    
    list_editable = ('grade', 'section',)

    ordering = ('-academic_year', 'student')

    date_hierarchy = 'created_at'

    list_per_page = 20

    # 📌 Form layout
    fieldsets = (
        ('Student Information', {
            'fields': ('student',)
        }),
        ('Academic Details', {
            'fields': (
                'academic_year',
                ('grade', 'section'),
            )
        }),
        ('Status & Remarks', {
            'fields': ('status', 'remark'),
            'classes': ('collapse',),
        }),
    )# The above code is using Python to create a comment. In Python, comments are
    # denoted by the "#" symbol, and they are used to provide explanations or notes
    # within the code that are not executed by the interpreter. In this case, the
    # comment appears to be indicating a score or rating using the "#" symbol
    # repeated multiple times.
    

    autocomplete_fields = ('student',)

    readonly_fields = ('created_at',)

    # 🎨 Custom columns
    def student_name(self, obj):
        return obj.student
    student_name.short_description = "Student"
    student_name.admin_order_field = 'student'

    def status_badge(self, obj):
        color_map = {
            'Promoted': '#28a745',     # green
            'Repeated': '#ffc107',     # yellow
            'Transferred': '#17a2b8',  # blue
            'Dropped': '#dc3545',      # red
        }
        color = color_map.get(obj.status, '#6c757d')
        return format_html(
            '<span style="padding:4px 10px; '
            'border-radius:12px; '
            'color:white; '
            'background:{}; '
            'font-weight:600;">{}</span>',
            color,
            obj.status
        )
    status_badge.short_description = "Status"

@admin.register(StudentAssessment)
class StudentAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "subject_name",
        "academic_year",
        "total_score",
        "result_status",
        "colored_result_status",
        "created_at",
    )
    list_filter = (
        "result_status",
        "academic_year",
        "subject",
        "assessment_formula",
    )
    search_fields = (
        "student__Full_name",
        "subject__name",
        "assessment_formula__name",
    )
    autocomplete_fields = (
        "student",
        "subject",
        "assessment_formula",
        "academic_year",
    )
    date_hierarchy = "created_at"
    save_on_top = True
    list_select_related = (
        "student",
        "subject",
        "academic_year",
        "assessment_formula",
    )

    # ── Path must match the actual template location ───────────────
    change_list_template = "admin/student/studentassessment/change_list.html"

    # ── Queryset scoping for non-superusers ────────────────────────
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        try:
            teacher_assignment = TeacherAssignment.objects.get(
                assigned_to=request.user
            )
        except TeacherAssignment.DoesNotExist:
            return qs.none()

        details = TeacherAssignmentDetail.objects.filter(
            assignment=teacher_assignment,
            status="ACTIVE",
        )

        q = Q()
        for d in details:
            q |= Q(
                student__New_grade=d.grade,
                student__New_section=d.section,
                subject=d.subject,
            )

        return qs.filter(q)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        active_year = Year.objects.filter(status="Active").first()
        if active_year:
            initial["academic_year"] = active_year
        return initial

    # ── Custom URL for the generation endpoint ─────────────────────
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "generate-assessments/",
                self.admin_site.admin_view(self.generate_assessments_view),
                name="student_studentassessment_generate",
            ),
        ]
        return custom + urls

    # ── Display helpers ────────────────────────────────────────────
    @admin.display(description="Student", ordering="student__Full_name")
    def student_name(self, obj):
        return obj.student.Full_name if obj.student else "Unknown"

    @admin.display(description="Subject", ordering="subject__name")
    def subject_name(self, obj):
        return obj.subject.name if obj.subject else "Unknown"

    @admin.display(description="Result", ordering="result_status")
    def colored_result_status(self, obj):
        from django.utils.html import format_html

        if not obj.result_status:
            return format_html('<span style="color:gray;"><b>N/A</b></span>')

        color_map = {"PASS": "green", "FAIL": "red", "PENDING": "orange"}
        color = color_map.get(obj.result_status.upper(), "black")
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color,
            obj.result_status,
        )

    # ── Generation endpoint (GET = fragment, POST = run proc) ──────
    def generate_assessments_view(self, request):
        if request.method == "POST":
            form = GenerateAssessmentForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data["subject"]
                academic_year = form.cleaned_data["academic_year"]
                term = form.cleaned_data["term"]
                try:
                    with connection.cursor() as cursor:
                        cursor.callproc(
                            "GENERATE_STUDENT_ASSESSMENTS_WORKINGS",
                            [subject.id, academic_year.id, term.id],
                        )
                    messages.success(
                        request, "✅ Student assessments generated successfully!"
                    )
                    return redirect(
                        "admin:student_studentassessment_changelist"
                    )
                except Exception as exc:
                    logger.exception("Generate assessments failed")
                    messages.error(
                        request, f"❌ Error generating assessments: {exc}"
                    )
                    # fall through to re-render the form with error message
            else:
                messages.error(request, "❌ Please correct the errors below.")

            # Re-render the fragment (so JS can show errors inline)
            return render(
                request,
                "admin/student/studentassessment/generate_assessments.html",
                {"form": form, "title": "Generate Student Assessments"},
            )

        # GET → return the HTML fragment for the modal
        form = GenerateAssessmentForm()
        return render(
            request,
            "admin/student/studentassessment/generate_assessments.html",
            {"form": form, "title": "Generate Student Assessments"},
        )

# In setups/admin.py
@admin.register(AssignmentCompletenessView)
class AssignmentCompletenessViewAdmin(ImportExportModelAdmin):
    # Display
    list_display = (
        'issue_type_badge',
        'academic_year',
        'grade_section',
        'subject_or_info',
        'student_count',
        # 'quick_actions',
    )
    
    list_display_links = None  # No links since it's read-only
    
    # Filters
    list_filter = (
        'issue_type',
        'academic_year',
        'grade',
        'section',
    )
    
    # Search
    search_fields = (
        'grade',
        'section',
        'subject_name',
    )
    
    # Read-only
    readonly_fields = [f.name for f in AssignmentCompletenessView._meta.fields]
    
    # Layout
    list_per_page = 100
    actions = ['export_to_csv', 'send_report_email']
    
    # Change list template (inline)
    def changelist_view(self, request, extra_context=None):
        # Add custom context for dashboard
        extra_context = extra_context or {}
        extra_context.update({
            'title': '📊 Assignment Completeness Dashboard',
            'subtitle': 'Monitor and fix assignment issues in your school system',
        })
        return super().changelist_view(request, extra_context=extra_context)
    
    # Custom methods
    def issue_type_badge(self, obj):
        """Beautiful color-coded badge for issue type"""
        issue_config = {
            'SECTION_WITHOUT_HEAD': {
                'color': '#dc3545',
                'icon': '👑',
                'text': 'No Section Head',
                'bg_color': '#f8d7da',
                'text_color': '#721c24'
            },
            'SUBJECT_WITHOUT_TEACHER': {
                'color': '#ffc107',
                'icon': '📚',
                'text': 'No Teacher',
                'bg_color': '#fff3cd',
                'text_color': '#856404'
            },
            'STUDENT_WITHOUT_SUBJECTS': {
                'color': '#17a2b8',
                'icon': '👨‍🎓',
                'text': 'No Subjects',
                'bg_color': '#d1ecf1',
                'text_color': '#0c5460'
            },
        }
        
        config = issue_config.get(obj.issue_type, {
            'color': '#6c757d',
            'icon': '❓',
            'text': obj.get_issue_type_display(),
            'bg_color': '#e2e3e5',
            'text_color': '#383d41'
        })
        
        return format_html(
            '<div style="display: inline-flex; align-items: center; gap: 8px; '
            'padding: 6px 12px; border-radius: 6px; '
            'background-color:{}; border-left: 4px solid {};">'
            '<span style="font-size: 14px;">{}</span>'
            '<span style="font-weight: 600; font-size: 11px; color:{};">{}</span>'
            '</div>',
            config['bg_color'],
            config['color'],
            config['icon'],
            config['text_color'],
            config['text']
        )
    issue_type_badge.short_description = 'Issue Type'
    issue_type_badge.admin_order_field = 'issue_type'
    
    def grade_section(self, obj):
        """Beautiful grade and section display"""
        return format_html(
            '<div style="display: inline-flex; align-items: center; gap: 4px; '
            'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
            'padding: 6px 12px; border-radius: 6px; color: white; font-weight: 600;">'
            '<span>Grade {}</span>'
            '<span style="opacity: 0.8;">|</span>'
            '<span>Section {}</span>'
            '</div>',
            obj.grade,
            obj.section
        )
    grade_section.short_description = 'Class'
    grade_section.admin_order_field = 'grade'
    
    def subject_or_info(self, obj):
        """Display subject or contextual information"""
        if obj.issue_type == 'SUBJECT_WITHOUT_TEACHER' and obj.subject_name:
            return format_html(
                '<div style="display: flex; align-items: center; gap: 8px;">'
                '<span style="color: #495057; font-weight: 500;">📖 {}</span>'
                '</div>',
                obj.subject_name
            )
        elif obj.issue_type == 'SECTION_WITHOUT_HEAD':
            return format_html(
                '<span style="display: inline-flex; align-items: center; gap: 6px; '
                'color: #6c757d; font-size: 12px; padding: 4px 8px; '
                'background: #f8f9fa; border-radius: 4px;">'
                '<span>👨‍🏫</span>'
                '<span>Needs section head teacher</span>'
                '</span>'
            )
        elif obj.issue_type == 'STUDENT_WITHOUT_SUBJECTS':
            return format_html(
                '<span style="display: inline-flex; align-items: center; gap: 6px; '
                'color: #6c757d; font-size: 12px; padding: 4px 8px; '
                'background: #f8f9fa; border-radius: 4px;">'
                '<span>📝</span>'
                '<span>Students need subject assignments</span>'
                '</span>'
            )
        return format_html('<span style="color: #adb5bd;">—</span>')
    subject_or_info.short_description = 'Details'
    
    def student_count(self, obj):
        """Display count of affected students"""
        from django.db import connection
        
        try:
            if obj.issue_type == 'STUDENT_WITHOUT_SUBJECTS':
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student_studentprofile 
                        WHERE status = 'Active'
                        AND academic_year = :year
                        AND New_grade_id = :grade
                        AND New_section_id = :section
                        AND NOT EXISTS (
                            SELECT 1 FROM setups_teacherassignmentdetail 
                            WHERE grade_id = student_studentprofile.New_grade_id
                            AND section_id = student_studentprofile.New_section_id
                            AND status = 'ACTIVE'
                        )
                    """, {
                        'year': obj.academic_year,
                        'grade': obj.grade,
                        'section': obj.section
                    })
                    count = cursor.fetchone()[0]
                
                # Color based on count
                if count > 10:
                    badge_color = '#dc3545'
                    icon = '🔴'
                elif count > 5:
                    badge_color = '#ffc107'
                    icon = '🟡'
                else:
                    badge_color = '#28a745'
                    icon = '🟢'
                
                return format_html(
                    '<div style="display: inline-flex; align-items: center; gap: 8px; '
                    'padding: 4px 10px; background: {}; border-radius: 20px; '
                    'color: white; font-weight: 600;">'
                    '<span>{}</span>'
                    '<span>{}</span>'
                    '</div>',
                    badge_color,
                    icon,
                    f'{count} student(s)'
                )
            
            elif obj.issue_type == 'SUBJECT_WITHOUT_TEACHER':
                # Show that this affects all students in the section
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT COUNT(DISTINCT sp.id)
                        FROM student_studentprofile sp
                        WHERE sp.status = 'Active'
                        AND sp.academic_year = :year
                        AND sp.New_grade_id = :grade
                        AND sp.New_section_id = :section
                    """, {
                        'year': obj.academic_year,
                        'grade': obj.grade,
                        'section': obj.section
                    })
                    count = cursor.fetchone()[0]
                
                return format_html(
                    '<span style="color: #6c757d; font-size: 12px;">'
                    '📊 Affects {} students'
                    '</span>',
                    count
                )
        
        except Exception:
            pass
        
        return format_html('<span style="color: #adb5bd;">—</span>')
    student_count.short_description = 'Impact'
    
    
    # Admin actions
    @admin.action(description="📥 Export selected issues to CSV")
    def export_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="assignment_issues_{}.csv"'.format(
            timezone.now().strftime('%Y%m%d_%H%M%S')
        )
        
        writer = csv.writer(response)
        
        # Header
        writer.writerow([
            'Issue Type', 'Academic Year', 'Grade', 'Section',
            'Subject', 'Impact', 'Priority', 'Action Required'
        ])
        
        # Data
        for item in queryset:
            if item.issue_type == 'SECTION_WITHOUT_HEAD':
                priority = 'HIGH'
                action = 'Assign section head teacher'
            elif item.issue_type == 'SUBJECT_WITHOUT_TEACHER':
                priority = 'MEDIUM'
                action = f'Assign teacher to {item.subject_name}'
            else:
                priority = 'MEDIUM'
                action = 'Assign subjects to affected students'
            
            writer.writerow([
                item.get_issue_type_display(),
                item.academic_year,
                item.grade,
                item.section,
                item.subject_name or 'N/A',
                f'{item.affected_count if hasattr(item, "affected_count") else "Multiple"} affected',
                priority,
                action
            ])
        
        return response
    
    @admin.action(description="📊 Generate summary report")
    def send_report_email(self, request, queryset):
        # Create a simple summary
        summary = {}
        for item in queryset:
            key = f"{item.grade}{item.section}"
            if key not in summary:
                summary[key] = {
                    'sections_without_head': 0,
                    'subjects_without_teacher': 0,
                    'students_without_subjects': 0
                }
            
            if item.issue_type == 'SECTION_WITHOUT_HEAD':
                summary[key]['sections_without_head'] += 1
            elif item.issue_type == 'SUBJECT_WITHOUT_TEACHER':
                summary[key]['subjects_without_teacher'] += 1
            elif item.issue_type == 'STUDENT_WITHOUT_SUBJECTS':
                summary[key]['students_without_subjects'] += 1
        
        # Create message
        message_parts = ["📋 Assignment Issues Summary:\n"]
        message_parts.append("=" * 40)
        
        for class_key, counts in summary.items():
            message_parts.append(f"\n{class_key}:")
            if counts['sections_without_head']:
                message_parts.append(f"  • {counts['sections_without_head']} section(s) without head")
            if counts['subjects_without_teacher']:
                message_parts.append(f"  • {counts['subjects_without_teacher']} subject(s) without teacher")
            if counts['students_without_subjects']:
                message_parts.append(f"  • {counts['students_without_subjects']} student group(s) without subjects")
        
        message = "\n".join(message_parts)
        
        # Show as Django message
        from django.contrib import messages
        messages.success(request, message.replace('\n', '<br>'))
    
    # Permissions
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
# resources.py
from decimal import Decimal, InvalidOperation
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import (
    StudentAssessmentScore, StudentProfile, Subject, Year,
    Weight, Grade, Section, Term,
)


class StudentAssessmentScoreResource(resources.ModelResource):
    student = fields.Field(
        column_name="student", attribute="student",
        widget=ForeignKeyWidget(StudentProfile, "Full_name"),
    )
    subject = fields.Field(
        column_name="subject", attribute="subject",
        widget=ForeignKeyWidget(Subject, "name"),
    )
    academic_year = fields.Field(
        column_name="academic_year", attribute="academic_year",
        widget=ForeignKeyWidget(Year, "year"),
    )
    weight = fields.Field(
        column_name="weight", attribute="weight",
        widget=ForeignKeyWidget(Weight, "weight"),
    )
    grade = fields.Field(
        column_name="grade", attribute="grade",
        widget=ForeignKeyWidget(Grade, "code"),
    )
    section = fields.Field(
        column_name="section", attribute="section",
        widget=ForeignKeyWidget(Section, "name"),
    )
    term = fields.Field(
        column_name="term", attribute="term",
        widget=ForeignKeyWidget(Term, "name"),
    )

    class Meta:
        model = StudentAssessmentScore
        fields = (
            "id", "student", "grade", "section", "term",
            "academic_year", "subject", "weight",
            "raw_score", "weighted_score",
        )
        export_order = fields
        import_id_fields = ("id",)
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, row_number=None, **kwargs):
        raw = row.get("raw_score")
        if raw in (None, ""):
            return
        try:
            val = Decimal(str(raw))
        except (InvalidOperation, ValueError):
            raise ValueError(f"Row {row_number}: raw_score '{raw}' is not a number.")
        if val < 0:
            raise ValueError(f"Row {row_number}: raw_score cannot be negative.")
        if val > 100:
            raise ValueError(f"Row {row_number}: raw_score cannot exceed 100.")
@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ("id", "weight")
    search_fields = ("weight",)   # required for autocomplete_fields
    
# admin.py
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from import_export.admin import ImportExportMixin
from .forms import StudentAssessmentScoreForm
from .models import (
    StudentAssessmentScore, TeacherAssignment, TeacherAssignmentDetail,
)
from .resources import StudentAssessmentScoreResource


@admin.register(StudentAssessmentScore)
class StudentAssessmentScoreAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = StudentAssessmentScoreResource
    form = StudentAssessmentScoreForm

    list_display = (
        "student_name", "grade", "section", "term",
        "subject_name", "weight", "raw_score", "weighted_score",
    )
    list_display_links = ("student_name", "subject_name")
    list_editable = ("raw_score", "weighted_score")

    # THE single biggest admin speedup:
    list_select_related = (
        "student", "subject", "grade", "section",
        "term", "academic_year", "weight",
    )

    list_filter = (
        "weight", "subject", "grade", "section", "term", "academic_year",
    )

    search_fields = [
        "=student__Full_name",
        "student__Full_name_en",
        "subject__name",
        "grade__code",
        "term__name",
        "academic_year__year",
        "weight__weight",
    ]

    ordering = ("student__Full_name", "weight")
    list_per_page = 50

    autocomplete_fields = (
        "student_assessment", "student", "subject",
        "grade", "section", "term", "academic_year", "weight",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        assignment = (
            TeacherAssignment.objects
            .filter(assigned_to=request.user)
            .first()
        )
        if assignment is None:
            return qs.none()

        details = (
            TeacherAssignmentDetail.objects
            .filter(assignment=assignment, status="ACTIVE")
            .values_list("grade_id", "section_id", "subject_id")
        )
        q = Q()
        for grade_id, section_id, subject_id in details:
            q |= Q(
                student__New_grade=grade_id,
                student__New_section=section_id,
                subject=subject_id,
            )
        return qs.filter(q) if q else qs.none()

    @admin.display(description="Student")
    def student_name(self, obj):
        return obj.student.Full_name if obj.student else "(No Student)"

    @admin.display(description="Subject")
    def subject_name(self, obj):
        return obj.subject.name if obj.subject else "(No Subject)"

# ===== REGISTER NYALA FONT (MUST BE HERE) =====
NYALA_FONT_PATH = os.path.join(settings.BASE_DIR, 'fonts', 'Nyala.ttf')

if not os.path.exists(NYALA_FONT_PATH):
    raise FileNotFoundError(f"Nyala.ttf not found at {NYALA_FONT_PATH}")

pdfmetrics.registerFont(TTFont('Nyala', NYALA_FONT_PATH))

from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import StudentResultJSONView


@admin.register(StudentResultJSONView)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = (
        "colored_rank",
        "student_link",
        "gender_icon",
        "grade_badge",
        "section_badge",
        "semester",
        "colored_total",
        "colored_average",
        "result_status_badge",
    )
    list_display_links = ("student_link",)
    list_filter = ("academic_year", "grade", "section", "semester", "result_status")
    search_fields = ("=student_id", "student_name", "grade", "section")
    ordering = ("-academic_year", "student_id", "semester")
    list_per_page = 25
    show_full_result_count = False
    empty_value_display = "—"
    readonly_fields = [f.name for f in StudentResultJSONView._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    actions = (
        "print_student_result_pdf",
        "print_student_result_rank_pdf",
        "print_student_roster_pdf",
        "print_individual_student_result_pdf",
    )

    # ---- changelist columns (all use mark_safe, never format_html) ----

    @admin.display(description="#", ordering="rank")
    def colored_rank(self, obj):
        if obj.rank is None:
            return "—"
        if obj.rank <= 3:
            color, bg = "#1a7f37", "#e6f4ea"
        elif obj.rank <= 10:
            color, bg = "#8a6d00", "#fff8e1"
        else:
            color, bg = "#444444", "#f3f4f6"
        return mark_safe(
            f'<span style="display:inline-block;min-width:2em;padding:2px 8px;'
            f'border-radius:10px;font-weight:600;color:{color};background:{bg};">'
            f'{obj.rank}</span>'
        )

    @admin.display(description="Student", ordering="student_name")
    def student_link(self, obj):
        return mark_safe(
            f'<strong>{obj.student_name}</strong> '
            f'<span style="color:#888888;font-size:0.85em;">#{obj.student_id}</span>'
        )

    @admin.display(description="G", ordering="gender")
    def gender_icon(self, obj):
        val = (obj.gender or "").strip().lower()
        if val in ("f", "female", "ሴት"):
            return mark_safe('<span title="Female" style="color:#c026d3;">♀</span>')
        if val in ("m", "male", "ወንድ"):
            return mark_safe('<span title="Male" style="color:#2563eb;">♂</span>')
        return "—"

    @admin.display(description="Grade", ordering="grade")
    def grade_badge(self, obj):
        return mark_safe(
            f'<span style="padding:1px 8px;border-radius:4px;'
            f'background:#eef2ff;color:#3730a3;font-weight:600;">'
            f'{obj.grade or "—"}</span>'
        )

    @admin.display(description="Section", ordering="section")
    def section_badge(self, obj):
        return mark_safe(
            f'<span style="padding:1px 8px;border-radius:4px;'
            f'background:#ecfeff;color:#155e75;font-weight:600;">'
            f'{obj.section or "—"}</span>'
        )

    @admin.display(description="Total", ordering="total")
    def colored_total(self, obj):
        if obj.total is None:
            return "—"
        color = "#1a7f37" if obj.total >= 50 else "#b91c1c"
        return mark_safe(
            f'<span style="font-weight:600;color:{color};">{obj.total}</span>'
        )

    @admin.display(description="Average", ordering="average")
    def colored_average(self, obj):
        if obj.average is None:
            return "—"
        avg = float(obj.average)
        color = "#1a7f37" if avg >= 50 else "#b91c1c"
        return mark_safe(
            f'<span style="font-weight:600;color:{color};">{avg:.2f}</span>'
        )

    @admin.display(description="Status", ordering="result_status")
    def result_status_badge(self, obj):
        s = obj.result_status or ""
        if "ተዛዉ" in s:
            color, bg = "#1a7f37", "#e6f4ea"
        elif "አልተዛ" in s:
            color, bg = "#b91c1c", "#fdecec"
        else:
            color, bg = "#444444", "#f3f4f6"
        return mark_safe(
            f'<span style="padding:2px 10px;border-radius:10px;'
            f'font-size:0.85em;font-weight:600;color:{color};background:{bg};">'
            f'{s or "—"}</span>'
        )

    # ---- detail page ----

    fieldsets = (
        ("Student", {
            "fields": (
                ("student_id", "student_name"),
                ("gender", "age"),
                ("grade", "section"),
                ("section_head",),
            ),
        }),
        ("Report", {
            "fields": (
                ("academic_year", "semester"),
                ("display_subjects",),
            ),
        }),
        ("Scores", {
            "fields": (
                ("total", "average"),
                ("rank", "yearly_rank"),
                ("result_status",),
                ("discipline",),
            ),
        }),
        ("Metadata", {
            "classes": ("collapse",),
            "fields": (
                ("report_title", "report_date"),
                ("archive_officer_name", "school_director_name"),
                ("id",),
            ),
        }),
    )

    @admin.display(description="Subjects & Scores")
    def display_subjects(self, obj):
        if not obj.subjects:
            return "—"
        rows = "".join(
            f'<tr>'
            f'<td style="padding:4px 10px;border-bottom:1px solid #eeeeee;">{k}</td>'
            f'<td style="padding:4px 10px;border-bottom:1px solid #eeeeee;'
            f'text-align:right;font-weight:600;">{v}</td>'
            f'</tr>'
            for k, v in obj.subjects.items()
        )
        return mark_safe(
            f'<table style="border-collapse:collapse;min-width:260px;">'
            f'<thead><tr>'
            f'<th style="text-align:left;padding:6px 10px;border-bottom:2px solid #dddddd;">Subject</th>'
            f'<th style="text-align:right;padding:6px 10px;border-bottom:2px solid #dddddd;">Score</th>'
            f'</tr></thead>'
            f'<tbody>{rows}</tbody>'
            f'</table>'
        )

    def get_fields(self, request, obj=None):
        if obj is not None:
            fields = [f for f in super().get_fields(request, obj) if f != "subjects"]
            fields.append("display_subjects")
            return fields
        return super().get_fields(request, obj)
    
    def print_student_result_rank_pdf(modeladmin, request, queryset):
        from django.http import HttpResponse
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.pdfgen import canvas
        from reportlab.platypus import Table, TableStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="student_results.pdf"'

        c = canvas.Canvas(response, pagesize=landscape(A4))
        width, height = landscape(A4)

        ROWS_PER_PAGE = 56
        TOP_MARGIN = 1.2 * cm  # Reduced to fit everything
        BOTTOM_MARGIN = 1.0 * cm  # Reduced
        LEFT_MARGIN = 0.5 * cm  # Reduced
        RIGHT_MARGIN = 0.5 * cm  # Reduced
        
        # Calculate available width for the table
        available_width = width - LEFT_MARGIN - RIGHT_MARGIN

        # queryset = queryset.order_by("grade", "section")
        queryset = queryset.order_by("grade", "section", "student_name")

        grouped = {}
        for row in queryset:
            grouped.setdefault((row.grade, row.section), []).append(row)

        for (grade, section), students in grouped.items():
            # Sort by name. We use .lower() to ensure 'A' and 'a' are treated the same.
            students = sorted(students, key=lambda x: (x.student_name or "").lower())
            roll_no = 1
            y = height - TOP_MARGIN
            first = students[0]

            # ---------- TITLE ----------
            title = first.report_title
            c.setFont("Nyala", 14)  # Reduced from 14
            c.drawCentredString(width / 2, y, title)

            title_width = c.stringWidth(title, "Nyala", 14)
            underline_y = y - 0.1 * cm
            c.line(
                (width - title_width) / 2,
                underline_y,
                (width + title_width) / 2,
                underline_y
            )

            y -= 0.6 * cm  # Reduced spacing


            # ---------- SUBTITLE ----------
            subtitle = "የተማሪዎች መረጃ እና ማርክ ማጠራቀሚያ ቅጽ"
            c.setFont("Nyala", 11)  # Reduced from 11
            c.drawCentredString(width / 2, y, subtitle)

            subtitle_width = c.stringWidth(subtitle, "Nyala", 11)
            underline_y = y - 0.1 * cm
            c.line(
                (width - subtitle_width) / 2,
                underline_y,
                (width + subtitle_width) / 2,
                underline_y
            )

            y -= 0.6 * cm  # Reduced from 1 cm


            # ---------- METADATA IN 2 LINES ----------
            metadata_data = [
                # Line 1: ክፍል, ሴክሽን, ሰሚስተር, የት/ዘመን
                [
                    "ክፍል:", str(grade),
                    "ሴክሽን:", str(section),
                    "ሰሚስተር:", str(first.semester),
                    "የት/ዘመን:", str(first.academic_year or "")
                ],
                # Line 2: የክፍል ኃላፊ, የመዘክር ክፍል ኃላፊ, የት/ቤቱ ር/መ/ር, ቀን
                [
                    "የክፍል ኃላፊ:", str(first.section_head or ""),
                    "የመዘክር ክፍል ኃላፊ:", str(first.archive_officer_name or ""),
                    "የት/ቤቱ ር/መ/ር:", str(first.school_director_name or ""),
                    "ቀን:", str(first.report_date or "")
                ],
            ]

            # Use 8 columns (4 label-value pairs)
            metadata_table = Table(metadata_data, colWidths=[2*cm, 3*cm, 2*cm, 3*cm, 2*cm, 3*cm, 2*cm, 3*cm])
            metadata_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reduced from 9
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 1),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black),
            ]))

            w, h = metadata_table.wrapOn(c, width, y)
            metadata_table.drawOn(c, LEFT_MARGIN, y - h)
            y -= h + 0.2 * cm  # Reduced spacing

            # ---------- TABLE DATA ----------
            subjects = first.subjects or {}
            headers = ["#", "ሙሉ ስም", "ጾታ", "እድሜ"] + list(subjects.keys()) + ["ድምር", "አማካኝ", "ደረጃ", "ጸባይ"]
            table_data = [headers]

            for row in students:
                table_data.append([
                    roll_no,
                    row.student_name,
                    row.gender,
                    row.age or "",
                    *list((row.subjects or {}).values()),
                    row.total or "",
                    f"{row.average:.2f}" if row.average is not None else "",
                    row.rank or "",
                    row.discipline or "",
                ])
                roll_no += 1

            # Fill remaining rows if less than ROWS_PER_PAGE
            while len(table_data) < ROWS_PER_PAGE + 1:
                table_data.append([""] * len(headers))

            # ---------- ROW HEIGHTS ----------
            TOTAL_ROWS = len(table_data)
            available_height = y - BOTTOM_MARGIN
            
            # Calculate height more precisely
            max_rows_per_page = ROWS_PER_PAGE + 1  # +1 for header
            body_height = available_height / max_rows_per_page
            header_height = body_height * 1.2  # Slightly taller header
            
            row_heights = [header_height] + [body_height] * (TOTAL_ROWS - 1)

            # ---------- DYNAMIC COLUMN WIDTHS ----------
            # Count columns
            fixed_cols = 5  # #, ሙሉ ስም, ጾታ, እድሜ
            subject_cols = len(subjects)
            footer_cols = 4  # ድምር, አማካኝ, ደረጃ, ጸባይ
            total_cols = fixed_cols + subject_cols + footer_cols
            
            # Minimum widths (adjusted for longer names)
            min_fixed_width = 0.8 * cm  # Base width for small columns
            min_subject_width = 1.4 * cm  # Width for subject columns
            min_footer_width = 1.0 * cm  # Width for footer columns
            
            # Calculate total minimum width
            total_min_width = (
                fixed_cols * min_fixed_width +
                subject_cols * min_subject_width +
                footer_cols * min_footer_width
            )
            
            # ADD EXTRA WIDTH FOR FULL NAME COLUMN
            # Reserve additional width for the full name column to accommodate long names
            name_column_extra_width = 2.5 * cm  # Increase by 2.5 cm for full names
            
            # Add the extra width to the total minimum width
            total_min_width += name_column_extra_width
            
            # Scale down if needed
            if total_min_width > available_width:
                scale_factor = available_width / total_min_width
                min_fixed_width *= scale_factor
                min_subject_width *= scale_factor
                min_footer_width *= scale_factor
                # Scale down the extra width as well
                name_column_extra_width *= scale_factor
            
            # Set column widths with adjustments
            col_widths = []
            
            # Fixed columns
            col_widths.append(min_fixed_width * 0.8)  # Serial number (slightly smaller)
            col_widths.append((min_fixed_width * 4) + name_column_extra_width)  # Full name - INCREASED by extra width
            col_widths.append(min_fixed_width * 0.9)  # Gender
            col_widths.append(min_fixed_width * 0.8)  # Age
            
            # Subject columns
            col_widths.extend([min_subject_width] * subject_cols)
            
            # Footer columns
            col_widths.append(min_footer_width)      # ድምር
            col_widths.append(min_footer_width)      # አማካኝ
            col_widths.append(min_footer_width)      # ደረጃ
            col_widths.append(min_footer_width * 0.8) # ጸባይ
            
            # Final adjustment to ensure it fits
            total_width = sum(col_widths)
            if total_width > available_width:
                # If still too wide, reduce other columns proportionally
                scale = available_width / total_width
                col_widths = [w * scale for w in col_widths]

            # ---------- DRAW TABLE ----------
            student_table = Table(
                table_data,
                colWidths=col_widths,
                rowHeights=row_heights
            )

            student_table.setStyle(TableStyle([
                # Header
                ('FONTNAME', (0, 0), (-1, 0), 'Nyala'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, 0), 4),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 2),

                # Body
                ('FONTNAME', (0, 1), (-1, -1), 'Nyala'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
                
                # Special alignment for full name column (left align for better readability)
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('LEFTPADDING', (1, 0), (1, -1), 3),

                # Grid
                ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
            ]))

            w, h = student_table.wrapOn(c, width, y)
            
            # Check if table fits - if not, reduce font size further
            if y - h < BOTTOM_MARGIN:
                # Try with even smaller font
                student_table.setStyle(TableStyle([
                    # Header with smaller font
                    ('FONTNAME', (0, 0), (-1, 0), 'Nyala'),
                    ('FONTSIZE', (0, 0), (-1, 0), 7),  # Reduced to 7
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, 0), 1),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 1),

                    # Body with smaller font
                    ('FONTNAME', (0, 1), (-1, -1), 'Nyala'),
                    ('FONTSIZE', (0, 1), (-1, -1), 7),  # Reduced to 7
                    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
                    
                    # Special alignment for full name column
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('LEFTPADDING', (1, 0), (1, -1), 3),

                    # Grid
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                ]))
                
                # Recalculate height with smaller font
                w, h = student_table.wrapOn(c, width, y)
            
            # Draw the table
            student_table.drawOn(c, LEFT_MARGIN, y - h)

            c.showPage()

        c.save()
        return response

    print_student_result_rank_pdf.short_description = "Print Student Mark List (PDF)"

    # print_student_roster_pdf.short_description = "Print Student Roster (PDF)"
    from reportlab.lib.pagesizes import landscape, A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Table, TableStyle
    from django.http import HttpResponse
    import math

    def print_student_roster_pdf(modeladmin, request, queryset):
        from django.http import HttpResponse
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.pdfgen import canvas
        from reportlab.platypus import Table, TableStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from collections import defaultdict

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="student_results_report.pdf"'

        c = canvas.Canvas(response, pagesize=landscape(A4))
        width, height = landscape(A4)

        STUDENTS_PER_PAGE = 8
        ROWS_PER_STUDENT = 7
        TOP_MARGIN = 1.8 * cm
        LEFT_MARGIN = 0.5 * cm
        RIGHT_MARGIN = 0.4 * cm
        SEMESTER_LABELS = ["Q1", "Q2", "S1", "Q3", "Q4", "S2", "Av."]
        TERM_LABELS = ["Term one", "Term two", "Term three", "Term four"]

        available_width = width - LEFT_MARGIN - RIGHT_MARGIN

        # ---------- helpers ----------
        def to_num(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return None

        def avg_num(vals):
            nums = [to_num(v) for v in vals if to_num(v) is not None]
            return round(sum(nums) / len(nums), 2) if nums else None

        def avg_dict(dicts):
            acc, counts = {}, {}
            for d in dicts:
                if not d:
                    continue
                for k, v in d.items():
                    n = to_num(v)
                    if n is None:
                        continue
                    acc[k] = acc.get(k, 0.0) + n
                    counts[k] = counts.get(k, 0) + 1
            return {k: round(acc[k] / counts[k], 2) for k in acc}

        def competition_rank(values_by_id, descending=True):
            """Standard competition ranking (1,2,2,4) like Excel RANK().
            values_by_id: dict {student_id: numeric or None}
            Returns {student_id: rank_int}
            """
            pairs = [(sid, v) for sid, v in values_by_id.items() if v is not None]
            if not pairs:
                return {}
            pairs.sort(key=lambda kv: kv[1], reverse=descending)
            ranks, prev_val, prev_rank = {}, None, 0
            for idx, (sid, val) in enumerate(pairs, start=1):
                if prev_val is not None and val == prev_val:
                    ranks[sid] = prev_rank            # tie -> same rank
                else:
                    ranks[sid] = idx
                    prev_rank = idx
                prev_val = val
            return ranks

        def g(row, attr, default=""):
            if row is None:
                return default
            return getattr(row, attr, default) or default

        def fmt2(v):
            f = to_num(v)
            return f"{f:.2f}" if f is not None else ""

        # ---------- load & group ----------
        queryset = queryset.order_by("grade", "section", "student_name", "semester")

        grouped = defaultdict(lambda: defaultdict(dict))
        for row in queryset:
            key = (row.grade, row.section)
            grouped[key][row.student_id][row.semester] = row

        # ---------- pre-compute S1/S2/Av ranks per (grade, section) ----------
        # Structure: derived[(grade, section)][student_id] = dict of derived values
        derived = defaultdict(dict)

        for key, students_map in grouped.items():
            s1_avgs, s2_avgs, av_avgs = {}, {}, {}

            for sid, terms in students_map.items():
                q1 = terms.get("Term one")
                q2 = terms.get("Term two")
                q3 = terms.get("Term three")
                q4 = terms.get("Term four")
                anchor = q1 or q2 or q3 or q4
                if not anchor:
                    continue

                s1_subj = avg_dict([q1.subjects if q1 else None,
                                    q2.subjects if q2 else None])
                s2_subj = avg_dict([q3.subjects if q3 else None,
                                    q4.subjects if q4 else None])
                av_subj = avg_dict([s1_subj, s2_subj])

                s1_total = avg_num([g(q1, "total", None), g(q2, "total", None)])
                s1_avg   = avg_num([g(q1, "average", None), g(q2, "average", None)])
                s2_total = avg_num([g(q3, "total", None), g(q4, "total", None)])
                s2_avg   = avg_num([g(q3, "average", None), g(q4, "average", None)])
                av_total = avg_num([s1_total, s2_total])
                av_avg   = avg_num([s1_avg, s2_avg])

                derived[key][sid] = {
                    "s1_subj": s1_subj, "s2_subj": s2_subj, "av_subj": av_subj,
                    "s1_total": s1_total, "s1_avg": s1_avg,
                    "s2_total": s2_total, "s2_avg": s2_avg,
                    "av_total": av_total, "av_avg": av_avg,
                    "anchor": anchor,
                }

                s1_avgs[sid] = s1_avg
                s2_avgs[sid] = s2_avg
                av_avgs[sid] = av_avg

            # Compute competition ranks across the WHOLE class (not per page)
            s1_ranks = competition_rank(s1_avgs)
            s2_ranks = competition_rank(s2_avgs)
            av_ranks = competition_rank(av_avgs)

            for sid, d in derived[key].items():
                d["s1_rank"] = s1_ranks.get(sid)
                d["s2_rank"] = s2_ranks.get(sid)
                # Prefer YEARLY_RANK from the DB if present, else computed rank
                db_yearly = g(d["anchor"], "YEARLY_RANK", None)
                d["av_rank"] = db_yearly if db_yearly else av_ranks.get(sid)

        # ---------- render ----------
        for (grade, section), students_map in grouped.items():
            student_ids = sorted(
                students_map.keys(),
                key=lambda sid: (students_map[sid].get("Term one").student_name or "").lower()
                if students_map[sid].get("Term one") else ""
            )

            for page_start in range(0, len(student_ids), STUDENTS_PER_PAGE):
                page_ids = student_ids[page_start:page_start + STUDENTS_PER_PAGE]
                y = height - TOP_MARGIN

                first = students_map[page_ids[0]].get("Term one")
                if not first:
                    continue

                # ---- TITLE ----
                title = first.report_title or "የተማሪዎች ውጤት መግለጫ ሮስተር"
                full_title = f"{title} - የተማሪዎች ውጤት መግለጫ ሮስተር"
                c.setFont("Nyala", 9)
                c.drawCentredString(width / 2, y, full_title)
                tw = c.stringWidth(full_title, "Nyala", 9)
                c.line((width - tw) / 2, y - 0.15 * cm, (width + tw) / 2, y - 0.15 * cm)
                y -= 0.45 * cm

                # ---- HEADER ----
                header_data = [[
                    "የክፍል ደረጃ", str(grade),
                    "ሴክሽን", str(section),
                    "የት/ዘመን", str(first.academic_year or ""),
                ]]
                ht = Table(header_data, colWidths=[3 * cm] * 6)
                ht.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('TOPPADDING', (0, 0), (-1, -1), 1),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                    ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
                ]))
                w, h = ht.wrapOn(c, width, y)
                ht.drawOn(c, LEFT_MARGIN, y - h)
                y -= h + 0.2 * cm

                # ---- COLUMNS ----
                fixed_headers = ["ተ/ቁ", "መ.ቁ", "ሙሉ ስም", "ጾታ", "እድሜ", "ሰሚስተር"]
                subject_headers = list((first.subjects or {}).keys())
                footer_headers = ["ድምር", "አማካኝ", "ደረጃ", "ጸባይ", "የቀሩ ቀናት", "ምርመራ"]

                headers = fixed_headers + subject_headers + footer_headers
                table_data = [headers]

                n_fixed, n_subj, n_foot = len(fixed_headers), len(subject_headers), len(footer_headers)
                total_columns = n_fixed + n_subj + n_foot

                min_fixed, min_subj, min_foot = 0.7 * cm, 1.1 * cm, 1.0 * cm
                total_min = n_fixed * min_fixed + n_subj * min_subj + n_foot * min_foot
                if total_min > available_width:
                    s = available_width / total_min
                    min_fixed, min_subj, min_foot = min_fixed * s, min_subj * s, min_foot * s

                fixed_widths = [min_fixed, min_fixed, min_fixed * 4.0,
                                min_fixed, min_fixed, min_fixed * 1.2]
                subject_widths = [min_subj] * n_subj
                footer_widths = []
                for hdr in footer_headers:
                    if hdr == "ምርመራ":
                        footer_widths.append(min_foot * 1.6)
                    elif hdr == "የቀሩ ቀናት":
                        footer_widths.append(min_foot * 1.0)
                    elif hdr == "ጸባይ":
                        footer_widths.append(min_foot * 0.7)
                    else:
                        footer_widths.append(min_foot)

                col_widths = fixed_widths + subject_widths + footer_widths
                tot = sum(col_widths)
                if tot > available_width:
                    k = available_width / tot
                    col_widths = [wv * k for wv in col_widths]

                # ---- STUDENT ROWS ----
                roll_no = page_start + 1
                for sid in page_ids:
                    terms = students_map[sid]
                    d = derived[(grade, section)].get(sid)
                    if not d:
                        continue

                    q1 = terms.get("Term one")
                    q2 = terms.get("Term two")
                    q3 = terms.get("Term three")
                    q4 = terms.get("Term four")
                    anchor = d["anchor"]
                    gender_disp = {"Male": "ወ", "Female": "ሴ"}.get(anchor.gender, anchor.gender or "")

                    display_rows = [
                        ("Q1", q1.subjects if q1 else {}, g(q1, "total"), g(q1, "average"),
                        g(q1, "rank"), g(q1, "discipline"), ""),
                        ("Q2", q2.subjects if q2 else {}, g(q2, "total"), g(q2, "average"),
                        g(q2, "rank"), g(q2, "discipline"), ""),
                        ("S1", d["s1_subj"], d["s1_total"], d["s1_avg"],
                        d["s1_rank"], "", ""),                       # ✅ S1 rank
                        ("Q3", q3.subjects if q3 else {}, g(q3, "total"), g(q3, "average"),
                        g(q3, "rank"), g(q3, "discipline"), ""),
                        ("Q4", q4.subjects if q4 else {}, g(q4, "total"), g(q4, "average"),
                        g(q4, "rank"), g(q4, "discipline"), ""),
                        ("S2", d["s2_subj"], d["s2_total"], d["s2_avg"],
                        d["s2_rank"], "", ""),                       # ✅ S2 rank
                        ("Av.", d["av_subj"], d["av_total"], d["av_avg"],
                        d["av_rank"], "", g(anchor, "result_status")),  # ✅ Av. rank
                    ]

                    for i, (label, subj_dict, tot_v, avg_v, rnk, conduct, remark) in \
                            enumerate(display_rows):
                        data_row = [
                            str(roll_no) if i == 0 else "",
                            str(anchor.student_id) if i == 0 else "",
                            anchor.student_name if i == 0 else "",
                            gender_disp if i == 0 else "",
                            str(anchor.age or "") if i == 0 else "",
                            label,
                        ]
                        for subj in subject_headers:
                            data_row.append(str(subj_dict.get(subj, "") or ""))
                        data_row.extend([
                            str(tot_v or ""),
                            fmt2(avg_v),
                            str(rnk or ""),
                            str(conduct or ""),
                            "",
                            str(remark or ""),
                        ])
                        table_data.append(data_row)

                    roll_no += 1

                student_table = Table(table_data, colWidths=col_widths, repeatRows=1)

                style = [
                    ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
                    ('FONTSIZE', (0, 0), (-1, -1), 6.5),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('TOPPADDING', (0, 0), (-1, -1), 0.8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0.8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 1),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 1),
                    ('ALIGN', (2, 1), (2, -1), 'LEFT'),
                ]

                last_col_idx = total_columns - 1
                for i in range(len(page_ids)):
                    r1 = 1 + i * ROWS_PER_STUDENT
                    r2 = r1 + ROWS_PER_STUDENT - 1
                    for col_idx in (0, 1, 2, 3, 4):
                        style.append(('SPAN', (col_idx, r1), (col_idx, r2)))
                    style.append(('SPAN', (last_col_idx, r1), (last_col_idx, r2)))

                student_table.setStyle(TableStyle(style))

                w, h = student_table.wrapOn(c, width, y)
                if y - h < 4.2 * cm:
                    c.showPage()
                    y = height - TOP_MARGIN
                    c.setFont("Nyala", 9)
                    c.drawCentredString(width / 2, y, full_title)
                    c.line((width - tw) / 2, y - 0.15 * cm, (width + tw) / 2, y - 0.15 * cm)
                    y -= 0.45 * cm
                    w, h = student_table.wrapOn(c, width, y)

                student_table.drawOn(c, LEFT_MARGIN, y - h)
                y -= h + 0.4 * cm

                # ---- FOOTER ----
                footer_student = students_map[page_ids[0]].get("Term one")
                footer_headers_data = [[
                    "ሰሚስተር", "የክፍል ኃላፊ ስም", "ፊርማ",
                    "የመዘክር ክፍል ኃላፊ ስም", "ፊርማ",
                    "የት/ቤቱ ር/መ/ር ስም", "ፊርማ",
                ]]
                fw = [
                    1.5 * cm, 4.0 * cm, 2.0 * cm, 3.5 * cm,
                    2.0 * cm, 4.0 * cm, 1.5 * cm,
                    available_width - (1.5 + 4 + 2 + 2.5 + 2 + 4 + 1.5) * cm,
                ]
                ft_h = Table(footer_headers_data, colWidths=fw)
                ft_h.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 1),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                    ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                w, h = ft_h.wrapOn(c, width, y)
                ft_h.drawOn(c, LEFT_MARGIN, y - h)
                y -= h + 0.1 * cm

                for sem_label in ("1ኛ", "2ኛ"):
                    data = [[
                        f"{sem_label}  ",
                        str(footer_student.section_head or ""), "___________",
                        str(footer_student.archive_officer_name or ""), "_____________",
                        str(footer_student.school_director_name or ""), "___________",
                        "የት/ቤቱ ማህተም" if sem_label == "2ኛ" else "",
                    ]]
                    ft = Table(data, colWidths=fw)
                    ft.setStyle(TableStyle([
                        ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('TOPPADDING', (0, 0), (-1, -1), 1),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                        ('LINEBELOW', (1, 0), (1, 0), 0.5, colors.black),
                        ('LINEBELOW', (3, 0), (3, 0), 0.5, colors.black),
                        ('LINEBELOW', (5, 0), (5, 0), 0.5, colors.black),
                    ]))
                    w, h = ft.wrapOn(c, width, y)
                    ft.drawOn(c, LEFT_MARGIN, y - h)
                    y -= h + 0.1 * cm

                if page_start + STUDENTS_PER_PAGE < len(student_ids):
                    c.showPage()

        c.save()
        return response


    print_student_roster_pdf.short_description = "Print Student Roster (PDF)"
    
    def print_individual_student_result_pdf(modeladmin, request, queryset):
        """
        Django admin action: generate individual student report cards (PDF).
        """
        from django.http import HttpResponse
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.pdfgen import canvas
        from reportlab.platypus import Table, TableStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.lib.utils import ImageReader
        from collections import defaultdict
        import os

        # ---------- resolve logo path ----------
        try:
            from django.conf import settings
            LOGO_PATH = os.path.join(settings.BASE_DIR, "static", "images", "my_logo.png")
        except Exception:
            LOGO_PATH = r"D:\projects\kings\static\images\my_logo.png"
        if not os.path.exists(LOGO_PATH):
            LOGO_PATH = r"D:\projects\kings\static\images\my_logo.png"

        LOGO_SIZE = 1.6 * cm

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="student_report_cards.pdf"'

        c = canvas.Canvas(response, pagesize=landscape(A4))
        width, height = landscape(A4)

        LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN = 1.0*cm, 1.0*cm, 1.0*cm

        PD_TRAITS = [
            "Reading", "Writing", "Spelling", "Comprehension", "Computation Skill",
            "Punctuality", "Uniform", "Material Handling", "Following Directions",
            "Assignment Completion", "English Use", "Work Ethics",
            "Communication with others", "Overall Progress",
        ]

        # ---------- helpers ----------
        def fmt_num(v, nd=2):
            if v is None or v == "":
                return ""
            try:
                f = float(v)
                return f"{f:.{nd}f}".rstrip('0').rstrip('.') if f % 1 else f"{int(f)}"
            except (TypeError, ValueError):
                return str(v)

        def compute_ranks(values):
            indexed = [(i, v) for i, v in values
                    if isinstance(v, (int, float)) and v > 0]
            indexed.sort(key=lambda t: t[1], reverse=True)
            return {i: rank for rank, (i, _) in enumerate(indexed, 1)}

        def get_auto_remark(average, gender):
            g = (gender or "").strip().lower()
            suf = "ዋ" if g == "female" else "ው"
            a = float(average or 0)
            if a < 50:
                return (f"ውጤቱ{suf} ዝቅተኛ ስለሆነ ይህን ለማሻሻል የወላጅ ድጋፍ አይለይ{suf}።")
            if a < 70:
                return (f"ውጤቱ{suf} አጥጋቢ ቢሆንም ይህን ለማሻሻል የወላጅ ድጋፍ አይለይ{suf}።")
            if a < 80:
                return (f"ውጤቱ{suf} ጥሩ ቢሆንም ከዚህ የተሻለ ውጤት ለማምጣት የወላጅ ድጋፍ አይለይ{suf}።")
            if a < 90:
                return (f"ውጤቱ{suf} በጣም ጥሩ ቢሆንም ከዚህ የተሻለ ውጤት ለማምጣት የወላጅ ድጋፍና ክትትል አይለይ{suf}።")
            return (f"ውጤቱ{suf} እጅግ በጣም ጥሩ ስለሆነ ይህን አስጠብቆ የተሻለ ውጤት ለማምጣት የወላጅ ድጋፍና ክትትል አይለይ{suf}።")

        def draw_title(c, x_center, y, text, font_size=10):
            c.setFont("Nyala", font_size)
            c.setFillColor(colors.black)
            c.drawCentredString(x_center, y, text)
            tw = c.stringWidth(text, "Nyala", font_size)
            c.setLineWidth(0.6)
            c.line(x_center - tw/2, y - 2, x_center + tw/2, y - 2)

        def draw_logos(c):
            if not os.path.exists(LOGO_PATH):
                return
            try:
                img = ImageReader(LOGO_PATH)
                y_top = height - TOP_MARGIN - LOGO_SIZE
                c.drawImage(img, LEFT_MARGIN, y_top,
                            width=LOGO_SIZE, height=LOGO_SIZE,
                            mask='auto', preserveAspectRatio=True)
                c.drawImage(img, width - RIGHT_MARGIN - LOGO_SIZE, y_top,
                            width=LOGO_SIZE, height=LOGO_SIZE,
                            mask='auto', preserveAspectRatio=True)
            except Exception:
                pass

        SEM_MAP = {
            "term one":"Q1","term two":"Q2","term three":"Q3","term four":"Q4",
            "term 1":"Q1","term 2":"Q2","term 3":"Q3","term 4":"Q4",
            "q1":"Q1","q2":"Q2","q3":"Q3","q4":"Q4",
            "quarter one":"Q1","quarter two":"Q2","quarter three":"Q3","quarter four":"Q4",
            "semester one":"Q1","semester two":"Q2","semester three":"Q3","semester four":"Q4",
        }
        def sem_to_q(sem): return SEM_MAP.get((sem or "").strip().lower())

        grouped = defaultdict(list)
        for row in queryset:
            grouped[row.student_id].append(row)

        # ---------- pre-compute ranks ----------
        q_rank_inputs = {q: [] for q in ("Q1","Q2","Q3","Q4")}
        for sid, rows in grouped.items():
            for r in rows:
                q = sem_to_q(r.semester)
                if q:
                    q_rank_inputs[q].append((sid, float(getattr(r, "average", 0) or 0)))
        q_ranks = {q: compute_ranks(q_rank_inputs[q]) for q in q_rank_inputs}

        annual_rank_inputs = []
        for sid, rows in grouped.items():
            annual_row = None
            for r in rows:
                if sem_to_q(r.semester) == "Q4":
                    annual_row = r; break
            if annual_row is None:
                for r in rows:
                    if sem_to_q(r.semester) in ("Q3","Q2","Q1"):
                        annual_row = r; break
            if annual_row is None:
                annual_row = rows[0]
            yr = getattr(annual_row, "YEARLY_RANK", None)
            if yr not in (None, "", 0):
                annual_rank_inputs.append((sid, float(yr), True))
            else:
                annual_rank_inputs.append(
                    (sid, float(getattr(annual_row, "average", 0) or 0), False)
                )
        explicit_annual_ranks, computable = {}, []
        for sid, val, is_rank in annual_rank_inputs:
            if is_rank:
                explicit_annual_ranks[sid] = int(val)
            else:
                computable.append((sid, val))
        computed_annual_ranks = compute_ranks(computable)
        def annual_rank_of(sid):
            return explicit_annual_ranks.get(sid,
                    computed_annual_ranks.get(sid, ""))

        all_subjects, seen = [], set()
        for rows in grouped.values():
            for r in rows:
                for s in (r.subjects or {}):
                    if s not in seen:
                        seen.add(s); all_subjects.append(s)

        # ================= per-student =================
        for idx, (sid, rows) in enumerate(grouped.items()):
            y = height - TOP_MARGIN

            base            = rows[0]
            gender          = base.gender or ""
            age             = base.age or ""
            academic_year   = base.academic_year or ""
            grade           = base.grade or ""
            section         = base.section or ""
            student_name    = base.student_name or ""

            quarter_rows = {}
            for r in rows:
                q = sem_to_q(r.semester)
                if q: quarter_rows[q] = r
            annual_row = (quarter_rows.get("Q4") or quarter_rows.get("Q3")
                        or quarter_rows.get("Q2") or quarter_rows.get("Q1")
                        or base)

            def sc(r): return (r.subjects if r else {}) or {}
            def v(r, f, d=""): return getattr(r, f, d) if r else d

            # ---------- logos ----------
            draw_logos(c)
            y -= LOGO_SIZE + 0.2*cm

            # ============================================================
            # TABLE 1: MARKS
            # ============================================================
            title_line = (f"King's Academy   ·   Student's Report Card   ·   "
                        f"Grade: {grade}    Section: {section}   ·   "
                        f"Academic Yr.: {academic_year}")
            draw_title(c, width/2, y, title_line, font_size=11)
            y -= 0.45*cm

            headers = ["No", "Name", "Sex", "Age", "Sem."] + \
                    all_subjects + ["Total", "Average", "Rank", "Conduct", "Days-Abs", "Remark"]

            n_subj = len(all_subjects)
            table_width = width - LEFT_MARGIN - RIGHT_MARGIN
            no_w, name_w, sex_w, age_w, sem_w = 0.9*cm, 4.2*cm, 1.0*cm, 0.9*cm, 1.2*cm
            summary_w, remark_w = 1.4*cm, 2.6*cm
            used_w = (no_w + name_w + sex_w + age_w + sem_w
                    + 5*summary_w + remark_w)
            subj_w = max(0.8*cm, (table_width - used_w) / max(n_subj, 1))
            col_widths = ([no_w, name_w, sex_w, age_w, sem_w]
                        + [subj_w]*n_subj
                        + [summary_w]*5 + [remark_w])

            def build_row(label, r, score_dict=None, rank_val=""):
                scores = score_dict if score_dict is not None else sc(r)
                row = [str(sid), student_name, gender, str(age), label]
                for subj in all_subjects:
                    sc_v = scores.get(subj, "")
                    row.append(fmt_num(sc_v) if isinstance(sc_v, (int, float)) else str(sc_v))
                row.extend([
                    fmt_num(v(r, "total")) if r else "",
                    fmt_num(v(r, "average")) if r else "",
                    str(rank_val or ""),
                    str(v(r, "discipline") or ""),
                    str(v(r, "days_abs") or ""),
                    "",
                ])
                return row

            def merge_scores(a, b):
                out = {}
                for subj in all_subjects:
                    nums = [float(x) for x in (sc(a).get(subj), sc(b).get(subj))
                            if isinstance(x, (int, float))]
                    out[subj] = (sum(nums)/len(nums)) if nums else ""
                return out
            def merge_total(a, b):
                return float(v(a, "total", 0) or 0) + float(v(b, "total", 0) or 0)
            def merge_avg(a, b):
                nums = [x for x in (float(v(a, "average", 0) or 0),
                                    float(v(b, "average", 0) or 0)) if x]
                return sum(nums)/len(nums) if nums else 0

            rq1, rq2 = quarter_rows.get("Q1"), quarter_rows.get("Q2")
            rq3, rq4 = quarter_rows.get("Q3"), quarter_rows.get("Q4")

            class _F:
                def __init__(self, scores, total, avg):
                    self.subjects, self.total, self.average = scores, total, avg
                    self.discipline, self.days_abs = "", ""
            s1_fake = _F(merge_scores(rq1, rq2), merge_total(rq1, rq2), merge_avg(rq1, rq2))
            s2_fake = _F(merge_scores(rq3, rq4), merge_total(rq3, rq4), merge_avg(rq3, rq4))

            annual_avg_scores = {}
            for subj in all_subjects:
                nums = [float(sc(r).get(subj)) for r in (rq1, rq2, rq3, rq4)
                        if isinstance(sc(r).get(subj), (int, float))]
                annual_avg_scores[subj] = (sum(nums)/len(nums)) if nums else ""

            annual_total  = sum(float(v(r, "total", 0) or 0)
                                for r in (rq1, rq2, rq3, rq4) if r)
            annual_avg    = float(v(annual_row, "average", 0) or 0)
            annual_cond   = str(v(annual_row, "discipline") or "")
            annual_status = str(v(annual_row, "result_status") or "")
            rank_val      = annual_rank_of(sid)

            def q_rank(q, r):
                stored = v(r, "RANK") if r else ""
                if stored not in ("", None):
                    return stored
                return q_ranks.get(q, {}).get(sid, "")

            data = [headers]
            data.append(build_row("Q1", rq1, rank_val=q_rank("Q1", rq1)))
            data.append(build_row("Q2", rq2, rank_val=q_rank("Q2", rq2)))
            r1 = q_rank("Q1", rq1); r2 = q_rank("Q2", rq2)
            s1_rank = (round((int(r1) + int(r2))/2)
                    if str(r1).isdigit() and str(r2).isdigit() else "")
            data.append(build_row("S1", s1_fake, rank_val=s1_rank))
            data.append(build_row("Q3", rq3, rank_val=q_rank("Q3", rq3)))
            data.append(build_row("Q4", rq4, rank_val=q_rank("Q4", rq4)))
            r3 = q_rank("Q3", rq3); r4 = q_rank("Q4", rq4)
            s2_rank = (round((int(r3) + int(r4))/2)
                    if str(r3).isdigit() and str(r4).isdigit() else "")
            data.append(build_row("S2", s2_fake, rank_val=s2_rank))

            ann_row = [str(sid), student_name, gender, str(age), "Av."]
            for subj in all_subjects:
                ann_row.append(fmt_num(annual_avg_scores.get(subj)))
            ann_row.extend([
                fmt_num(annual_total), fmt_num(annual_avg),
                str(rank_val or ""), annual_cond, "", "",
            ])
            data.append(ann_row)

            tbl = Table(data, colWidths=col_widths, repeatRows=1)
            last_col = len(headers) - 1
            tbl.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.35, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.8, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#DDDDDD")),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('SPAN', (0, 1), (0, -1)),
                ('SPAN', (1, 1), (1, -1)),
                ('SPAN', (2, 1), (2, -1)),
                ('SPAN', (3, 1), (3, -1)),
                ('SPAN', (last_col, 1), (last_col, -1)),
                ('ALIGN', (last_col, 1), (last_col, -1), 'CENTER'),
                ('VALIGN', (last_col, 1), (last_col, -1), 'MIDDLE'),
            ]))
            w_, h_ = tbl.wrapOn(c, width, y)
            tbl.drawOn(c, LEFT_MARGIN, y - h_)

            if annual_status:
                remark_x = LEFT_MARGIN + sum(col_widths[:-1]) + remark_w / 2
                remark_y = y - h_ + h_ / 2 - 2
                c.setFont("Nyala", 8.5)
                c.drawCentredString(remark_x, remark_y, annual_status)

            y -= h_ + 0.6*cm

            # ============================================================
            # TABLE 2: PERSONAL DEVELOPMENT
            # ============================================================
            pd_col_w = [4.8*cm, 1.2*cm, 1.2*cm, 1.2*cm, 1.2*cm]
            pd_total_w = sum(pd_col_w)
            pd_center_x = LEFT_MARGIN + pd_total_w / 2

            draw_title(c, pd_center_x, y, "Basic Skills & Personal Development", font_size=9.5)
            y -= 0.45*cm

            pd_data = [["Traits", "Q1", "Q2", "Q3", "Q4"]]
            pd_src = {
                "Q1": getattr(rq1, "personal_development", {}) or {},
                "Q2": getattr(rq2, "personal_development", {}) or {},
                "Q3": getattr(rq3, "personal_development", {}) or {},
                "Q4": getattr(rq4, "personal_development", {}) or {},
            }
            for trait in PD_TRAITS:
                pd_data.append([trait] + [str(pd_src[q].get(trait, ""))
                                        for q in ("Q1","Q2","Q3","Q4")])
            pd_tbl = Table(pd_data, colWidths=pd_col_w)
            pd_tbl.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
                ('FONTSIZE', (0, 0), (-1, -1), 7.5),
                ('GRID', (0, 0), (-1, -1), 0.35, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.8, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#DDDDDD")),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            pw, ph = pd_tbl.wrapOn(c, width, y)
            pd_bottom = y - ph
            pd_tbl.drawOn(c, LEFT_MARGIN, pd_bottom)

            # ============================================================
            # ADDRESSES — only under the PD table (4 compact lines)
            # ============================================================
            addr_y = pd_bottom - 0.35*cm
            c.setFont("Nyala", 7.5)

            # Line 1: "King's Academy Addresses" + "P.O.Box: 179"
            c.drawString(LEFT_MARGIN, addr_y, "King's Academy Addresses")
            c.drawString(LEFT_MARGIN + 5.5*cm, addr_y, "P.O.Box: 179")
            addr_y -= 0.3*cm

            # Line 2
            c.drawString(LEFT_MARGIN, addr_y,
                        "1. Primary & High School Division  —  Tel: 251--58--114--19--03")
            addr_y -= 0.3*cm

            # Line 3
            c.drawString(LEFT_MARGIN, addr_y,
                        "2. Kindergarten Division  —  Tel: 251--58--114--19--02")
            addr_y -= 0.3*cm

            # Line 4
            c.drawString(LEFT_MARGIN, addr_y,
                        "E-Mail: king's.academy1@yahoo.com")
            addr_bottom = addr_y - 0.2*cm

            # ============================================================
            # TABLE 3: HR COMMENTS
            # ============================================================
            gap = 0.6*cm
            hr_x = LEFT_MARGIN + pd_total_w + gap
            hr_width = width - RIGHT_MARGIN - hr_x
            hr_center_x = hr_x + hr_width / 2

            draw_title(c, hr_center_x, y + 0.45*cm,
                    "Home Room Teacher's Comments", font_size=9.5)

            hr_top = y

            INDENT = 0.35*cm
            SIG_INDENT = 0.7*cm

            hr_rows = []
            hr_style_rules = []
            row_index = 0
            for qn, qr in zip(("Quarter 1.", "Quarter 2.", "Quarter 3."),
                            (rq1, rq2, rq3)):
                avg = float(getattr(qr, "average", 0) or 0) if qr else 0
                remark = get_auto_remark(avg, gender) if qr else ""

                hr_rows.append([qn, ""])
                hr_style_rules.append(('SPAN', (0, row_index), (-1, row_index)))
                hr_style_rules.append(('ALIGN', (0, row_index), (-1, row_index), 'LEFT'))
                hr_style_rules.append(('LEFTPADDING', (0, row_index), (-1, row_index), INDENT))
                hr_style_rules.append(('LINEBELOW', (0, row_index), (-1, row_index),
                                    0.8, colors.black))
                row_index += 1

                hr_rows.append([f"አስተያየት: {remark}", ""])
                hr_style_rules.append(('SPAN', (0, row_index), (-1, row_index)))
                hr_style_rules.append(('ALIGN', (0, row_index), (-1, row_index), 'LEFT'))
                hr_style_rules.append(('LEFTPADDING', (0, row_index), (-1, row_index), INDENT))
                hr_style_rules.append(('FONTSIZE', (0, row_index), (-1, row_index), 7.5))
                hr_style_rules.append(('LINEBELOW', (0, row_index), (-1, row_index),
                                    0.3, colors.HexColor("#888888")))
                row_index += 1

                hr_rows.append(["Teacher's Name & Signature", ""])
                hr_style_rules.append(('SPAN', (0, row_index), (-1, row_index)))
                hr_style_rules.append(('ALIGN', (0, row_index), (-1, row_index), 'LEFT'))
                hr_style_rules.append(('LEFTPADDING', (0, row_index), (-1, row_index), SIG_INDENT))
                hr_style_rules.append(('FONTSIZE', (0, row_index), (-1, row_index), 7.5))
                row_index += 1

                hr_rows.append(["Parent's Name & Signature", ""])
                hr_style_rules.append(('SPAN', (0, row_index), (-1, row_index)))
                hr_style_rules.append(('ALIGN', (0, row_index), (-1, row_index), 'LEFT'))
                hr_style_rules.append(('LEFTPADDING', (0, row_index), (-1, row_index), SIG_INDENT))
                hr_style_rules.append(('FONTSIZE', (0, row_index), (-1, row_index), 7.5))
                hr_style_rules.append(('BOTTOMPADDING', (0, row_index), (-1, row_index), 8))
                row_index += 1

            hr_col_w = [hr_width * 0.30, hr_width * 0.70]
            hr_tbl = Table(hr_rows, colWidths=hr_col_w)
            hr_tbl.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Nyala'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ] + hr_style_rules))
            hw, hh = hr_tbl.wrapOn(c, width, hr_top)
            hr_bottom = hr_top - hh
            hr_tbl.drawOn(c, hr_x, hr_bottom)

            # signature lines after each label
            row_heights = hr_tbl._rowHeights
            cur_top = hr_top
            for ri, row in enumerate(hr_rows):
                label = row[0]
                if label in ("Teacher's Name & Signature",
                            "Parent's Name & Signature"):
                    rh = row_heights[ri]
                    line_y = cur_top - rh * 0.55
                    label_x = hr_x + SIG_INDENT
                    tw = c.stringWidth(label, "Nyala", 7.5)
                    c.setStrokeColor(colors.black)
                    c.setLineWidth(0.4)
                    c.line(label_x + tw + 0.3*cm, line_y,
                        hr_x + hr_width - 0.4*cm, line_y)
                cur_top -= row_heights[ri]

            # ============================================================
            # (Footer removed — no report_title / report_date line)
            # ============================================================

            if idx < len(grouped) - 1:
                c.showPage()

        c.save()
        return response


    print_individual_student_result_pdf.short_description = "Print Student Report Cards (PDF)"
# student/admin.py
from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm
# from .models import StudentResultSectionSummary

import requests
from io import BytesIO
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
from django.contrib import admin
# from .models import StudentResultSectionSummary

@admin.action(description="Print Section Summary (PDF) - Subjects Vertical (Dynamic Widths, Logos)")
def print_section_summary_vertical_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="section_summary_vertical.pdf"'

    c = canvas.Canvas(response, pagesize=landscape(A4))
    page_width, page_height = landscape(A4)

    LEFT_MARGIN = 2 * cm
    RIGHT_MARGIN = 2 * cm
    TOP_MARGIN = 2 * cm

    # Logo URL
    logo_url = "https://uog.edu.et/wp-content/uploads/2022/08/logo.png"

    # Download logo once
    try:
        r = requests.get(logo_url)
        logo_image = ImageReader(BytesIO(r.content))  # <-- wrap with ImageReader
    except:
        logo_image = None

    for idx, section in enumerate(queryset, start=1):
        y = page_height - TOP_MARGIN

        # ===== Draw Logos =====
        logo_height = 4*cm
        logo_width = 4*cm
        if logo_image:
            # Left corner
            c.drawImage(logo_image, LEFT_MARGIN, y - logo_height, width=logo_width, height=logo_height, preserveAspectRatio=True)
            # Right corner
            c.drawImage(logo_image, page_width - RIGHT_MARGIN - logo_width, y - logo_height, width=logo_width, height=logo_height, preserveAspectRatio=True)

        # ===== Title =====
        title = f"{section.grade} - {section.section} ({section.academic_year}) Section Summary"
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(page_width / 2, y - logo_height/2, title)
        y -= logo_height + 0.8*cm

        # Section Info
        c.setFont("Helvetica", 10)
        c.drawString(LEFT_MARGIN, y, f"Section Head: {section.section_head or ''}")
        c.drawString(page_width/2, y, f"Archive Officer: {section.archive_officer_name or ''}")
        y -= 0.4 * cm
        c.drawString(LEFT_MARGIN, y, f"School Director: {section.school_director_name or ''}")
        c.drawString(page_width/2, y, f"Report Date: {section.report_date or ''}")
        y -= 1*cm

        # Subjects
        subjects = (section.subjects or "").splitlines()
        if not subjects:
            subjects = ["No subjects"]

        # Horizontal headers
        headers = [
            "Registered", "Seated", "Not Seated",
            "Mark < 50", "Mark >= 50", "Mark >= 75", "Mark >= 85",
            "% < 50", "% >= 50", "% >= 75", "% >= 85",
            "Total", "Average"
        ]

        values = [
            section.registered_total,
            section.seated_total,
            section.not_seated_total,
            section.mark_lt_50,
            section.mark_ge_50,
            section.mark_ge_75,
            section.mark_ge_85,
            section.pct_lt_50,
            section.pct_ge_50,
            section.pct_ge_75,
            section.pct_ge_85,
            section.section_total_mark,
            section.section_average_mark
        ]

        # Table data
        table_data = [["Subject"] + headers]
        for subj in subjects:
            row = [subj] + values
            table_data.append(row)

        # ===== DYNAMIC COLUMN WIDTHS =====
        total_width = page_width - LEFT_MARGIN - RIGHT_MARGIN
        subject_col_width = max(0*cm, total_width * 0.1)
        remaining_width = total_width - subject_col_width
        metric_col_width = remaining_width / len(headers)
        col_widths = [subject_col_width] + [metric_col_width]*len(headers)

        # Create Table 
        t = Table(table_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ]))

        w, h = t.wrapOn(c, page_width, y)
        t.drawOn(c, LEFT_MARGIN, y - h)
        y -= h + 1*cm

        if idx < queryset.count():
            c.showPage()

    c.save()
    return response

# Register Admin
# @admin.register(StudentResultSectionSummary)
# class StudentResultSectionSummaryAdmin(admin.ModelAdmin):
#     list_display = ("grade", "section", "academic_year", "section_head", "report_date")
#     actions = [print_section_summary_vertical_pdf]
#     readonly_fields = [f.name for f in StudentResultSectionSummary._meta.fields]
    
# class StudentRosterAdmin(ImportExportModelAdmin):
#     # pass
#     fields = [('id', 'academic_year'), ('student', 'semester'), ('amharic', 'english', 'mathematics', 'physics', 'chemistry', 'biology', 'civics', 'td', 'hpe', 'it', 'agriculture'), ('total', 'average', 'rank'), ('remark', 'conduct')]
#     list_display = ['id', 'academic_year', 'student', 'semester', 'total', 'average', 'rank']
#     search_fields = ['id', 'student', 'academic_year']
#     list_filter = ['academic_year', 'semester']
#     list_display_links = ['id', 'academic_year', 'student', 'semester', 'total', 'average']
#     readonly_fields = ('id', 'academic_year', 'total', 'average',)
#     list_per_page = 10
#     list_select_related = True
#     autocomplete_fields = ['student']
#     save_on_top = True  # Show save buttons at the top of the form

#     # def get_actions(self, request):
#     #     actions = super().get_actions(request)
#     #     if 'delete_selected' in actions:
#     #         del actions['delete_selected']
#     #     return actions

#     class Meta:
#         model = StudentRoster

# admin.site.register(StudentRoster, StudentRosterAdmin)

# class SocialStudentRosterAdmin(ImportExportModelAdmin):
#     # pass
#     fields = [('id', 'academic_year'), ('student', 'semester'), ('amharic', 'english', 'mathematics', 'geography', 'gbusiness', 'history', 'economics', 'civics', 'hpe', 'it', 'agriculture'), ('total', 'average', 'rank'), ('remark', 'conduct')]
#     list_display = ['id', 'academic_year', 'student', 'semester', 'total', 'average', 'rank']
#     search_fields = ['id', 'student', 'academic_year']
#     list_filter = ['academic_year', 'semester']
#     list_display_links = ['id', 'academic_year', 'student', 'semester', 'total', 'average']
#     readonly_fields = ('id', 'academic_year', 'total', 'average',)
#     list_per_page = 10
#     list_select_related = True
#     autocomplete_fields = ['student']
#     save_on_top = True  # Add this line to enable the "Save" button at the top of the form

#     # def get_actions(self, request):
#     #     actions = super().get_actions(request)
#     #     if 'delete_selected' in actions:
#     #         del actions['delete_selected']
#     #     return actions

#     class Meta:
#         model = SocialStudentRoster

# admin.site.register(SocialStudentRoster, SocialStudentRosterAdmin)

# Custom PDF generation action
def generate_pdf_report(modeladmin, request, queryset):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Students by Section Report")
    p.setFont("Helvetica", 10)
    p.drawString(100, 730, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Column headers
    p.setFont("Helvetica-Bold", 12)
    y_position = 700
    p.drawString(100, y_position, "Grade")
    p.drawString(180, y_position, "Section")
    p.drawString(260, y_position, "Total Students")
    p.drawString(380, y_position, "ID")
    
    # Data rows
    p.setFont("Helvetica", 10)
    y_position = 680
    
    for student in queryset:
        p.drawString(100, y_position, str(student.grade_id))
        p.drawString(180, y_position, str(student.section_id))
        p.drawString(260, y_position, str(student.total_students))
        p.drawString(380, y_position, str(student.id))
        
        y_position -= 20
        if y_position < 100:  # New page if needed
            p.showPage()
            p.setFont("Helvetica", 10)
            y_position = 750
    
    # Footer
    p.drawString(100, 50, "Gondar University Community School")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students_by_section_report.pdf"'
    return response

generate_pdf_report.short_description = "Generate PDF Report"


# HTML Report Action
def print_students_by_section_report(modeladmin, request, queryset):
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Students by Section Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                position: relative;
            }}
            h1 {{
                text-align: center;
                margin-top: 0;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }}
            .header-logo {{
                text-align: center;
            }}
            .header-logo img {{
                max-width: 150px;
            }}
            .watermark {{
                position: absolute;
                top: 50%;
                left: 50%;
                width: 400px;
                height: auto;
                opacity: 0.1;
                transform: translate(-50%, -50%);
                z-index: -1;
            }}
            hr {{
                border: 1px solid black;
                margin: 10px 0;
            }}
            .date-info {{
                text-align: right;
                margin-top: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #000;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                font-size: 12px;
                color: #555;
            }}
            .print-button {{
                text-align: center;
                margin: 10px 0 20px;
            }}
            .print-button button {{
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
            }}
            @media print {{
                .print-button {{
                    display: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                <strong>ጎንደር ዩኒቨርሲቲ</strong><br>
                የማህበረሰብ ት/ቤት<br>
                ጎንደር ኢትዮጵያ
            </div>
            <div class="header-logo">
                <img src="https://ncee.org.uk/wp-content/uploads/2023/11/gondar.png" alt="Logo">
            </div>
            <div>
                <strong>University of Gondar</strong><br>
                Community School<br>
                Gondar, Ethiopia
            </div>
        </div>

        <hr>

        <div class="date-info">
            Date: {current_date}
        </div>

        <h1>Students by Section Report</h1>
        
        <div class="print-button">
            <button onclick="window.print()">Print Report</button>
        </div>

        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Grade</th>
                    <th>Section</th>
                    <th>Total Students</th>
                </tr>
            </thead>
            <tbody>
    '''
    
    for student in queryset:
        html_content += f'''
                <tr>
                    <td>{student.id}</td>
                    <td>{escape(str(student.grade_id))}</td>
                    <td>{escape(str(student.section_id))}</td>
                    <td>{escape(str(student.total_students))}</td>
                </tr>
        '''
    
    html_content += f'''
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="3" style="text-align: right; font-weight: bold;">Total Records:</td>
                    <td style="font-weight: bold;">{queryset.count()}</td>
                </tr>
            </tfoot>
        </table>

        <div class="watermark">
            <img src="https://ncee.org.uk/wp-content/uploads/2023/11/gondar.png" alt="Watermark">
        </div>

        <div class="footer">
            Gondar University - Community School<br>
            Phone: 0581141240 | Fax: 0581141240 | P.O. Box: 196
        </div>
        
        <script>
            window.onload = function() {{
                // Auto-print option (uncomment if needed)
                // window.print();
            }};
        </script>
    </body>
    </html>
    '''
    
    return HttpResponse(html_content)

print_students_by_section_report.short_description = "Generate HTML Report"


class StudentsBySectionAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ("grade_id", "section_id", "total_students", "print_report_link")
    
    # Only actual fields should be in list_display_links
    list_display_links = ("grade_id", "section_id")
    
    # Filters for easy navigation
    list_filter = ("grade_id", "section_id")
    
    # Enable search
    search_fields = ("grade_id", "section_id")
    
    # Default ordering
    ordering = ("grade_id", "section_id")
    
    # Add custom actions
    actions = [print_students_by_section_report, generate_pdf_report]
    
    # Make all fields read-only since it's a view
    def get_readonly_fields(self, request, obj=None):
        return ["grade_id", "section_id", "total_students"]
    
    # Custom method to display print link
    def print_report_link(self, obj):
        return format_html(
            '<a href="/admin/students_by_section_report/?grade={}&section={}" target="_blank">📄 Print</a>',
            obj.grade_id,
            obj.section_id
        )
    
    print_report_link.short_description = "Actions"
    
    # Optional: Add a custom URL for the report
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('students_by_section_report/', 
                 self.admin_site.admin_view(self.students_report_view),
                 name='students_by_section_report'),
        ]
        return custom_urls + urls
    
    def students_report_view(self, request):
        # Get grade and section from query parameters
        grade = request.GET.get('grade')
        section = request.GET.get('section')
        
        # Filter queryset based on parameters
        queryset = StudentsBySection.objects.all()
        if grade:
            queryset = queryset.filter(grade_id=grade)
        if section:
            queryset = queryset.filter(section_id=section)
        
        # Return the print view with filtered queryset
        return print_students_by_section_report(self, request, queryset)


admin.site.register(StudentsBySection, StudentsBySectionAdmin)

class StudentStatisticsAdmin(ImportExportModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'academic_year', 'grade', 'section', 'gender', 'total_students')
    list_display_links = ('id', 'academic_year', 'grade', 'section', 'gender', 'total_students') 
    
    # Filters for easy navigation
    list_filter = ("grade", "section")
    
    # Enable search by grade and section
    search_fields = ("grade", "section")
    
    # Default ordering
    ordering = ("grade", "section")
    
    # Add grouping and read-only fields for the view
    readonly_fields = ('id', 'academic_year', 'grade', 'section', 'gender', 'total_students')
    
    # Admin display customization
    fieldsets = (
        ("General Details", {
            "fields": ('academic_year', 'grade', 'section', 'gender'),
            "description": "Displays grade and section details.",
        }),
        ("Student Count", {
            "fields": ("total_students",),
            "description": "Shows the total number of students in each grade-section combination.",
        }),
    )
    
    # actions = [print_students_by_section_report, generate_pdf_report]
    
    # actions = [generate_pdf_report]
    
    # def print_students_by_section_report(self, obj):
    #     return format_html(
    #         '<a href="{}" target="_blank">Print</a>',
    #         reverse('students_by_section_report')
    #     )
    # print_students_by_section_report.short_description = "Print Students Report"
    
    
    class Meta:
        model = StudentStatistics

admin.site.register(StudentStatistics, StudentStatisticsAdmin)

from django.contrib import admin
from django.db.models import F, Q
from django.utils.html import format_html

from .models import StudentResultAnalysisView, StudentGradeLevelAnalysisView


# ---------------------------------------------------------------------------
# Reusable admin display helpers
# ---------------------------------------------------------------------------
def _pct(part, whole):
    """Return 'xx.x%' or '—'."""
    try:
        if not whole:
            return "—"
        return f"{part * 100 / whole:.1f}%"
    except Exception:
        return "—"


def _badge(text, color):
    """Small colored badge using Django admin's built-in badge style."""
    return format_html(
        '<span style="display:inline-block;padding:2px 8px;border-radius:10px;'
        'font-size:11px;font-weight:600;background:{};color:#fff;">{}</span>',
        color, text,
    )


# ---------------------------------------------------------------------------
# Subject-level analysis
# ---------------------------------------------------------------------------
@admin.register(StudentResultAnalysisView)
class StudentResultAnalysisViewAdmin(ImportExportModelAdmin):
    list_display = (
        "academic_year",
        "grade",
        "subject_name",
        "registered_total",
        "tested_total",
        "pass_rate_display",
        "above_75_display",
        "above_85_display",
        "under_50_display",
        "gender_split_display",
    )
    list_filter = ("academic_year", "grade", "subject_name")
    search_fields = ("subject_name",)
    ordering = ("academic_year", "grade", "subject_name")
    list_per_page = 50
    list_select_related = False

    # Read-only view → no add / change / delete
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # ---------- computed columns ----------
    @admin.display(description="Pass rate (≥50)")
    def pass_rate_display(self, obj):
        pct = _pct(obj.above_50_total, obj.tested_total)
        color = "#198754" if obj.tested_total and obj.above_50_total * 100 / obj.tested_total >= 80 else \
                "#fd7e14" if obj.tested_total and obj.above_50_total * 100 / obj.tested_total >= 50 else \
                "#dc3545"
        return _badge(pct, color)

    @admin.display(description="Above 75")
    def above_75_display(self, obj):
        return _pct(obj.above_75_total, obj.tested_total)

    @admin.display(description="Above 85")
    def above_85_display(self, obj):
        return _pct(obj.above_85_total, obj.tested_total)

    @admin.display(description="Under 50")
    def under_50_display(self, obj):
        if not obj.under_50_total:
            return "—"
        return _badge(str(obj.under_50_total), "#dc3545")

    @admin.display(description="M / F")
    def gender_split_display(self, obj):
        return format_html(
            '<span style="color:#0d6efd;font-weight:600;">{}</span>'
            ' <span style="color:#adb5bd;">/</span> '
            '<span style="color:#d63384;font-weight:600;">{}</span>',
            obj.registered_males, obj.registered_females,
        )

    # ---------- readonly detail page ----------
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def get_fieldsets(self, request, obj=None):
        return (
            ("Context", {
                "fields": ("academic_year", "grade", "subject_name"),
            }),
            ("Registration", {
                "fields": (
                    ("registered_males", "registered_females", "registered_total"),
                ),
            }),
            ("Tested", {
                "fields": (
                    ("tested_males", "tested_females", "tested_total"),
                ),
            }),
            ("Below 50", {
                "fields": (
                    ("under_50_males", "under_50_females", "under_50_total"),
                ),
            }),
            ("Above 50", {
                "fields": (
                    ("above_50_males", "above_50_females", "above_50_total"),
                ),
            }),
            ("Above 75", {
                "fields": (
                    ("above_75_males", "above_75_females", "above_75_total"),
                ),
            }),
            ("Above 85", {
                "fields": (
                    ("above_85_males", "above_85_females", "above_85_total"),
                ),
            }),
        )

    # ---------- queryset tweaks ----------
    def get_queryset(self, request):
        return super().get_queryset(request)


# ---------------------------------------------------------------------------
# Grade-level analysis
# ---------------------------------------------------------------------------
@admin.register(StudentGradeLevelAnalysisView)
class StudentGradeLevelAnalysisViewAdmin(ImportExportModelAdmin):
    list_display = (
        "academic_year",
        "grade",
        "registered_total",
        "tested_total",
        "promoted_total",
        "repeated_total",
        "promotion_rate_display",
        "pass_rate_display",
        "above_85_display",
    )
    list_filter = ("academic_year", "grade")
    search_fields = ("grade",)
    ordering = ("academic_year", "id")
    list_per_page = 30

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # ---------- computed columns ----------
    @admin.display(description="Promotion rate")
    def promotion_rate_display(self, obj):
        pct = _pct(obj.promoted_total, obj.registered_total)
        try:
            ratio = obj.promoted_total * 100 / obj.registered_total if obj.registered_total else 0
        except Exception:
            ratio = 0
        color = "#198754" if ratio >= 90 else "#fd7e14" if ratio >= 75 else "#dc3545"
        return _badge(pct, color)

    @admin.display(description="Pass rate (≥50)")
    def pass_rate_display(self, obj):
        pct = _pct(obj.above_50_total, obj.tested_total)
        try:
            ratio = obj.above_50_total * 100 / obj.tested_total if obj.tested_total else 0
        except Exception:
            ratio = 0
        color = "#198754" if ratio >= 80 else "#fd7e14" if ratio >= 50 else "#dc3545"
        return _badge(pct, color)

    @admin.display(description="Above 85")
    def above_85_display(self, obj):
        return _pct(obj.above_85_total, obj.tested_total)

    # ---------- readonly detail page ----------
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def get_fieldsets(self, request, obj=None):
        return (
            ("Context", {"fields": ("academic_year", "grade")}),
            ("Registration / Testing", {
                "fields": (
                    ("registered_males", "registered_females", "registered_total"),
                    ("tested_males", "tested_females", "tested_total"),
                ),
            }),
            ("Promotion", {
                "fields": (
                    ("promoted_males", "promoted_females", "promoted_total"),
                    ("repeated_males", "repeated_females", "repeated_total"),
                ),
            }),
            ("Score bands", {
                "fields": (
                    ("under_50_males", "under_50_females", "under_50_total"),
                    ("above_50_males", "above_50_females", "above_50_total"),
                    ("above_75_males", "above_75_females", "above_75_total"),
                    ("above_85_males", "above_85_females", "above_85_total"),
                ),
            }),
        )