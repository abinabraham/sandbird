from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import activate
from django.views.decorators.http import require_POST

from website.forms import QuickEnquiryForm
from website.models import QuickEnquiry
from tours.models import TourPackage


def home(request: HttpRequest) -> HttpResponse:
    featured_packages = (
        TourPackage.objects.filter(is_active=True, is_featured=True)
        .order_by('-updated_at')
        .only('title', 'slug', 'location', 'price_from', 'duration_days', 'thumbnail_url', 'image_url')[:5]
    )

    top_packages = (
        TourPackage.objects.filter(is_active=True)
        .order_by('-is_featured', '-updated_at')
        .only(
            'title',
            'slug',
            'location',
            'price_from',
            'duration_days',
            'thumbnail_url',
            'image_url',
            'gallery',
        )[:12]
    )

    return render(
        request,
        'website/home.html',
        {
            'featured_packages': featured_packages,
            'top_packages': top_packages,
        },
    )


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'website/about.html')


def services(request: HttpRequest) -> HttpResponse:
    return render(request, 'website/services.html')


def our_fleet(request: HttpRequest) -> HttpResponse:
    fleet_items = [
        {
            'driver_included': True,
            'hours_10': '5,500 AED',
            'hours_5': '3,500 AED',
            'ex_hours': '500 AED',
            'title': 'Rolls Royce Cullinan Mansory',
            'description': (
                'The Rolls-Royce Cullinan is a full-size luxury SUV produced by Rolls-Royce Motor Cars. '
                'The Cullinan is the first SUV to be launched by the Rolls-Royce marque, and is also the '
                'brand’s first all-wheel-drive vehicle. It is named after the Cullinan Diamond, the largest '
                'gem-quality rough diamond ever discovered.'
            ),
            'image_url': 'https://sandbirdtours.com/assets/img/fleet/rr-cullinan-mansory.jpg',
        },
        {
            'driver_included': True,
            'hours_10': '5,500 AED',
            'hours_5': '3,500 AED',
            'ex_hours': '500 AED',
            'title': 'Rolls Royce Cullinan Black Badge',
            'description': (
                'The Rolls-Royce Cullinan is a full-size luxury SUV produced by Rolls-Royce Motor Cars. '
                'The Cullinan is the first SUV to be launched by the Rolls-Royce marque, and is also the '
                'brand’s first all-wheel-drive vehicle. It is named after the Cullinan Diamond, the largest '
                'gem-quality rough diamond ever discovered.'
            ),
            'image_url': 'https://sandbirdtours.com/assets/img/fleet/rr-cullinan-black-badge.jpg',
        },
        {
            'driver_included': True,
            'hours_10': '4,000 AED',
            'hours_5': '2,800 AED',
            'ex_hours': '400 AED',
            'title': 'Rolls Royce Dawn',
            'description': (
                'Highs Beautifully designed body, exceptionally luxurious interior, totally customizable. '
                'Lows Inefficient engine, lacks driver-assistance tech, doesn’t have a sporting bone in its body. '
                'Verdict With the top down, the Dawn is a perfect way to catch the eye. The Rolls Royce Dawn has '
                'a huge 6.6 litre twin-turbo V12 engine under its fantastically designed hood, and cant dish out '
                'a hefty 563 HP. Having a combination of stylishness and power is surely a heavenly experience.'
            ),
            'image_url': 'https://sandbirdtours.com/assets/img/fleet/rr-dawn.jpg',
        },
        {
            'driver_included': True,
            'hours_10': '4,000 AED',
            'hours_5': '2,800 AED',
            'ex_hours': '400 AED',
            'title': 'Rolls Royce Dawn Black',
            'description': (
                'The Rolls Royce Dawn epitomises the pinnacle of luxury and elegance, featuring an exterior of '
                'exquisite craftsmanship and an opulent cabin design, all fully customisable to meet the refined '
                'tastes of our distinguished clientele. Under its elegantly sculpted bonnet, the Dawn houses a '
                'powerful 6.6-litre twin-turbo V12 engine, ensuring a smooth and robust ride that promises not just '
                'a journey, but an experience of unparalleled luxury and power.'
            ),
            'image_url': 'https://sandbirdtours.com/assets/img/fleet/rr-dawn-black.jpg',
        },
        {
            'driver_included': True,
            'hours_10': '2,800 AED',
            'hours_5': '1,800 AED',
            'ex_hours': '200 AED',
            'title': 'Mercedes Benz S 560 Maybach',
            'description': (
                'If you love the Mercedes-Benz S-Class but find it isn’t big enough or exclusive enough for your '
                'tastes, take a look at our Mercedes-Maybach S560. These large ultra-luxury sedans ride on longer '
                'wheelbases than the Benz S-class, and they come with the finest appointments. The S560 is made for '
                'limousine living. Their palatial rear seats are available with all the comforts needed to make '
                'chauffeured journeys an unmitigated delight.'
            ),
            'image_url': 'https://sandbirdtours.com/assets/img/fleet/mercedes-benz-s-560-maybach.jpg',
        },
        {
            'driver_included': True,
            'hours_10': '2,800 AED',
            'hours_5': '1,800 AED',
            'ex_hours': '200 AED',
            'title': 'Mercedes Benz S 500 AMG LINE',
            'description': (
                'The 2022 Mercedes-Benz 500 sedan is beautiful on the outside, stunning on the inside and brings '
                'enough technology into the mix to satisfy even the savviest of owners. It gets bonus points in each '
                'category, going from passenger comfort, safety and performance, leaving no detail unattended. One '
                'could spend days configuring the ideal sedan and still have options to explore. The plethora of '
                'choices and a push for sky-high standards is what makes the 2022 S500 a hallmark of executive sedans.'
            ),
            'image_url': 'https://sandbirdtours.com/assets/img/fleet/mercedes-benz-s-500-amg-line.jpg',
        },
        {
            'driver_included': True,
            'hours_10': '2,800 AED',
            'hours_5': '1,800 AED',
            'ex_hours': '250 AED',
            'title': 'Mercedes Benz G 63 AMG',
            'description': (
                'Experience unparalleled luxury with our Mercedes-Benz G63 AMG in stunning white. This iconic SUV '
                'combines performance and elegance, boasting a handcrafted V8 engine and a lavish interior. Elevate '
                'your travel experience with the perfect blend of comfort and prestige in our white Mercedes-Benz G63 AMG.'
            ),
            'image_url': 'https://sandbirdtours.com/assets/img/fleet/mercedes-benz-g-63-amg.jpg',
        },
        {
            'driver_included': True,
            'hours_10': '4,000 AED',
            'hours_5': '2,800 AED',
            'ex_hours': '350 AED',
            'title': 'Bentley Bentayga',
            'description': (
                'The new Bentayga has been breathtakingly reimagined to inspire exploration in its purest form. It '
                'seamlessly fuses a commanding new design with empowering performance and a suite of innovative '
                'technologies to create a luxury SUV that excels in any environment. Bentayga’s exceptional handling '
                'and outstanding ride comfort lets you experience every environment in world-class refinement. With '
                'its 6.0 litre, twin-turbocharged W12 engine, a step-change in technology and a truly stunning design '
                'language, the Bentley Bentayga is unmatched in its class.'
            ),
            'image_url': 'https://sandbirdtours.com/assets/img/fleet/bentley-bentayga-2.jpg',
        },
        {
            'driver_included': True,
            'hours_10': '2,800 AED',
            'hours_5': '1,800 AED',
            'ex_hours': '250 AED',
            'title': 'BMW 7 Series',
            'description': (
                'Step into the elegance of the BMW 7 Series Black, a distinguished addition to our chauffeur service '
                'fleet. This car, draped in a black finish, effortlessly marries classic aesthetics with advanced '
                'technology. Immerse yourself in supremely comfortable seating and cutting-edge features. With a '
                'formidable engine and top of the range suspension, the BMW 7 Series Black ensures a stylish and '
                'comfortable travel experience.'
            ),
            'image_url': 'https://sandbirdtours.com/assets/img/fleet/bmw-7-series.jpg',
        },
        {
            'driver_included': True,
            'hours_10': '4,000 AED',
            'hours_5': '2,800 AED',
            'ex_hours': '350 AED',
            'title': 'Mercedes-Benz GLS Brabus',
            'description': (
                'The Mercedes-Benz GLS Brabus is a high-performance and luxurious version of the GLS-Class SUV, '
                'customized by Brabus. It features a powerful engine tuned for increased horsepower, along with '
                'bespoke exterior modifications like body kits and larger wheels. Inside, it offers premium materials '
                'and customizable features. Tuned suspension and technology upgrades enhance performance and comfort. '
                'Produced in limited numbers, it represents the epitome of luxury and exclusivity, blending practicality '
                'with refined craftsmanship.'
            ),
            'image_url': 'https://sandbirdtours.com/assets/img/fleet/mercedes-benz-gls-brabus.jpg',
        },
        {
            'driver_included': True,
            'hours_10': '4,000 AED',
            'hours_5': '2,800 AED',
            'ex_hours': '350 AED',
            'title': 'Mercedes-Benz AMG G6 Brabus',
            'description': (
                'The Mercedes-Benz AMG G63 Brabus is a high-performance version of the iconic G-Class SUV, customized '
                'by Brabus for enhanced power and luxury. It boasts a twin-turbo V8 engine with increased horsepower, '
                'along with bespoke exterior modifications like body kits and larger wheels. Inside, it offers premium '
                'materials and customizable features. Tuned suspension and technology upgrades improve performance and '
                'comfort. Produced in limited numbers, it’s a symbol of exclusivity and craftsmanship, blending rugged '
                'capability with refined luxury.'
            ),
            'image_url': 'https://sandbirdtours.com/assets/img/fleet/Mercedes-Benz-AMG-G6-Brabus.jpg',
        },
    ]

    return render(
        request,
        'website/our_fleet.html',
        {
            'fleet_items': fleet_items,
        },
    )


def contact(request: HttpRequest) -> HttpResponse:
    success = False

    if request.method == 'POST':
        form = QuickEnquiryForm(request.POST)
        if form.is_valid():
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
            if ip_address and ',' in ip_address:
                ip_address = ip_address.split(',')[0].strip()

            enquiry = QuickEnquiry.objects.create(
                full_name=form.cleaned_data['full_name'].strip(),
                phone=(form.cleaned_data.get('phone') or '').strip(),
                email=(form.cleaned_data.get('email') or '').strip(),
                interested_tour=(form.cleaned_data.get('interested_tour') or '').strip(),
                message=form.cleaned_data['message'].strip(),
                ip_address=ip_address or None,
                user_agent=(request.META.get('HTTP_USER_AGENT') or '')[:300],
            )

            manager_email = getattr(settings, 'MANAGER_EMAIL', '')
            if manager_email:
                subject = f"New Quick Enquiry: {enquiry.full_name}"
                body = (
                    "A new Quick Enquiry was submitted on SandBird Tours.\n\n"
                    f"Name: {enquiry.full_name}\n"
                    f"Phone: {enquiry.phone or '-'}\n"
                    f"Email: {enquiry.email or '-'}\n"
                    f"Interested Tour: {enquiry.interested_tour or '-'}\n\n"
                    "Message:\n"
                    f"{enquiry.message}\n\n"
                    f"IP Address: {enquiry.ip_address or '-'}\n"
                    f"User Agent: {enquiry.user_agent or '-'}\n"
                    f"Submitted At: {enquiry.created_at}\n"
                )
                try:
                    send_mail(
                        subject,
                        body,
                        getattr(settings, 'DEFAULT_FROM_EMAIL', None) or None,
                        [manager_email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

            success = True
            form = QuickEnquiryForm(initial={'interested_tour': request.GET.get('tour', '')})
    else:
        form = QuickEnquiryForm(initial={'interested_tour': request.GET.get('tour', '')})

    return render(
        request,
        'website/contact.html',
        {
            'form': form,
            'quick_enquiry_success': success,
        },
    )


def tour_package(request: HttpRequest) -> HttpResponse:
    location_q = (request.GET.get('location') or '').strip().lower()
    active_location = None

    qs = TourPackage.objects.filter(is_active=True)
    if location_q in {'dubai'}:
        qs = qs.filter(location=TourPackage.Location.DUBAI)
        active_location = TourPackage.Location.DUBAI
    elif location_q in {'abu-dhabi', 'abudhabi', 'abu_dhabi'}:
        qs = qs.filter(location=TourPackage.Location.ABU_DHABI)
        active_location = TourPackage.Location.ABU_DHABI

    packages = qs.order_by('-is_featured', 'title')
    return render(
        request,
        'website/tour_package.html',
        {
            'packages': packages,
            'active_location': active_location,
        },
    )


def tour_package_detail(request: HttpRequest, slug: str) -> HttpResponse:
    package = get_object_or_404(TourPackage, slug=slug, is_active=True)

    keywords_list: list[str] = []
    if package.keywords:
        keywords_list = [k.strip() for k in package.keywords.split(',') if k.strip()]

    return render(
        request,
        'website/tour_package_detail.html',
        {
            'package': package,
            'keywords_list': keywords_list,
        },
    )


@require_POST
def set_prefs(request: HttpRequest) -> HttpResponse:
    currency = (request.POST.get('currency') or 'AED').upper().strip()
    language = (request.POST.get('language') or 'EN').upper().strip()

    allowed_currency = {'AED', 'USD', 'EUR', 'GBP'}
    allowed_language = {'EN', 'AR'}

    lang_code = None
    if language in allowed_language:
        lang_code = 'ar' if language == 'AR' else 'en'

    if currency in allowed_currency:
        request.session['currency'] = currency
    if language in allowed_language:
        request.session['language'] = language

    if lang_code:
        activate(lang_code)
        request.session['django_language'] = lang_code

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'

    if lang_code:
        parts = urlsplit(next_url)
        path = parts.path or '/'

        # Strip any existing language prefix, then prepend the requested one.
        if path == '/en' or path.startswith('/en/'):
            path = path[3:] or '/'
        elif path == '/ar' or path.startswith('/ar/'):
            path = path[3:] or '/'

        if not path.startswith('/'):
            path = '/' + path

        path = '/' + lang_code + ('' if path == '/' else path)

        next_url = urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))

    return redirect(next_url)
