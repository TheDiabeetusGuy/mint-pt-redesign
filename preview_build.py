# -*- coding: utf-8 -*-
"""
Generates 3 standalone preview pages, each showing the same content in a
different color palette, so the client can compare and pick one before we
apply it site-wide. Font + real logo are already final in all 3.

Run: python3 preview_build.py
"""
import os
from build import (
    topo_lines, footer_skyline, elevation_chart, icon,
    SERVICES, TESTIMONIALS, avatar, PHONE_MAIN, PHONE_MAIN_TEL, EMAIL_MAIN
)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "color-previews")

PALETTES = [
    dict(
        key="sage-trail",
        label="1 · Sage Trail",
        blurb="A refined, natural version of the current direction — warm stone neutrals, forest green, a touch of trail-marker gold. Calm and grounded.",
        vars={
            "--stone-50": "#FAF9F4", "--stone-100": "#F1EEE1", "--stone-200": "#E7E2CF",
            "--ink-900": "#1E2A20", "--ink-700": "#3B463C", "--ink-500": "#616D60",
            "--forest-900": "#16301F", "--forest-800": "#1B4128", "--forest-700": "#256B39",
            "--forest-600": "#2E8B49", "--forest-500": "#37A257", "--forest-400": "#5CBE73",
            "--mint-200": "#C7E9C8", "--mint-100": "#E4F2E3", "--mint-050": "#F0F8EE",
            "--gold-600": "#B4791F", "--gold-500": "#E3A94A", "--gold-300": "#F0C878",
        },
    ),
    dict(
        key="mint-charcoal",
        label="2 · Mint Charcoal",
        blurb="Bold and modern — near-black charcoal surfaces, a bright saturated mint, and a coral pop for calls to action. Feels more like a confident, energetic health-tech brand.",
        vars={
            "--stone-50": "#F5F6F3", "--stone-100": "#EAECE7", "--stone-200": "#DCDFD8",
            "--ink-900": "#121815", "--ink-700": "#333B36", "--ink-500": "#5C655E",
            "--forest-900": "#0F1613", "--forest-800": "#16211C", "--forest-700": "#1B3327",
            "--forest-600": "#22B573", "--forest-500": "#2ECE84", "--forest-400": "#5BDE9E",
            "--mint-200": "#B9F0D2", "--mint-100": "#DFF6EA", "--mint-050": "#EFFBF3",
            "--gold-600": "#C24E2E", "--gold-500": "#FF7A59", "--gold-300": "#FFA98D",
        },
    ),
    dict(
        key="meadow-blush",
        label="3 · Meadow Blush",
        blurb="Soft and approachable — fresh meadow green, warm blush accent, buttery highlight. Feels friendlier and a little more wellness-spa than clinical.",
        vars={
            "--stone-50": "#FBF7F4", "--stone-100": "#F3EBE4", "--stone-200": "#EADDD2",
            "--ink-900": "#2B332C", "--ink-700": "#48504A", "--ink-500": "#707A71",
            "--forest-900": "#28402F", "--forest-800": "#325038", "--forest-700": "#3A7A4D",
            "--forest-600": "#3FA66B", "--forest-500": "#4CBB79", "--forest-400": "#72CC94",
            "--mint-200": "#CDE9D5", "--mint-100": "#EAF5EC", "--mint-050": "#F4FAF5",
            "--gold-600": "#C46B60", "--gold-500": "#E98F86", "--gold-300": "#F3C0BA",
        },
    ),
]

def vars_block(v):
    return "\n".join(f"  {k}: {val} !important;" for k, val in v.items())

def preview_page(p):
    top_services = SERVICES[:4]
    body = f'''
  <header class="site-header">
    <div class="container nav">
      <a href="#" class="brand"><img src="../assets/img/logo.png" alt="MINT Physical Therapy" class="brand-logo"></a>
      <nav aria-label="Primary">
        <ul class="nav-links">
          <li><a class="active" href="#">Home</a></li>
          <li><a href="#">Locations</a></li>
          <li><a href="#">Our Providers</a></li>
          <li><a href="#">Services</a></li>
          <li><a href="#">Contact</a></li>
        </ul>
      </nav>
      <div class="nav-cta">
        <a class="btn btn-primary btn-sm" href="#">Request Appointment</a>
      </div>
    </div>
  </header>

  <section class="hero">
    {topo_lines(seed=1)}
    <div class="container hero-inner">
      <div>
        <div class="eyebrow on-dark">Mobile &amp; In-Clinic Physical Therapy &middot; Utah</div>
        <h1>Every step back starts with <em>one</em> good one.</h1>
        <p class="lead">One-on-one physical therapy &mdash; in one of our nine Utah clinics, or at your own front door.</p>
        <div class="hero-badges">
          <span class="hero-badge"><b>M</b>ove</span>
          <span class="hero-badge"><b>I</b>mprove</span>
          <span class="hero-badge"><b>N</b>urture</span>
          <span class="hero-badge"><b>T</b>each</span>
        </div>
        <div class="hero-cta">
          <a class="btn btn-gold" href="#">Request an Appointment</a>
          <a class="btn btn-outline on-dark" href="#">{icon('phone')} Call {PHONE_MAIN}</a>
        </div>
      </div>
      <div class="summit-card">
        {elevation_chart()}
        <div class="summit-legend">
          <div><b>Session 1</b>Where you start</div>
          <div style="text-align:right;"><b>Pain-Free</b>Where we&rsquo;re headed</div>
        </div>
      </div>
    </div>
    <div class="hero-strip">
      <div class="container stat-strip">
        <div><div class="num">9</div><div class="lbl">Clinics across Utah</div></div>
        <div><div class="num">1:1</div><div class="lbl">Time with your therapist</div></div>
        <div><div class="num">16+</div><div class="lbl">Providers &amp; specialists</div></div>
        <div><div class="num">Ogden&ndash;Payson</div><div class="lbl">Mobile visit coverage</div></div>
      </div>
    </div>
  </section>

  <section class="section bg-stone">
    <div class="container">
      <div class="section-head">
        <div class="eyebrow">What We Treat</div>
        <h2>Specialized care for the injuries that slow you down.</h2>
      </div>
      <div class="grid-4">
        {''.join(f'''<a class="card-service" href="#"><div class="ico-wrap">{icon(s['icon'])}</div><h3>{s['title']}</h3><p>{s['card']}</p><span class="go">Learn more {icon('arrow-right')}</span></a>''' for s in top_services)}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head center">
        <div class="eyebrow" style="justify-content:center;">Patient Stories</div>
        <h2>Real progress, in their own words.</h2>
      </div>
      <div class="grid-4">
        {''.join(f'''<div class="testimonial"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>&ldquo;{t['quote']}&rdquo;</p><div class="who">{avatar(t['name'],36,13)}<div><b>{t['name']}</b><span>{t['meta']}</span></div></div></div>''' for t in TESTIMONIALS)}
      </div>
    </div>
  </section>

  <section class="section bg-stone">
    <div class="container">
      <div class="cta-band">
        <div>
          <h2>Ready to start feeling like yourself again?</h2>
          <p>Tell us what&rsquo;s going on and we&rsquo;ll help you find the right provider, clinic, or mobile visit.</p>
        </div>
        <div class="actions">
          <a class="btn btn-gold" href="#">Request Appointment</a>
          <a class="btn btn-outline on-dark" href="#">{icon('phone')} {PHONE_MAIN}</a>
        </div>
      </div>
    </div>
  </section>

  <footer class="site-footer">
    <div class="container footer-top">
      <div class="footer-grid">
        <div>
          <div class="footer-brand"><img src="../assets/img/logo.png" alt="MINT Physical Therapy" class="footer-logo"></div>
          <p style="max-width:280px;font-size:14.5px;">Utah-based, one-on-one physical therapy &mdash; in one of our clinics, or at your door.</p>
          <div class="footer-social">
            <a href="#" aria-label="Facebook">{icon("facebook")}</a>
            <a href="#" aria-label="Instagram">{icon("instagram")}</a>
            <a href="#" aria-label="YouTube">{icon("youtube")}</a>
            <a href="#" aria-label="Spotify">{icon("spotify")}</a>
          </div>
        </div>
        <div class="footer-col">
          <h4>Get in Touch</h4>
          <ul>
            <li><a href="#">{PHONE_MAIN}</a></li>
            <li><a href="#">{EMAIL_MAIN}</a></li>
            <li><a href="#">Request an Appointment</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="container footer-bottom">
      <span>&copy; 2026 MINT Physical Therapy. All rights reserved.</span>
      <span>Move &middot; Improve &middot; Nurture &middot; Teach</span>
    </div>
    {footer_skyline()}
  </footer>
'''

    other_links = "".join(
        f'<a href="{o["key"]}.html" class="swatch-link{" current" if o["key"]==p["key"] else ""}">{o["label"]}</a>'
        for o in PALETTES
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Preview: {p['label']} | MINT Physical Therapy</title>
<link rel="stylesheet" href="../assets/css/style.css">
<style>
  :root {{
{vars_block(p['vars'])}
  }}
  .preview-bar{{
    position:sticky; top:0; z-index:200; background:#fff; border-bottom:2px solid var(--ink-900);
    padding:14px clamp(20px,5vw,64px); display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:14px;
    font-family: var(--f-body);
  }}
  .preview-bar h4{{ font-family:var(--f-display); font-size:16px; margin:0; }}
  .preview-bar p{{ font-size:13px; color:var(--ink-500); max-width:520px; margin:4px 0 0; }}
  .swatch-links{{ display:flex; gap:8px; flex-wrap:wrap; }}
  .swatch-link{{ font-size:13px; font-weight:600; padding:8px 14px; border-radius:100px; border:1.5px solid var(--line); color:var(--ink-700); }}
  .swatch-link.current{{ background:var(--forest-600); color:#fff; border-color:var(--forest-600); }}
</style>
</head>
<body>
<div class="preview-bar">
  <div>
    <h4>{p['label']}</h4>
    <p>{p['blurb']}</p>
  </div>
  <div class="swatch-links">{other_links}</div>
</div>
{body}
</body>
</html>'''

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for p in PALETTES:
        path = os.path.join(OUT_DIR, f"{p['key']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(preview_page(p))
        print("wrote", path)

if __name__ == "__main__":
    main()
