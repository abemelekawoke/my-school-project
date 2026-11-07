from django.contrib import admin, messages
from django.utils import timezone
from .models import Parent, SmsMessage, SmsCampaign
from .services import send_sms_hilink


# ---------- Parent ----------

class SmsMessageInline(admin.TabularInline):
    model = SmsMessage
    extra = 0
    fields = ("body", "status", "error_message", "sent_at")
    readonly_fields = ("status", "error_message", "sent_at")
    # can_delete = False
    show_change_link = True


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_number", "student_name", "grade", "is_active")
    list_filter = ("grade", "is_active")
    search_fields = ("full_name", "phone_number", "student_name")
    inlines = [SmsMessageInline]


# ---------- Single SMS ----------

@admin.register(SmsMessage)
class SmsMessageAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "status", "sent_at", "created_at")
    list_display_links = ("phone_number",)
    list_filter = ("status",)
    search_fields = ("phone_number", "body")
    readonly_fields = ("status", "error_message", "sent_at", "created_at")

    def save_model(self, request, obj, form, change):
        if not change and obj.phone_number and obj.body:
            super().save_model(request, obj, form, change)
            ok, err = send_sms_hilink(obj.phone_number, obj.body)
            obj.status = "sent" if ok else "failed"
            obj.error_message = err
            obj.sent_at = timezone.now() if ok else None
            obj.save()
            if ok:
                messages.success(request, f"SMS sent to {obj.phone_number}.")
            else:
                messages.error(request, f"SMS failed: {err}")
            return
        super().save_model(request, obj, form, change)


# ---------- Bulk SMS campaign ----------

@admin.register(SmsCampaign)
class SmsCampaignAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "audience",
        "is_sent",
        "total_sent",
        "total_failed",
        "sent_at",
        "created_at",
    )
    list_display_links = ("title",)
    list_filter = ("is_sent", "audience")
    search_fields = ("title", "body", "grade")
    readonly_fields = ("is_sent", "sent_at", "total_sent", "total_failed", "created_at")
    filter_horizontal = ("selected_parents",)
    fieldsets = (
        ("Message", {"fields": ("title", "body")}),
        ("Audience", {"fields": ("audience", "grade", "selected_parents")}),
        (
            "Result",
            {
                "fields": (
                    "is_sent",
                    "sent_at",
                    "total_sent",
                    "total_failed",
                    "created_at",
                )
            },
        ),
    )
    actions = ["send_campaign_now"]

    def _targets(self, campaign):
        if campaign.audience == SmsCampaign.AUDIENCE_ALL:
            return Parent.objects.filter(is_active=True)
        if campaign.audience == SmsCampaign.AUDIENCE_GRADE:
            return Parent.objects.filter(is_active=True, grade=campaign.grade)
        return campaign.selected_parents.filter(is_active=True)

    def _run(self, request, campaign):
        if campaign.is_sent:
            messages.warning(request, f"'{campaign.title}' was already sent.")
            return
        if not campaign.body.strip():
            messages.error(request, "Body is empty.")
            return
        if campaign.audience == SmsCampaign.AUDIENCE_GRADE and not campaign.grade.strip():
            messages.error(request, "Grade is required for 'Parents in one grade'.")
            return

        targets = list(self._targets(campaign))
        if not targets:
            messages.error(request, "No parents matched the audience.")
            return

        success = fail = 0
        for parent in targets:
            ok, err = send_sms_hilink(parent.phone_number, campaign.body)
            SmsMessage.objects.create(
                recipient=parent,
                phone_number=parent.phone_number,
                body=campaign.body,
                status="sent" if ok else "failed",
                error_message=err,
                sent_at=timezone.now() if ok else None,
            )
            success += 1 if ok else 0
            fail += 0 if ok else 1

        campaign.is_sent = True
        campaign.sent_at = timezone.now()
        campaign.total_sent = success
        campaign.total_failed = fail
        campaign.save(update_fields=["is_sent", "sent_at", "total_sent", "total_failed"])

        messages.success(
            request,
            f"'{campaign.title}' sent: {success} success, {fail} failed.",
        )

    def send_campaign_now(self, request, queryset):
        for campaign in queryset:
            self._run(request, campaign)

    send_campaign_now.short_description = "Send selected campaign(s) now"