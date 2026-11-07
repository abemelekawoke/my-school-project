from django.db import models


class Parent(models.Model):
    full_name = models.CharField(max_length=120)
    phone_number = models.CharField(
        max_length=20,
        help_text="Include country code, e.g. 251912345678",
    )
    student_name = models.CharField(max_length=120, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"


class SmsMessage(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    recipient = models.ForeignKey(
        Parent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sms_messages",
    )
    phone_number = models.CharField(max_length=20)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.phone_number} - {self.status}"


class SmsCampaign(models.Model):
    AUDIENCE_ALL = "all"
    AUDIENCE_GRADE = "grade"
    AUDIENCE_SELECTED = "selected"
    AUDIENCE_CHOICES = [
        (AUDIENCE_ALL, "All active parents"),
        (AUDIENCE_GRADE, "Parents in one grade"),
        (AUDIENCE_SELECTED, "Only parents I pick below"),
    ]

    title = models.CharField(max_length=120, help_text="Internal name, not sent.")
    body = models.TextField(help_text="The SMS text that parents will receive.")
    audience = models.CharField(
        max_length=10, choices=AUDIENCE_CHOICES, default=AUDIENCE_ALL
    )
    grade = models.CharField(
        max_length=50,
        blank=True,
        help_text="Required when audience = 'Parents in one grade'.",
    )
    selected_parents = models.ManyToManyField(
        Parent,
        blank=True,
        help_text="Used when audience = 'Only parents I pick below'.",
    )
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    total_sent = models.PositiveIntegerField(default=0)
    total_failed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title