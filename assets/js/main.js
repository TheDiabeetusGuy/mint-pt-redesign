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
