// Reserved for small progressive enhancements.

(function () {
  function hideLoader() {
    document.body.classList.add('sb-loaded');
    document.body.classList.remove('sb-preload');
  }

  if (document.readyState === 'complete') {
    hideLoader();
  } else {
    window.addEventListener('load', hideLoader, { once: true });
    window.setTimeout(hideLoader, 2200);
  }
})();

(function () {
  function setupQuickEnquiry() {
    var form = document.getElementById('sbQuickEnquiry');
    if (!form) return;

    var submitBtn = document.getElementById('sbQuickEnquirySubmit');
    var isSubmitting = false;

    function markValidity() {
      var fields = Array.prototype.slice.call(form.querySelectorAll('input, textarea, select'));
      fields.forEach(function (field) {
        if (field.disabled) return;
        if (!field.willValidate) return;
        if (field.checkValidity()) {
          field.classList.remove('is-invalid');
        } else {
          field.classList.add('is-invalid');
        }
      });
    }

    form.addEventListener('submit', function (e) {
      if (isSubmitting) {
        e.preventDefault();
        return;
      }

      if (!form.checkValidity()) {
        e.preventDefault();
        markValidity();
        return;
      }

      isSubmitting = true;
      if (submitBtn) submitBtn.disabled = true;
    });

    form.addEventListener('input', function (e) {
      var t = e.target;
      if (!t || !t.willValidate) return;
      if (t.checkValidity()) {
        t.classList.remove('is-invalid');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupQuickEnquiry);
  } else {
    setupQuickEnquiry();
  }
})();

(function () {
  function setupReveal() {
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-sb-reveal]'));
    if (!items.length) return;

    // Set base class so non-supporting browsers still look fine after a tick.
    items.forEach(function (el) {
      el.classList.add('sb-reveal');
    });

    if (!('IntersectionObserver' in window)) {
      window.setTimeout(function () {
        items.forEach(function (el) { el.classList.add('is-in'); });
      }, 60);
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { root: null, threshold: 0.16 });

    items.forEach(function (el) {
      var d = el.getAttribute('data-sb-reveal-delay');
      if (d) el.setAttribute('data-sb-reveal-delay', String(d));
      io.observe(el);
    });
  }

  function setupCountUp() {
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-sb-count]'));
    if (!items.length) return;

    function animate(el) {
      var rawTarget = el.getAttribute('data-sb-count');
      var target = parseFloat(rawTarget);
      if (!isFinite(target)) return;

      var suffix = el.getAttribute('data-sb-count-suffix') || '';
      var duration = parseInt(el.getAttribute('data-sb-count-duration') || '900', 10);
      var current = parseFloat((el.textContent || '').replace(/[^0-9.\-]/g, ''));
      var start = isFinite(current) ? current : 0;
      var t0 = null;

      function tick(ts) {
        if (t0 === null) t0 = ts;
        var p = Math.min(1, (ts - t0) / duration);
        // Ease-out
        var eased = 1 - Math.pow(1 - p, 3);
        var value = start + (target - start) * eased;
        var out = (target % 1 === 0) ? Math.round(value).toString() : value.toFixed(1);
        el.textContent = out + suffix;
        if (p < 1) requestAnimationFrame(tick);
      }

      requestAnimationFrame(tick);
    }

    if (!('IntersectionObserver' in window)) {
      items.forEach(animate);
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        animate(entry.target);
        io.unobserve(entry.target);
      });
    }, { threshold: 0.35 });

    items.forEach(function (el) {
      io.observe(el);
    });
  }

  function init() {
    setupReveal();
    setupCountUp();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

(function () {
  function setupSliderButtons() {
    function scrollByCard(container, direction) {
      if (!container) return;
      var firstCard = container.querySelector('.sb-card-slide, .sb-hscroll-item');
      var cardWidth = firstCard ? firstCard.getBoundingClientRect().width : 320;
      var gap = 14;
      var amount = (cardWidth + gap) * 1.2;
      container.scrollBy({ left: direction * amount, behavior: 'smooth' });
    }

    document.querySelectorAll('[data-sb-slider-prev]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var sel = btn.getAttribute('data-sb-slider-prev');
        var el = document.querySelector(sel);
        scrollByCard(el, -1);
      });
    });

    document.querySelectorAll('[data-sb-slider-next]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var sel = btn.getAttribute('data-sb-slider-next');
        var el = document.querySelector(sel);
        scrollByCard(el, 1);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupSliderButtons);
  } else {
    setupSliderButtons();
  }
})();
