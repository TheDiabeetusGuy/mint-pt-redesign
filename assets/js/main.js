// MINT Physical Therapy — site interactions
document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Mobile menu ---------- */
  var toggle = document.querySelector('.menu-toggle');
  var navLinks = document.querySelector('.nav-links');
  var menuScrollY = 0;

  /* ---------- Mobile header: follows the swipe in real time ---------- */
  // Desktop keeps the header always visible (sticky); this only runs at
  // mobile widths. Rather than waiting for a scroll-distance threshold
  // before snapping the header away, it tracks the header's hidden
  // amount 1:1 with the scroll delta, so it slides out/in exactly as
  // fast as you swipe. Once scrolling settles, it snaps to fully shown
  // or fully hidden, whichever it's closer to.
  (function () {
    var header = document.querySelector('.site-header');
    if (!header) return;
    var lastY = window.scrollY || window.pageYOffset || 0;
    var hidden = 0; // 0 = fully shown, header height = fully hidden
    var ticking = false;
    var settleTimer = null;

    function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
    function apply(withTransition) {
      header.style.transition = withTransition ? 'transform .2s ease' : 'none';
      header.style.transform = 'translateY(' + (-hidden) + 'px)';
    }

    function onScroll() {
      var mobile = window.matchMedia('(max-width: 980px)').matches;
      var menuOpen = navLinks && navLinks.classList.contains('mobile-open');
      var y = window.scrollY || window.pageYOffset || 0;
      if (!mobile || menuOpen) {
        hidden = 0;
        apply(true);
        lastY = y;
        ticking = false;
        return;
      }
      var h = header.offsetHeight;
      var delta = y - lastY;
      lastY = y;
      hidden = y <= 0 ? 0 : clamp(hidden + delta, 0, h);
      apply(false);
      ticking = false;

      clearTimeout(settleTimer);
      settleTimer = setTimeout(function () {
        hidden = hidden > h / 2 ? h : 0;
        apply(true);
      }, 120);
    }

    window.addEventListener('scroll', function () {
      if (!ticking) {
        window.requestAnimationFrame(onScroll);
        ticking = true;
      }
    }, { passive: true });
  })();

  // Prevents the background page from scrolling while the mobile menu is
  // open. Deliberately NOT using body{overflow:hidden} — on iOS Safari that
  // snaps the scroll position back to 0, which is why the menu used to
  // appear "at the top of the page" when opened partway down. Locking the
  // body in place at its current scroll position avoids that entirely, so
  // the menu opens exactly where you were.
  function lockBodyScroll() {
    menuScrollY = window.scrollY || window.pageYOffset || 0;
    document.body.style.position = 'fixed';
    document.body.style.top = (-menuScrollY) + 'px';
    document.body.style.left = '0';
    document.body.style.right = '0';
  }
  function unlockBodyScroll() {
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.left = '';
    document.body.style.right = '';
    window.scrollTo(0, menuScrollY);
  }

  if (toggle && navLinks) {
    toggle.addEventListener('click', function () {
      var open = navLinks.classList.toggle('mobile-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) { lockBodyScroll(); } else { unlockBodyScroll(); }
    });
  }

  /* ---------- Dropdowns (desktop + mobile click) ---------- */
  var dropdownParents = document.querySelectorAll('.nav-links > li.has-dropdown');

  // Forces the flattened mobile look directly on the element, bypassing
  // the stylesheet entirely. Used as a hard guarantee that the dropdown
  // never renders as the floating desktop card on small screens,
  // regardless of any CSS cascade/caching issue.
  function forceMobileDropdownLayout(dropdownEl) {
    if (!dropdownEl) return;
    var props = {
      'position': 'static', 'transform': 'none', 'box-shadow': 'none',
      'border': 'none', 'border-radius': '0', 'max-width': '100%',
      'width': '100%', 'min-width': '0', 'left': 'auto'
    };
    Object.keys(props).forEach(function (k) {
      dropdownEl.style.setProperty(k, props[k], 'important');
    });
  }
  function clearForcedDropdownLayout(dropdownEl) {
    if (dropdownEl) dropdownEl.removeAttribute('style');
  }

  dropdownParents.forEach(function (li) {
    var btn = li.querySelector('button');
    var dropdownEl = li.querySelector('.dropdown');
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = li.classList.contains('open');
      dropdownParents.forEach(function (other) {
        other.classList.remove('open');
        other.querySelector('button').setAttribute('aria-expanded', 'false');
        clearForcedDropdownLayout(other.querySelector('.dropdown'));
      });
      if (!isOpen) {
        li.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
        if (window.matchMedia('(max-width: 980px)').matches) {
          forceMobileDropdownLayout(dropdownEl);
        }
      }
    });

    // "Services" is split into a label (links to the hub page) and a
    // separate toggle button, so hovering + clicking a specific service
    // works on desktop. On mobile there's no hover, so tapping the label
    // should behave exactly like every other mobile dropdown (Locations
    // included) and just open the list — not navigate away immediately.
    if (li.classList.contains('split')) {
      var label = li.querySelector(':scope > a');
      if (label) {
        label.addEventListener('click', function (e) {
          if (window.matchMedia('(max-width: 980px)').matches) {
            e.preventDefault();
            e.stopPropagation();
            btn.click();
          }
        });
      }
    }
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
      if (navLinks && navLinks.classList.contains('mobile-open')) {
        navLinks.classList.remove('mobile-open');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
        unlockBodyScroll();
      }
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
      btn.setAttribute('aria-expanded', !isOpen ? 'true' : 'false');
      panel.style.maxHeight = !isOpen ? panel.scrollHeight + 'px' : '0px';
    });
  });

  /* ---------- Locations page: city list + detail panel ---------- */
  var locList = document.querySelector('.loc-list');
  if (locList) {
    var locMobileSelect = document.getElementById('locMobileSelect');

    function locLoadMap(panel) {
      var frame = panel.querySelector('iframe[data-src]');
      if (frame) {
        frame.src = frame.getAttribute('data-src');
        frame.removeAttribute('data-src');
      }
    }

    function showPanel(panel) {
      document.querySelectorAll('.loc-detail').forEach(function (d) {
        d.classList.remove('is-active', 'is-visible');
      });
      panel.classList.add('is-active');
      locLoadMap(panel);
      // Force layout so the browser registers the starting (invisible) state
      // before switching it to visible — otherwise it just snaps straight in.
      void panel.offsetWidth;
      requestAnimationFrame(function () {
        panel.classList.add('is-visible');
      });
    }

    function activateLocation(slug) {
      var targetId = 'loc-' + slug;
      var item = locList.querySelector('.loc-list-item[data-target="' + targetId + '"]');
      var panel = document.getElementById(targetId);
      if (!item || !panel) return false;
      if (locMobileSelect) locMobileSelect.value = slug;
      if (panel.classList.contains('is-active')) return true;

      locList.querySelectorAll('.loc-list-item').forEach(function (i) { i.classList.remove('is-active'); });
      item.classList.add('is-active');

      var current = document.querySelector('.loc-detail.is-active');
      if (current && current !== panel) {
        current.classList.remove('is-visible');
        window.setTimeout(function () { showPanel(panel); }, 220);
      } else {
        showPanel(panel);
      }
      return true;
    }

    // On page load: if the URL points at a specific clinic (e.g. from a
    // header link), show that one instead of always defaulting to the first.
    // Ogden ships pre-marked active in the raw HTML (so the page still looks
    // right before JS runs) — that has to be cleared before switching, or
    // both Ogden and the target clinic end up visible at once.
    var startSlug = window.location.hash ? window.location.hash.slice(1) : null;
    var startPanel = (startSlug && document.getElementById('loc-' + startSlug)) || document.querySelector('.loc-detail.is-active');
    document.querySelectorAll('.loc-detail').forEach(function (d) { d.classList.remove('is-active', 'is-visible'); });
    locList.querySelectorAll('.loc-list-item').forEach(function (i) { i.classList.remove('is-active'); });
    var startItem = startSlug
      ? locList.querySelector('.loc-list-item[data-target="loc-' + startSlug + '"]')
      : locList.querySelector('.loc-list-item');
    if (startItem) startItem.classList.add('is-active');
    if (startPanel) {
      startPanel.classList.add('is-active', 'is-visible');
      locLoadMap(startPanel);
    }
    if (locMobileSelect && startItem) {
      locMobileSelect.value = startItem.dataset.target.replace(/^loc-/, '');
    }

    locList.querySelectorAll('.loc-list-item').forEach(function (item) {
      item.addEventListener('click', function () {
        var slug = item.dataset.target.replace(/^loc-/, '');
        history.replaceState(null, '', '#' + slug);
        activateLocation(slug);
      });
    });

    if (locMobileSelect) {
      locMobileSelect.addEventListener('change', function () {
        var slug = locMobileSelect.value;
        history.replaceState(null, '', '#' + slug);
        activateLocation(slug);
      });
    }

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

  /* ---------- Providers page: DPT / PTA tabs ---------- */
  document.querySelectorAll('.prov-tabs').forEach(function (tabs) {
    var buttons = tabs.querySelectorAll('.prov-tab');
    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var targetId = btn.dataset.tabTarget;
        buttons.forEach(function (b) {
          var isMatch = b === btn;
          b.classList.toggle('is-active', isMatch);
          b.setAttribute('aria-selected', isMatch ? 'true' : 'false');
        });
        document.querySelectorAll('.prov-tab-panel').forEach(function (panel) {
          var isMatch = panel.id === targetId;
          panel.classList.toggle('is-active', isMatch);
          panel.hidden = !isMatch;
          // Coming back to a tab restarts its auto-cycle (desktop list or
          // mobile carousel, whichever applies) if it had stopped — only
          // leaving the page (or a real refresh) should otherwise do that.
          if (isMatch) {
            var shownSection = panel.querySelector('.prov-list-section');
            if (shownSection && shownSection._resetAutoCycle) shownSection._resetAutoCycle();
            if (shownSection && shownSection._resetCarousel) shownSection._resetCarousel();
          }
        });
      });
    });
  });

  /* ---------- Providers page: hover-preview / click-to-pin list + detail panel ---------- */
  document.querySelectorAll('.prov-list-section').forEach(function (section) {
    var list = section.querySelector('.prov-list');
    var wrap = section.querySelector('.prov-detail-wrap');
    if (!list || !wrap) return;

    var items = list.querySelectorAll('.prov-list-item');
    var startItem = list.querySelector('.prov-list-item.is-active') || items[0];
    var pinnedTarget = startItem ? startItem.dataset.target : null;
    var activeTarget = pinnedTarget;
    var switchTimer = null;

    // Makes `next` the only visible/active panel. Defensive: clears is-active
    // from every other panel (not just the one we think is current), so a
    // stray double-active state from an interrupted transition can't persist.
    function activateNow(next) {
      wrap.querySelectorAll('.prov-detail.is-active').forEach(function (el) {
        if (el !== next) el.classList.remove('is-active', 'is-visible');
      });
      next.classList.add('is-active');
      void next.offsetWidth;
      requestAnimationFrame(function () { next.classList.add('is-visible'); });
    }

    function showPanel(targetId) {
      if (!targetId || targetId === activeTarget) return;
      // Cancel any transition still in flight from a previous hover before
      // starting a new one — otherwise fast mouse movement across several
      // list items queues up multiple timers that each activate their own
      // panel, leaving more than one visible at once.
      if (switchTimer) { clearTimeout(switchTimer); switchTimer = null; }
      var next = document.getElementById(targetId);
      if (!next) return;
      var current = wrap.querySelector('.prov-detail.is-active');
      activeTarget = targetId;
      if (current && current !== next) {
        current.classList.remove('is-visible');
        switchTimer = window.setTimeout(function () {
          switchTimer = null;
          activateNow(next);
        }, 180);
      } else {
        activateNow(next);
      }
    }

    function applyPin(item) {
      pinnedTarget = item.dataset.target;
      items.forEach(function (i) { i.classList.toggle('is-active', i === item); });
      showPanel(pinnedTarget);
    }

    function pauseAutoCycle() {
      if (autoCycleTimer) { clearInterval(autoCycleTimer); autoCycleTimer = null; }
    }

    function startAutoCycle() {
      if (autoCycleStopped || items.length <= 1 || autoCycleTimer) return;
      autoCycleTimer = window.setInterval(advanceAuto, 4000);
    }

    // A click (or keyboard select) is a deliberate choice — it pins the
    // provider and permanently stops the auto-cycle for this list. Only a
    // page refresh restarts it. Hovering only pauses it (see below).
    function pinItem(item) {
      autoCycleStopped = true;
      pauseAutoCycle();
      applyPin(item);
    }

    // Advances to the next provider in the list, wrapping around, and
    // highlights it exactly like a click would (green dot + shown bio) —
    // just without stopping the cycle.
    function advanceAuto() {
      var currentIndex = -1;
      items.forEach(function (i, idx) { if (i.dataset.target === pinnedTarget) currentIndex = idx; });
      var nextIndex = (currentIndex + 1) % items.length;
      applyPin(items[nextIndex]);
    }

    var autoCycleTimer = null;
    var autoCycleStopped = false;
    startAutoCycle();

    // Lets the tab-switch handler above fully reset this list whenever its
    // tab is shown again — back to the original starting provider, cycle
    // running fresh, exactly like a first page load. This covers both a
    // click-stopped cycle and one that simply drifted while the tab was
    // hidden; either way, returning to the tab starts over from the top.
    section._resetAutoCycle = function () {
      autoCycleStopped = false;
      pauseAutoCycle();
      applyPin(startItem);
      startAutoCycle();
    };

    items.forEach(function (item) {
      // Hovering previews a provider's bio without changing what's pinned,
      // and pauses the auto-cycle for as long as the mouse stays there;
      // moving away resumes it (unless a click has stopped it for good) and
      // reverts the panel to whichever provider is currently pinned.
      item.addEventListener('mouseenter', function () {
        pauseAutoCycle();
        showPanel(item.dataset.target);
      });
      item.addEventListener('mouseleave', function () {
        showPanel(pinnedTarget);
        startAutoCycle();
      });
      item.addEventListener('click', function () { pinItem(item); });
      item.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          pinItem(item);
        }
      });
      item.addEventListener('focus', function () {
        pauseAutoCycle();
        showPanel(item.dataset.target);
      });
      item.addEventListener('blur', function () {
        showPanel(pinnedTarget);
        startAutoCycle();
      });
    });
  });

  /* ---------- Providers page: mobile carousel (swipe/arrows, auto-advance every 5s) ---------- */
  document.querySelectorAll('.prov-list-section').forEach(function (section) {
    var carousel = section.querySelector('.prov-carousel');
    if (!carousel) return;
    var viewport = carousel.querySelector('.prov-carousel-viewport');
    var slides = carousel.querySelectorAll('.prov-carousel-slide');
    var prevBtn = carousel.querySelector('.prov-carousel-prev');
    var nextBtn = carousel.querySelector('.prov-carousel-next');
    if (!viewport || !slides.length) return;

    var startIndex = 0;
    slides.forEach(function (s, i) { if (s.classList.contains('is-active')) startIndex = i; });
    var currentIndex = startIndex;
    var timer = null;
    var stopped = false;
    var switchTimer = null;

    function positionArrows() {
      if (!prevBtn || !nextBtn) return;
      var activeSlide = carousel.querySelector('.prov-carousel-slide.is-active') || slides[currentIndex];
      var visual = activeSlide.querySelector('.prov-detail-visual');
      if (!visual) return;
      var carouselRect = carousel.getBoundingClientRect();
      var visualRect = visual.getBoundingClientRect();
      var centerY = (visualRect.top - carouselRect.top) + (visualRect.height / 2);
      prevBtn.style.top = centerY + 'px';
      nextBtn.style.top = centerY + 'px';
    }

    // Same crossfade technique as the desktop list/detail panel: fade the
    // outgoing slide out, swap which one is in the document flow, then fade
    // the new one in — smooth regardless of whether it was triggered by an
    // arrow tap, a swipe, or the automatic 5-second advance.
    function activateNow(next) {
      slides.forEach(function (s) { if (s !== next) s.classList.remove('is-active', 'is-visible'); });
      next.classList.add('is-active');
      void next.offsetWidth;
      requestAnimationFrame(function () {
        next.classList.add('is-visible');
        positionArrows();
      });
    }

    function showSlide(index) {
      if (switchTimer) { clearTimeout(switchTimer); switchTimer = null; }
      var next = slides[index];
      var current = carousel.querySelector('.prov-carousel-slide.is-active');
      if (current && current !== next) {
        current.classList.remove('is-visible');
        switchTimer = window.setTimeout(function () {
          switchTimer = null;
          activateNow(next);
        }, 180);
      } else {
        activateNow(next);
      }
    }

    function goTo(index) {
      currentIndex = ((index % slides.length) + slides.length) % slides.length;
      showSlide(currentIndex);
    }

    function next() { goTo(currentIndex + 1); }
    function prev() { goTo(currentIndex - 1); }

    function pause() { if (timer) { clearInterval(timer); timer = null; } }
    function start() {
      if (stopped || slides.length <= 1 || timer) return;
      timer = window.setInterval(next, 5000);
    }

    // Tapping an arrow or starting a swipe is a deliberate interaction — it
    // stops the auto-advance for good, just like a click does on desktop.
    // Only leaving the tab and coming back (or a refresh) restarts it.
    function stopForGood() {
      stopped = true;
      pause();
    }

    if (prevBtn) prevBtn.addEventListener('click', function () { stopForGood(); prev(); });
    if (nextBtn) nextBtn.addEventListener('click', function () { stopForGood(); next(); });

    var touchStartX = null;

    viewport.addEventListener('touchstart', function (e) {
      if (!e.touches || !e.touches.length) return;
      stopForGood();
      touchStartX = e.touches[0].clientX;
    }, { passive: true });

    viewport.addEventListener('touchend', function (e) {
      if (touchStartX === null) return;
      var endX = (e.changedTouches && e.changedTouches[0] && e.changedTouches[0].clientX);
      var dx = (endX === undefined ? touchStartX : endX) - touchStartX;
      var threshold = 40;
      if (dx <= -threshold) next();
      else if (dx >= threshold) prev();
      touchStartX = null;
    });

    window.addEventListener('resize', positionArrows);

    // Lets the tab-switch handler above fully reset this carousel back to
    // its first slide with the cycle running fresh, same as the desktop list.
    section._resetCarousel = function () {
      stopped = false;
      pause();
      goTo(startIndex);
      start();
    };

    positionArrows();
    start();
  });

  /* ---------- Mobile swipe carousels (What We Treat, Our Team, Patient Stories) ---------- */
  document.querySelectorAll('.hz-carousel').forEach(function (carousel) {
    var viewport = carousel.querySelector('.hz-carousel-viewport');
    var track = carousel.querySelector('.hz-carousel-track');
    var slides = carousel.querySelectorAll('.hz-carousel-slide');
    var prevBtn = carousel.querySelector('.hz-carousel-prev');
    var nextBtn = carousel.querySelector('.hz-carousel-next');
    var bars = carousel.querySelectorAll('.hz-carousel-bar');
    if (!viewport || !track || !slides.length) return;

    var currentIndex = 0;
    var timer = null;
    var stopped = false;

    function render(withTransition) {
      var w = viewport.clientWidth;
      track.style.transition = withTransition === false ? 'none' : '';
      track.style.transform = 'translateX(-' + (currentIndex * w) + 'px)';
      slides.forEach(function (s) { s.style.width = w + 'px'; });
      bars.forEach(function (b, i) { b.classList.toggle('is-active', i === currentIndex); });
    }

    function goTo(index) {
      currentIndex = ((index % slides.length) + slides.length) % slides.length;
      render();
    }
    function next() { goTo(currentIndex + 1); }
    function prev() { goTo(currentIndex - 1); }

    function pause() { if (timer) { clearInterval(timer); timer = null; } }
    function start() {
      if (stopped || slides.length <= 1 || timer) return;
      timer = window.setInterval(next, 4000);
    }
    function stopForGood() { stopped = true; pause(); }

    if (prevBtn) prevBtn.addEventListener('click', function () { stopForGood(); prev(); });
    if (nextBtn) nextBtn.addEventListener('click', function () { stopForGood(); next(); });

    var touchStartX = null, dragBase = 0, dragging = false;

    viewport.addEventListener('touchstart', function (e) {
      if (!e.touches || !e.touches.length) return;
      stopForGood();
      dragging = true;
      touchStartX = e.touches[0].clientX;
      dragBase = -currentIndex * viewport.clientWidth;
      track.style.transition = 'none';
    }, { passive: true });

    viewport.addEventListener('touchmove', function (e) {
      if (!dragging || touchStartX === null || !e.touches || !e.touches.length) return;
      var dx = e.touches[0].clientX - touchStartX;
      track.style.transform = 'translateX(' + (dragBase + dx) + 'px)';
    }, { passive: true });

    viewport.addEventListener('touchend', function (e) {
      if (!dragging) return;
      dragging = false;
      var endX = (e.changedTouches && e.changedTouches[0] && e.changedTouches[0].clientX);
      var dx = (endX === undefined ? touchStartX : endX) - touchStartX;
      var threshold = 40;
      if (dx <= -threshold) goTo(currentIndex + 1);
      else if (dx >= threshold) goTo(currentIndex - 1);
      else render();
      touchStartX = null;
    });

    window.addEventListener('resize', function () { render(false); });

    render(false);
    start();
  });

  /* ---------- Home "Our Team" cards: tap-to-reveal bio on touch ---------- */
  // Desktop reveals the overlay on hover via pure CSS. Touch devices have
  // no hover, so tapping a card toggles it open, and tapping anywhere
  // else (another card or the rest of the page) closes it again.
  var teamCards = document.querySelectorAll('.team-section .provider-card.has-bio');
  if (teamCards.length && !window.matchMedia('(hover: hover)').matches) {
    teamCards.forEach(function (card) {
      card.addEventListener('click', function (e) {
        var isOpen = card.classList.contains('is-open');
        teamCards.forEach(function (c) { c.classList.remove('is-open'); });
        if (!isOpen) card.classList.add('is-open');
        e.stopPropagation();
      });
    });
    document.addEventListener('click', function () {
      teamCards.forEach(function (c) { c.classList.remove('is-open'); });
    });
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

  /* ---------- Footer logo: back to top ---------- */
  var footerBrandTop = document.getElementById('footerBrandTop');
  if (footerBrandTop) {
    footerBrandTop.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- Back to top button (home page, mobile only) ---------- */
  // Shows shortly after the user stops scrolling (not while actively
  // scrolling), and only once they've scrolled down a bit. Hides again
  // the instant scrolling resumes, or once back near the top.
  (function () {
    var btn = document.getElementById('scrollTopBtn');
    if (!btn) return;
    var pauseTimer = null;
    var showAfter = 400; // px scrolled before it's eligible to appear
    var pauseDelay = 500; // ms of no scrolling before it pops up

    function onScroll() {
      btn.classList.remove('is-visible');
      clearTimeout(pauseTimer);
      var y = window.scrollY || window.pageYOffset || 0;
      if (y < showAfter) return;
      pauseTimer = setTimeout(function () {
        btn.classList.add('is-visible');
      }, pauseDelay);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      btn.classList.remove('is-visible');
    });
  })();

  /* ---------- Active nav link highlight ---------- */
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href && href.split('/').pop() === here && here !== '') {
      a.classList.add('active');
    }
  });
});
