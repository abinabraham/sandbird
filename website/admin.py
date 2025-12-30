from django.contrib import admin

from website.models import QuickEnquiry


@admin.register(QuickEnquiry)
class QuickEnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'interested_tour', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'phone', 'email', 'interested_tour', 'message')
