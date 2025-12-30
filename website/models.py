from django.db import models


class QuickEnquiry(models.Model):
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    interested_tour = models.CharField(max_length=160, blank=True)
    message = models.TextField(max_length=2000)

    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=300, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.full_name} ({self.email or self.phone or 'no-contact'})"
