// MINT Physical Therapy — site interactions
document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Mobile menu ---------- */
  var toggle = document.querySelector('.menu-toggle');
  var navLinks = document.querySelector('.nav-links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', function () {
      var open = navLinks.classList.toggle('mobile-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }

  /* ---------- Dropdowns (desktop + mobile click) ---------- */
  var dropdownParents = document.querySelectorAll('.nav-links > li.has-dropdown');
  dropdownParents.forEach(function (li) {
    var btn = li.querySelector('button');
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = li.classList.contains('open');
      dropdownParents.forEach(function (other) {
        other.classList.remove('open');
        other.querySelector('button').setAttribute('aria-expanded', 'false');
      });
      if (!isOpen) {
        li.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });
  document.addEventListener('click', function () {
    dropdownParents.forEach(function (li) {
      li.classList.remove('open');
      li.querySelector('button').setAttribute('aria-expanded', 'false');
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      dropdownParents.forEach(function (li) { li.classList.remove('open'); });
      if (navLinks) navLinks.classList.remove('mobile-open');
      document.body.style.overflow = '';
    }
  });

  /* ---------- Accordions ---------- */
  document.querySelectorAll('.accordion-item').forEach(function (item) {
    var btn = item.querySelector('button');
    var panel = item.querySelector('.panel');
    if (!btn || !panel) return;
    btn.addEventListener('click', function () {
      var isOpen = item.classList.contains('open');
      item.classList.toggle('open', !isOpen);
      panel.style.maxHeight = !isOpen ? panel.scrollHeight + 'px' : '0px';
    });
  });

  /* ---------- Locations page: city list + detail panel ---------- */
  var locList = document.querySelector('.loc-list');
  if (locList) {
    function locLoadMap(panel) {
      var frame = panel.querySelector('iframe[data-src]');
      if (frame) {
        frame.src = frame.getAttribute('data-src');
        frame.removeAttribute('data-src');
      }
    }

    function activateLocation(slug) {
      var targetId = 'loc-' + slug;
      var item = locList.querySelector('.loc-list-item[data-target="' + targetId + '"]');
      var panel = document.getElementById(targetId);
      if (!item || !panel) return false;
      locList.querySelectorAll('.loc-list-item').forEach(function (i) { i.classList.remove('is-active'); });
      item.classList.add('is-active');
      document.querySelectorAll('.loc-detail').forEach(function (d) { d.classList.remove('is-active'); });
      panel.classList.add('is-active');
      locLoadMap(panel);
      return true;
    }

    // On page load: if the URL points at a specific clinic (e.g. from a
    // header link), show that one instead of always defaulting to the first.
    var startSlug = window.location.hash ? window.location.hash.slice(1) : null;
    if (!startSlug || !activateLocation(startSlug)) {
      var defaultPanel = document.querySelector('.loc-detail.is-active');
      if (defaultPanel) locLoadMap(defaultPanel);
    }

    locList.querySelectorAll('.loc-list-item').forEach(function (item) {
      item.addEventListener('click', function () {
        var slug = item.dataset.target.replace(/^loc-/, '');
        history.replaceState(null, '', '#' + slug);
        activateLocation(slug);
      });
    });

    // Clicking a location link in the header while already on this page only
    // changes the URL hash (no reload) — listen for that and switch to match.
    window.addEventListener('hashchange', function () {
      var slug = window.location.hash ? window.location.hash.slice(1) : null;
      if (slug) activateLocation(slug);
    });
  }

  /* ---------- Home hero carousel ---------- */
  var carousel = document.getElementById('homeCarousel');
  if (carousel) {
    var slides = carousel.querySelectorAll('.hc-slide');
    var current = 0;
    var timer = null;

    function showSlide(i) {
      slides.forEach(function (s, idx) {
        s.classList.toggle('is-active', idx === i);
      });
    }

    function next() {
      current = (current + 1) % slides.length;
      showSlide(current);
    }

    function start() {
      if (timer) return;
      timer = setInterval(next, 4000);
    }

    function stop() {
      clearInterval(timer);
      timer = null;
    }

    if (slides.length > 1) {
      start();
      carousel.addEventListener('mouseenter', stop);
      carousel.addEventListener('mouseleave', start);
    }
  }

  /* ---------- Testimonial carousel ---------- */
  var tCarousel = document.getElementById('testimonialCarousel');
  if (tCarousel) {
    var tPages = tCarousel.querySelectorAll('.tc-page');
    var tCurrent = 0;
    var tTimer = null;

    function tShowPage(i) {
      tPages.forEach(function (p, idx) {
        p.classList.toggle('is-active', idx === i);
      });
    }

    function tNext() {
      tCurrent = (tCurrent + 1) % tPages.length;
      tShowPage(tCurrent);
    }

    function tStart() {
      if (tTimer) return;
      tTimer = setInterval(tNext, 4000);
    }

    function tStop() {
      clearInterval(tTimer);
      tTimer = null;
    }

    if (tPages.length > 1) {
      tStart();
      tCarousel.addEventListener('mouseenter', tStop);
      tCarousel.addEventListener('mouseleave', tStart);
    }
  }

  /* ---------- Video placeholders ---------- */
  document.querySelectorAll('.video-frame').forEach(function (frame) {
    frame.addEventListener('click', function () {
      var cap = frame.querySelector('.cap');
      if (cap) cap.textContent = 'Video coming soon';
    });
  });

  /* ---------- Appointment / contact form (front-end only placeholder) ---------- */
  var form = document.getElementById('appointment-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      form.style.display = 'none';
      var success = document.getElementById('form-success');
      if (success) success.style.display = 'block';
      // NOTE for site owner: this form currently only confirms in-page.
      // Connect it to Formspree, Netlify Forms, or your booking system
      // by adding an action/method to the <form id="appointment-form"> tag.
    });
  }

  /* ---------- Active nav link highlight ---------- */
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href && href.split('/').pop() === here && here !== '') {
      a.classList.add('active');
    }
  });
});
