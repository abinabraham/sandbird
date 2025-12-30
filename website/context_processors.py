from __future__ import annotations

from django.http import HttpRequest
from django.utils.translation import get_language


def site_prefs(request: HttpRequest):
    currency = request.session.get('currency', 'AED')
    language = request.session.get('language', 'EN')

    active_lang = get_language() or 'en'

    return {
        'site_currency': currency,
        'site_language': language,
        'site_language_code': active_lang,
        'site_contact_phone': '+256 214 203 215',
        'site_address': 'P.O. Box: 0000, Dubai, UAE',
        'site_hours': 'Mon - Sat: 8:00 - 15:00',
        'site_socials': {
            'facebook': '#',
            'youtube': '#',
            'instagram': '#',
        },
        'site_logo_url': 'https://sandbirdtours.com/assets/img/favicon.png',
        'site_footer_links': {
            'menu': [
                ('About Us', '/about/'),
                ('Services', '/services/'),
                ('Tour Packages', '/tour-package/'),
                ('Our Fleet', '/our-fleet/'),
                ('Become A Traveller', '/contact/'),
            ],
            'useful_links': [
                ('All Packages', '/tour-package/'),
                ('Abu Dhabi Packages', '/tour-package/?location=abu-dhabi'),
                ('Dubai Packages', '/tour-package/?location=dubai'),
                ('Pilgrimage Tour', '/tour-package/'),
                ('Desert', '/tour-package/'),
            ],
            'resources': [
                ('Adventure Packages', '/tour-package/'),
                ('Family Packages', '/tour-package/'),
                ('Pilgrimage Tour', '/tour-package/'),
                ('Desert Safari', '/tour-package/'),
                ('UAE Tour', '/tour-package/'),
            ],
        },
        'site_footer_tags': [
            'Desert Safari',
            'Family Packages',
            'Tour Packages',
            'UAE Tour',
            'Abu Dhabi',
            'Dubai',
        ],
        'site_footer_travellers': [
            {
                'title': 'Become Traveler',
                'subtitle': 'Get The Best Tour &\nUpgrade Your Skills',
                'image_url': 'https://sandbirdtours.com/assets/img/offer/traveller1.png',
                'cta': 'Become A Traveler',
                'href': '/contact/',
            },
            {
                'title': 'Become Traveler',
                'subtitle': 'Get The Best Tour &\nUpgrade Your Skills',
                'image_url': 'https://sandbirdtours.com/assets/img/offer/traveller2.png',
                'cta': 'Become A Traveler',
                'href': '/contact/',
            },
        ],
    }
