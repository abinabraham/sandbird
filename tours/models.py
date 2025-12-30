from django.db import models
from django.utils.text import slugify


class TourPackage(models.Model):
    class Location(models.TextChoices):
        DUBAI = 'DUBAI', 'Dubai'
        ABU_DHABI = 'ABU_DHABI', 'Abu Dhabi'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    location = models.CharField(max_length=20, choices=Location.choices)

    short_description = models.CharField(max_length=260, blank=True)
    description = models.TextField(blank=True)

    duration_days = models.PositiveIntegerField(null=True, blank=True)
    price_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='AED')

    image_url = models.URLField(blank=True)
    thumbnail_url = models.URLField(blank=True)

    highlights = models.TextField(blank=True)
    itinerary = models.JSONField(default=list, blank=True)
    gallery = models.JSONField(default=list, blank=True)
    reviews = models.JSONField(default=list, blank=True)
    keywords = models.CharField(max_length=500, blank=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'title']

    def __str__(self) -> str:
        return f"{self.title} ({self.get_location_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200] or 'tour'
            slug = base
            i = 2
            while TourPackage.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)
