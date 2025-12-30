from django.contrib import admin

from .models import TourPackage


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'location',
        'price_from',
        'currency',
        'duration_days',
        'is_featured',
        'is_active',
        'updated_at',
    )
    list_filter = ('location', 'is_featured', 'is_active')
    search_fields = ('title', 'short_description', 'description', 'keywords')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (
            'Basic',
            {
                'fields': (
                    'title',
                    'slug',
                    'location',
                    'short_description',
                    'description',
                    'is_featured',
                    'is_active',
                )
            },
        ),
        (
            'Media',
            {
                'fields': (
                    'thumbnail_url',
                    'image_url',
                    'gallery',
                )
            },
        ),
        (
            'Pricing & Duration',
            {'fields': ('duration_days', 'price_from', 'currency')},
        ),
        (
            'Content',
            {'fields': ('highlights', 'itinerary', 'reviews', 'keywords')},
        ),
        (
            'Timestamps',
            {'fields': ('created_at', 'updated_at')},
        ),
    )
