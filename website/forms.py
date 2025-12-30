from __future__ import annotations

import re

from django import forms


_PHONE_RE = re.compile(r"^[0-9+()\-\s]{7,30}$")


class QuickEnquiryForm(forms.Form):
    full_name = forms.CharField(max_length=120, required=True)
    phone = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    interested_tour = forms.CharField(max_length=160, required=False)
    message = forms.CharField(max_length=2000, required=True, widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()

        phone = (cleaned_data.get('phone') or '').strip()
        email = (cleaned_data.get('email') or '').strip()

        if not phone and not email:
            raise forms.ValidationError('Please provide at least a phone number or an email address.')

        if phone and not _PHONE_RE.match(phone):
            self.add_error('phone', 'Please enter a valid phone / WhatsApp number.')

        return cleaned_data
