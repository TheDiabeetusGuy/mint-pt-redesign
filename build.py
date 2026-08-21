# -*- coding: utf-8 -*-
"""
MINT Physical Therapy — static site generator.
Run: python3 build.py
Outputs plain HTML files (no build step needed to view the site —
this script is just a convenience for keeping ~20 pages consistent).
"""
import os, math, re
from icons import icon, ICONS

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_NAME = "MINT Physical Therapy"
PHONE_MAIN = "555-555-5555"
PHONE_MAIN_TEL = "5555555555"
EMAIL_MAIN = "info@mint-pt.com"

# ---------------------------------------------------------------
# Logo mark (recreated as scalable SVG from the client's existing
# two-peak "M" mountain logo, so it stays crisp at every size)
# ---------------------------------------------------------------
def logo_mark(color="#2FA84F", cls="mark"):
    return f'''<svg class="{cls}" viewBox="0 0 60 52" aria-hidden="true">
      <path d="M2 47 L19 7 L27.5 24 L21.5 47 Z" fill="{color}"/>
      <path d="M22 47 L38 12 L54 47 Z" fill="none" stroke="{color}" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/>
      <path d="M4 47h5M5.5 43h4M7 39h3" stroke="{color}" stroke-width="3" stroke-linecap="round"/>
    </svg>'''

# ---------------------------------------------------------------
# Decorative topographic contour lines (the site's signature motif)
# ---------------------------------------------------------------
def topo_lines(seed=0, rows=7, w=1400, h=460, stroke="rgba(255,255,255,.16)", sw=1.2):
    paths = []
    for r in range(rows):
        base_y = (h / (rows + 1)) * (r + 1)
        pts = []
        segs = 14
        amp = 26 + (r % 3) * 10
        phase = seed + r * 0.7
        for s in range(segs + 1):
            x = (w / segs) * s
            y = base_y + math.sin(s * 0.9 + phase) * amp + math.sin(s * 0.35 + phase * 1.4) * (amp * 0.5)
            pts.append((x, y))
        d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(
            f"Q{pts[i][0]:.1f},{pts[i][1]:.1f} {(pts[i][0]+pts[i+1][0])/2:.1f},{(pts[i][1]+pts[i+1][1])/2:.1f}"
            for i in range(len(pts) - 1)
        )
        paths.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}"/>')
    return f'<svg class="hero-topo" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">{"".join(paths)}</svg>'

def footer_skyline():
    return '''<svg class="footer-skyline" viewBox="0 0 1400 160" preserveAspectRatio="none" aria-hidden="true">
      <path d="M0 160 L120 70 220 120 340 40 460 120 600 60 760 130 900 55 1040 120 1180 75 1300 130 1400 90 1400 160 Z" fill="rgba(255,255,255,.04)"/>
      <path d="M0 160 L90 110 200 150 330 90 480 150 640 100 800 155 960 100 1120 150 1260 105 1400 150 1400 160 Z" fill="rgba(255,255,255,.06)"/>
    </svg>'''

def elevation_chart():
    return '''<svg class="elevation-chart" viewBox="0 0 420 220" aria-hidden="true">
      <defs>
        <linearGradient id="ascentFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#54C46E" stop-opacity=".38"/>
          <stop offset="1" stop-color="#54C46E" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <path d="M10 190 L70 165 130 175 190 110 250 130 310 55 370 70 410 20" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="2"/>
      <path d="M10 190 L70 165 130 175 190 110 250 130 310 55 370 70 410 20 L410 210 10 210 Z" fill="url(#ascentFill)"/>
      <path d="M10 190 L70 165 130 175 190 110 250 130 310 55 370 70 410 20" fill="none" stroke="#54C46E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 10"/>
      <circle cx="10" cy="190" r="6" fill="#F0C878"/>
      <circle cx="410" cy="20" r="7" fill="#54C46E" stroke="#0F2216" stroke-width="3"/>
      <text x="4" y="208" fill="rgba(255,255,255,.55)" font-family="IBM Plex Mono, monospace" font-size="11">DAY 1</text>
      <text x="352" y="14" fill="#fff" font-family="IBM Plex Mono, monospace" font-size="11">GOAL</text>
    </svg>'''

# ---------------------------------------------------------------
# Content data
# ---------------------------------------------------------------
LOCATIONS = [
    dict(slug="ogden", name="Ogden Clinic", addr1="533 26th St. #202", city="Ogden, UT 84401",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com"),
    dict(slug="clearfield", name="Clearfield Clinic", addr1="1030 University Park Blvd, Suite 1", city="Clearfield, UT 84015",
         phone="555-555-5555", fax="555-555-5555", email="daviscounty@mint-pt.com"),
    dict(slug="brigham-city", name="Brigham City Clinic", addr1="Call for suite details", city="Brigham City, UT",
         phone=PHONE_MAIN, fax="555-555-5555", email=EMAIL_MAIN),
    dict(slug="murray", name="Murray Clinic", addr1="6095 S Fashion Blvd, STE 120", city="Murray, UT 84107",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com"),
    dict(slug="riverton", name="Riverton Clinic", addr1="12427 4000 W #202", city="Riverton, UT 84096",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com"),
    dict(slug="west-valley-city", name="West Valley City Clinic", addr1="3451 S 5600 W", city="West Valley City, UT 84120",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com"),
    dict(slug="lehi", name="Lehi Clinic", addr1="120 W Main St", city="Lehi, UT 84043",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com"),
    dict(slug="american-fork", name="American Fork Clinic", addr1="476 N 900 W, Suite B", city="American Fork, UT 84003",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com"),
    dict(slug="provo", name="Provo Clinic", addr1="1807 N 1120 W", city="Provo, UT 84604",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com"),
]

SERVICES = [
    dict(slug="back-pain", title="Back Pain", icon="spine",
         card="Relief and long-term strength for acute strains, chronic tension, and everything in between.",
         intro="Back pain can start suddenly or build slowly, and it has a way of shrinking your world — cutting out favorite activities, hobbies, even a good night's sleep. At MINT, we look past the pain itself to find what's actually driving it, then build a plan that gets you moving again with confidence.",
         causes_label="Common Causes",
         causes=["Muscle strain or ligament sprain", "Herniated or bulging discs", "Poor posture and prolonged sitting",
                 "Degenerative changes or spinal stenosis", "Past injury, including auto accidents"],
         approach=["Hands-on manual therapy to ease tension and restore movement", "A personalized strengthening plan for your core and spine",
                   "Posture and body-mechanics coaching for work and home", "Dry needling or other modalities when helpful",
                   "A gradual, guided return to the activities you miss"]),
    dict(slug="sciatica", title="Sciatica", icon="leg",
         card="Calming nerve pain that radiates through the hip, leg, or foot — at the source, not just the symptom.",
         intro="That sharp, shooting pain down your leg has a root cause — usually pressure or irritation somewhere along the sciatic nerve. We find where it starts and treat it there, so relief actually lasts.",
         causes_label="Common Causes",
         causes=["Herniated disc pressing on the nerve", "Spinal stenosis", "Piriformis muscle tightness",
                 "Pregnancy-related nerve pressure", "Prolonged sitting or poor movement patterns"],
         approach=["Targeted nerve-gliding and mobility exercises", "Manual therapy to release tight muscles around the nerve",
                   "Core and hip strengthening to reduce pressure on the spine", "Dry needling for stubborn muscle tension",
                   "Movement coaching to help prevent flare-ups"]),
    dict(slug="chronic-pain", title="Chronic Pain", icon="pulse",
         card="A steady, whole-person plan for pain that's stuck around longer than it should.",
         intro="Pain that lingers for months or years changes how you move, sleep, and live. Our approach treats the whole picture — body and habits together — so you can build momentum instead of just managing symptoms.",
         causes_label="Common Contributors",
         causes=["Old injuries that never fully resolved", "Ongoing inflammation or joint changes", "Nervous system sensitization",
                 "Compensating movement patterns", "Stress, poor sleep, and inactivity feeding the cycle"],
         approach=["A graded activity plan that rebuilds tolerance safely", "Manual therapy to reduce tension and improve mobility",
                   "Education on pain science, so you understand what's happening", "Strength and conditioning tailored to your capacity",
                   "Ongoing check-ins so we can adjust the plan as you improve"]),
    dict(slug="knee-pain", title="Knee Pain", icon="knee",
         card="Stronger, steadier knees — whether it's an old injury, arthritis, or overuse.",
         intro="Knees carry a lot of weight, literally and figuratively. Whether it's a sports injury, post-surgical recovery, or pain that crept in over time, we build the strength and mechanics your knee needs to trust itself again.",
         causes_label="Common Causes",
         causes=["Ligament or meniscus injury", "Overuse or tendinitis", "Osteoarthritis",
                 "Muscle imbalances at the hip or ankle", "Post-surgical stiffness"],
         approach=["Targeted strengthening for the muscles that support the knee", "Manual therapy to restore range of motion",
                   "Gait and movement analysis", "Sport- and activity-specific return-to-motion training",
                   "Bracing or taping guidance when helpful"]),
    dict(slug="shoulder-pain", title="Shoulder Pain", icon="shoulder",
         card="Restoring reach, strength, and sleep-through-the-night comfort to a cranky shoulder.",
         intro="Shoulder pain has a way of showing up in everything — reaching for a cabinet, sleeping on your side, throwing a ball. We rebuild strength and mobility through the whole shoulder complex, not just the sore spot.",
         causes_label="Common Causes",
         causes=["Rotator cuff strain or tear", "Impingement or bursitis", "Frozen shoulder",
                 "Instability or a past dislocation", "Postural strain from desk work"],
         approach=["Manual therapy to restore joint and soft-tissue mobility", "A progressive strengthening program for the rotator cuff and scapula",
                   "Postural correction for lasting relief", "Dry needling for trigger points",
                   "A guided return to lifting, throwing, or reaching overhead"]),
    dict(slug="headaches-migraines", title="Headaches & Migraines", icon="head",
         card="Getting to the root of tension headaches and migraines — often hiding in the neck.",
         intro="Many headaches and migraines are connected to tension and restriction in the neck and upper back. We assess that connection and treat it directly, often bringing relief other approaches miss.",
         causes_label="Common Triggers",
         causes=["Neck and upper-back muscle tension", "Poor posture, especially from screen time", "TMJ dysfunction",
                 "Stress and muscle guarding", "Cervicogenic (neck-related) triggers"],
         approach=["Manual therapy for the neck, jaw, and upper back", "Dry needling for trigger-point release",
                   "Postural retraining for desk and driving habits", "Gentle mobility and strengthening exercises",
                   "Guidance on triggers and self-management between visits"]),
    dict(slug="concussion-tbi", title="Concussion / Mild TBI", icon="brain",
         card="A careful, step-by-step return to clear thinking, balance, and daily life.",
         intro="Recovering from a concussion or mild traumatic brain injury isn't one-size-fits-all. We assess balance, vision, and neck function together, then guide a safe, steady return to school, work, and sport.",
         causes_label="Common Causes",
         causes=["Sports injuries or falls", "Auto accidents", "Workplace incidents",
                 "Repeated head impacts", "Whiplash-associated neck involvement"],
         approach=["Vestibular (balance and dizziness) rehabilitation", "Vision and eye-tracking exercises",
                   "Neck assessment and treatment — a frequent hidden contributor", "Graded exertion protocols to safely rebuild tolerance",
                   "Close coordination with your physician or care team"]),
    dict(slug="long-covid", title="Long COVID / Post-COVID Syndrome", icon="lungs",
         card="Rebuilding stamina and function after long COVID or a tough post-viral recovery.",
         intro="Long COVID and post-viral syndromes can leave you fatigued, short of breath, or simply not yourself. We build a pacing and conditioning plan that respects your limits while steadily expanding them.",
         causes_label="Common Symptoms We Address",
         causes=["Post-viral fatigue and deconditioning", "Breathing pattern changes", "Reduced cardiovascular tolerance",
                 "Muscle weakness from extended rest", "Post-exertional symptom flare-ups"],
         approach=["Careful, symptom-guided pacing that avoids overexertion", "Breathing retraining exercises",
                   "Gradual cardiovascular and strength reconditioning", "Energy conservation strategies for daily life",
                   "Ongoing monitoring so we adjust before you crash"]),
    dict(slug="dry-needling", title="Dry Needling", icon="needle",
         card="A thin-needle technique that releases tight, irritable muscle knots fast.",
         intro="Dry needling targets the small, contracted knots in muscle tissue — often called trigger points — that cause pain, stiffness, and referred discomfort elsewhere in the body. It's a precise, effective tool we use alongside hands-on and exercise-based care.",
         causes_label="Commonly Used For",
         causes=["Muscle tightness and trigger points", "Chronic tension patterns", "Sports-related muscle strain",
                 "Headaches originating in the neck and shoulders", "Slow-healing overuse injuries"],
         approach=["A focused evaluation to find the muscles driving your pain", "Thin filament needles placed directly into trigger points",
                   "Often paired with stretching or strengthening the same visit", "Fast, targeted relief for stubborn muscle tension",
                   "A clear plan for how many sessions typically help"]),
    dict(slug="winback-diathermy", title="WinBack Diathermy", icon="waves",
         card="Deep, therapeutic heat that speeds tissue healing and eases stiffness.",
         intro="WinBack diathermy uses a gentle electromagnetic current to generate heat deep inside muscle and connective tissue — well beyond what a heating pad can reach — to boost circulation, ease pain, and accelerate recovery.",
         causes_label="Well Suited For",
         causes=["Muscle stiffness and chronic tightness", "Slow-healing soft-tissue injuries", "Pre-exercise warm-up for injured areas",
                 "Scar tissue and post-surgical stiffness", "Pain that responds well to heat"],
         approach=["A comfortable, non-invasive treatment — no needles, no downtime", "Increases blood flow to accelerate natural healing",
                   "Often combined with manual therapy or exercise the same visit", "Intensity customized to your tissue and tolerance",
                   "A relaxing addition to your broader treatment plan"]),
    dict(slug="auto-accidents", title="Auto Accident Recovery", icon="car",
         card="Full-picture recovery after a collision, from whiplash to lasting nerve pain.",
         intro="Car accidents can leave injuries that aren't obvious right away — whiplash, joint strain, nerve irritation — that show up hours or days later. We evaluate thoroughly, document your recovery, and work directly with your claim so you can focus on healing.",
         causes_label="What We Treat",
         causes=["Whiplash-associated neck injuries", "Back and joint strain from impact", "Headaches and concussion-like symptoms",
                 "Nerve compression or irritation", "Soft-tissue injury that worsens without early treatment"],
         approach=["A thorough initial evaluation, even if pain seems mild", "A treatment plan tailored to your specific injuries",
                   "Detailed documentation to support your claim", "Coordination with attorneys, case managers, or insurers",
                   "A steady path back to full, pain-free function"]),
    dict(slug="workers-comp", title="Workers' Comp", icon="briefcase",
         card="Getting you back to work safely, with care coordinated around your claim.",
         intro="A workplace injury shouldn't mean uncertainty about your recovery or your paycheck. We work directly with your employer, case manager, and insurance carrier so treatment moves forward without added stress on you.",
         causes_label="What We Treat",
         causes=["Overuse and repetitive strain injuries", "Lifting and back injuries", "Slip, trip, and fall injuries",
                 "Post-surgical work injuries", "Re-aggravated prior injuries"],
         approach=["Direct communication with your case manager and employer", "Functional, work-specific rehabilitation and conditioning",
                   "Clear documentation for your claim", "A safe, graded return-to-work plan",
                   "Advocacy focused on getting you back to full duty"]),
]

EXTRA_SPECIALTIES = ["Active Release Therapy (ASTYM)", "Manual Therapy & Massage", "Occupational Therapy Services",
                      "Orthopedic Certified Specialists", "Return-to-Sport Conditioning", "Sports Medicine",
                      "TMJ/TMD Therapy", "Work Conditioning"]

PROVIDERS = [
    dict(name="Brad Klemetson", cred="PT, DPT", role="Founder & Clinical Director",
         bio="The steady hand behind MINT — patients call him relentless in the best way, staying on a problem until it's actually solved."),
    dict(name="Ryan Rindlesbacher", cred="PT, DPT", role="Physical Therapist",
         bio="Brings a calm, methodical approach to complex cases, breaking recovery into steps that make sense."),
    dict(name="Joseph Zeigler", cred="PT, DPT", role="Physical Therapist · Ogden",
         bio="Focused on function first — getting patients back to the specific movements their life and work demand."),
    dict(name="Christian Bentley", cred="PT, DPT", role="Physical Therapist",
         bio="Blends manual therapy with hands-on coaching, with an eye for the small details that speed recovery."),
    dict(name="Grace Waters", cred="PT, DPT", role="Physical Therapist",
         bio="Brings warmth and patience to every session, with a gift for making a hard recovery feel manageable."),
    dict(name="Adam Gilbert", cred="PT, DPT", role="Physical Therapist · Ogden",
         bio="Direct and encouraging, with a strength-and-conditioning background that shows in his treatment plans."),
    dict(name="Kate Light", cred="PT, DPT", role="Physical Therapist",
         bio="Approaches every patient as an individual, tailoring pace and technique to what actually works for them."),
    dict(name="Casey Snell", cred="PT, DPT", role="Physical Therapist",
         bio="Combines a sharp clinical eye with genuine encouragement — patients leave sessions knowing their why."),
    dict(name="Andrew Mitchell", cred="PT, DPT", role="Physical Therapist",
         bio="Detail-oriented and thorough, with a knack for catching what other evaluations miss."),
    dict(name="Josh", cred="PT, DPT", role="Physical Therapist · Ogden",
         bio="Brings energy and a genuine investment in every patient's progress, session after session."),
    dict(name="Sandy Larson", cred="PTA", role="Physical Therapist Assistant",
         bio="A friendly, familiar face for patients working through their day-to-day exercise progressions."),
    dict(name="Maryn Christensen", cred="PTA", role="Physical Therapist Assistant",
         bio="Keeps sessions upbeat and encouraging, helping patients stay consistent with their home programs."),
    dict(name="Tawny Cruz", cred="PTA", role="Physical Therapist Assistant",
         bio="Brings hands-on care and steady encouragement to every appointment."),
    dict(name="Natoshia Diffendaffer", cred="PTA", role="Physical Therapist Assistant",
         bio="Detail-focused and supportive, helping translate the treatment plan into real daily progress."),
    dict(name="Amber Hankes", cred="PTA", role="Physical Therapist Assistant",
         bio="Patient and thorough, with a talent for putting nervous first-time patients at ease."),
    dict(name="Gabby Willardsen", cred="PTA", role="Physical Therapist Assistant",
         bio="Brings consistency and care to every session, cheering on every bit of progress along the way."),
]

TESTIMONIALS = [
    dict(quote="Brad understands the demands of working with athletes. If my athletes get hurt, I trust him to get them back stronger, not just healed.",
         name="Zachary Gee", meta="Strength & Conditioning Coach"),
    dict(quote="Dr. Brad is the best PT around. Knowledgeable, caring, and he won't stop until you're actually feeling better.",
         name="Nancy Ford", meta="Google Review"),
    dict(quote="After 30 years of chronic back pain from an accident, Dr. Brad gave me my life back. Years later, I'm still moving pain-free.",
         name="Darlene Anderson", meta="Google Review"),
    dict(quote="Brad relieved my neck pain from work and breastfeeding the same day I saw him, then taught me how to keep it that way.",
         name="Julieta Lewellyn", meta="Google Review"),
]

SOCIAL = dict(
    facebook="https://www.facebook.com/p/MINT-Physical-Therapy-100040214448643/",
    instagram="https://www.instagram.com/mint.physicaltherapy/",
    youtube="https://www.youtube.com/@MINTCONDITION1",
    spotify="https://open.spotify.com/show/2oc45lmxIXZNCoSB4jgwGP",
)

# ---------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------
AVATAR_COLORS = ["#1E6B37", "#238C44", "#2FA84F", "#B4791F", "#173B22", "#D79A31"]

def initials(name):
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()

def avatar(name, size=84, font=24):
    idx = sum(ord(c) for c in name) % len(AVATAR_COLORS)
    color = AVATAR_COLORS[idx]
    return f'<div class="avatar" style="width:{size}px;height:{size}px;background:{color};font-size:{font}px;">{initials(name)}</div>'

def maps_href(loc):
    q = f"{loc['name']} {loc.get('addr1','')} {loc['city']}".replace(" ", "+")
    return f"https://www.google.com/maps/search/?api=1&query={q}"

# ---------------------------------------------------------------
# Header / Footer / Base layout
# ---------------------------------------------------------------
def nav_html(depth="", active=""):
    def a(href, label, key):
        cls = ' class="active"' if active == key else ""
        return f'<a href="{depth}{href}"{cls}>{label}</a>'

    loc_links = "".join(f'<a href="{depth}locations.html#{l["slug"]}">{l["name"]}</a>' for l in LOCATIONS)
    svc_links = "".join(f'<a href="{depth}services/{s["slug"]}.html">{s["title"]}</a>' for s in SERVICES)

    return f'''<header class="site-header">
    <div class="container nav">
      <a href="{depth}index.html" class="brand">
        {logo_mark()}
        <span>MINT<small>Physical Therapy</small></span>
      </a>

      <nav aria-label="Primary">
        <ul class="nav-links" id="navLinks">
          <li>{a("index.html", "Home", "home")}</li>
          <li class="has-dropdown">
            <button type="button" aria-haspopup="true">Locations {icon("chev-down", cls="icon chev")}</button>
            <div class="dropdown">{loc_links}</div>
          </li>
          <li>{a("providers.html", "Our Providers", "providers")}</li>
          <li class="has-dropdown">
            <button type="button" aria-haspopup="true">Services {icon("chev-down", cls="icon chev")}</button>
            <div class="dropdown wide">{svc_links}</div>
          </li>
          <li>{a("join-team.html", "Join Our Team", "join")}</li>
          <li>{a("contact.html", "Contact", "contact")}</li>
        </ul>
      </nav>

      <div class="nav-cta">
        <div class="nav-phone">
          <span>Call today</span>
          <b><a href="tel:+1{PHONE_MAIN_TEL}">{PHONE_MAIN}</a></b>
        </div>
        <a class="btn btn-primary btn-sm" href="{depth}contact.html"><span class="long">Request&nbsp;</span>Appointment</a>
        <button class="menu-toggle" aria-label="Open menu" aria-expanded="false">{icon("menu")}</button>
      </div>
    </div>
  </header>'''

def footer_html(depth=""):
    loc_links = "".join(f'<li><a href="{depth}locations.html#{l["slug"]}">{l["name"]}</a></li>' for l in LOCATIONS[:6])
    svc_links = "".join(f'<li><a href="{depth}services/{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES[:7])
    return f'''<footer class="site-footer">
    <div class="container footer-top">
      <div class="footer-grid">
        <div>
          <div class="footer-brand">{logo_mark(color="#54C46E")}<span>MINT Physical Therapy</span></div>
          <p style="max-width:280px;font-size:14.5px;">Utah-based, one-on-one physical therapy — in one of our clinics, or at your door. Mobile visits available from Ogden to Payson.</p>
          <div class="footer-social">
            <a href="{SOCIAL['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">{icon("facebook")}</a>
            <a href="{SOCIAL['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{icon("instagram")}</a>
            <a href="{SOCIAL['youtube']}" target="_blank" rel="noopener" aria-label="YouTube">{icon("youtube")}</a>
            <a href="{SOCIAL['spotify']}" target="_blank" rel="noopener" aria-label="Spotify">{icon("spotify")}</a>
          </div>
        </div>
        <div class="footer-col">
          <h4>Clinics</h4>
          <ul>{loc_links}<li><a href="{depth}locations.html">View all locations &rarr;</a></li></ul>
        </div>
        <div class="footer-col">
          <h4>Services</h4>
          <ul>{svc_links}<li><a href="{depth}services.html">View all services &rarr;</a></li></ul>
        </div>
        <div class="footer-col">
          <h4>Get in Touch</h4>
          <ul>
            <li><a href="tel:+1{PHONE_MAIN_TEL}">{PHONE_MAIN}</a></li>
            <li><a href="mailto:{EMAIL_MAIN}">{EMAIL_MAIN}</a></li>
            <li><a href="{depth}providers.html">Our Providers</a></li>
            <li><a href="{depth}join-team.html">Join Our Team</a></li>
            <li><a href="{depth}contact.html">Request an Appointment</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="container footer-bottom">
      <span>&copy; 2026 MINT Physical Therapy. All rights reserved.</span>
      <span>Move &middot; Improve &middot; Nurture &middot; Teach</span>
    </div>
    {footer_skyline()}
  </footer>'''

def base_page(title, description, body, depth="", active="", extra_head=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | MINT Physical Therapy</title>
<meta name="description" content="{description}">
<link rel="icon" href="{depth}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{depth}assets/css/style.css">
{extra_head}
</head>
<body>
<a href="#main" class="skip-link">Skip to content</a>
{nav_html(depth, active)}
<main id="main">
{body}
</main>
{footer_html(depth)}
<script src="{depth}assets/js/main.js"></script>
</body>
</html>'''

def page_hero(eyebrow, title, lead, crumbs, depth=""):
    crumb_html = " / ".join([f'<a href="{depth}index.html">Home</a>'] + crumbs)
    return f'''<section class="page-hero">
    {topo_lines(seed=3, rows=5)}
    <div class="container">
      <div class="breadcrumb">{crumb_html}</div>
      <div class="eyebrow on-dark" style="margin-top:18px;">{eyebrow}</div>
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
    </div>
  </section>'''

# ---------------------------------------------------------------
# Reusable component builders
# ---------------------------------------------------------------
def service_card(s, depth=""):
    return f'''<a class="card-service" href="{depth}services/{s['slug']}.html">
      <div class="ico-wrap">{icon(s['icon'])}</div>
      <h3>{s['title']}</h3>
      <p>{s['card']}</p>
      <span class="go">Learn more {icon('arrow-right')}</span>
    </a>'''

def testimonial_card(t):
    return f'''<div class="testimonial">
      <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
      <p>&ldquo;{t['quote']}&rdquo;</p>
      <div class="who">{avatar(t['name'], 36, 13)}<div><b>{t['name']}</b><span>{t['meta']}</span></div></div>
    </div>'''

def provider_card(p):
    return f'''<div class="provider-card">
      {avatar(p['name'])}
      <h3>{p['name']}, {p['cred']}</h3>
      <div class="role">{p['role']}</div>
      <p class="bio">{p['bio']}</p>
    </div>'''

def location_card(l, depth=""):
    return f'''<div class="location-card" id="{l['slug']}">
      <div class="map-swatch" style="background:linear-gradient(135deg,var(--mint-100),var(--stone-200));display:flex;align-items:center;justify-content:center;color:var(--forest-600);">
        {icon('pin', cls='icon', extra='style="width:30px;height:30px"')}
      </div>
      <div class="body">
        <h3>{l['name']}</h3>
        <p class="addr">{l['addr1']}<br>{l['city']}</p>
        <div class="meta">
          <span>P {l['phone']}</span>
          <span>F {l['fax']}</span>
          <span>{l['email']}</span>
        </div>
        <div class="actions">
          <a class="btn btn-outline btn-sm" href="{maps_href(l)}" target="_blank" rel="noopener">Directions</a>
          <a class="btn btn-primary btn-sm" href="{depth}contact.html">Book</a>
        </div>
      </div>
    </div>'''

def cta_band(heading, sub, depth=""):
    return f'''<div class="cta-band">
      <div>
        <h2>{heading}</h2>
        <p>{sub}</p>
      </div>
      <div class="actions">
        <a class="btn btn-gold" href="{depth}contact.html">Request Appointment</a>
        <a class="btn btn-outline on-dark" href="tel:+1{PHONE_MAIN_TEL}">{icon('phone')} {PHONE_MAIN}</a>
      </div>
    </div>'''

def video_frame(caption="Video coming soon"):
    return f'''<div class="video-frame" role="button" tabindex="0" aria-label="Play video">
      {topo_lines(seed=4, rows=5, w=800, h=450, stroke="rgba(255,255,255,.12)")}
      <button class="play" aria-hidden="true">{icon('play')}</button>
      <span class="cap">{caption}</span>
    </div>'''

# ---------------------------------------------------------------
# Pages
# ---------------------------------------------------------------
def home_page():
    top_services = SERVICES[:8]
    steps = [
        dict(n="01", title="Reduces pain naturally", text="Hands-on care and targeted movement calm inflammation and pain without relying on medication."),
        dict(n="02", title="Speeds up recovery", text="A plan built around your specific injury gets you back to normal faster than resting and hoping."),
        dict(n="03", title="Prevents future injuries", text="Strengthening the muscles and joints around an injury keeps it from happening again."),
    ]
    body = f'''
  <section class="hero">
    {topo_lines(seed=1)}
    <div class="container hero-inner">
      <div>
        <div class="eyebrow on-dark">Mobile &amp; In-Clinic Physical Therapy &middot; Utah</div>
        <h1>Every step back starts with <em>one</em> good one.</h1>
        <p class="lead">One-on-one physical therapy &mdash; in one of our nine Utah clinics, or at your own front door. We accept cash pay, workers&rsquo; comp, and auto-accident patients, and we don&rsquo;t stop until you&rsquo;re actually feeling better.</p>
        <div class="hero-badges">
          <span class="hero-badge"><b>M</b>ove</span>
          <span class="hero-badge"><b>I</b>mprove</span>
          <span class="hero-badge"><b>N</b>urture</span>
          <span class="hero-badge"><b>T</b>each</span>
        </div>
        <div class="hero-cta">
          <a class="btn btn-gold" href="contact.html">Request an Appointment</a>
          <a class="btn btn-outline on-dark" href="tel:+1{PHONE_MAIN_TEL}">{icon('phone')} Call {PHONE_MAIN}</a>
        </div>
        <div class="hero-callout">
          <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
          <span>Rated 5 stars by patients across the Wasatch Front</span>
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

  <section class="section">
    <div class="container">
      <div class="section-head center">
        <div class="eyebrow" style="justify-content:center;">Why Physical Therapy</div>
        <h2>Three reasons people choose to move first, not last.</h2>
      </div>
      <div class="journey">
        {''.join(f"""<div class="journey-step"><div class="n">{s['n']}</div><h3>{s['title']}</h3><p>{s['text']}</p></div>""" for s in steps)}
      </div>
    </div>
  </section>

  <section class="section bg-stone">
    <div class="container">
      <div class="section-head">
        <div class="eyebrow">What We Treat</div>
        <h2>Specialized care for the injuries that slow you down.</h2>
        <p>From everyday aches to complex, claim-based recovery &mdash; here&rsquo;s where we spend most of our time.</p>
      </div>
      <div class="grid-4">
        {''.join(service_card(s) for s in top_services)}
      </div>
      <div style="margin-top:34px;text-align:center;">
        <a class="btn btn-outline" href="services.html">View All Services &amp; Specialties {icon('arrow-right')}</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container split">
      <div class="panel-art dark">
        {topo_lines(seed=6, rows=6, w=600, h=450, stroke="rgba(84,196,110,.35)")}
        <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">{icon('home-ico', cls='icon', extra='style="width:56px;height:56px;color:#fff;opacity:.9"')}</div>
      </div>
      <div>
        <div class="eyebrow">Mobile Physical Therapy</div>
        <h2 style="font-size:clamp(26px,3.2vw,36px);margin-top:14px;">1:1 treatment in the comfort of your own home or office.</h2>
        <p style="color:var(--ink-500);margin-top:16px;font-size:16px;">No traffic, no waiting room &mdash; just focused, one-on-one care wherever you are. Mobile visits are available from Ogden all the way down to Payson, or you&rsquo;re welcome to join us at any of our nine clinics.</p>
        <ul class="list-check">
          <li>{icon('check')} Full evaluation and treatment, at your location</li>
          <li>{icon('check')} Same high standard of care as our clinics</li>
          <li>{icon('check')} Ideal for busy schedules, mobility limits, or recovery at home</li>
        </ul>
        <div style="margin-top:26px;display:flex;gap:14px;flex-wrap:wrap;">
          <a class="btn btn-primary" href="contact.html">Request a Mobile Visit</a>
          <a class="btn btn-outline" href="locations.html">Or Find a Clinic</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section bg-mint">
    <div class="container">
      <div class="section-head center">
        <div class="eyebrow" style="justify-content:center;">Our Team</div>
        <h2>Sixteen providers. One standard of care.</h2>
        <p>Doctors of Physical Therapy and PTAs across our Utah clinics, all trained in the same hands-on, whole-person approach.</p>
      </div>
      <div class="grid-4">
        {''.join(provider_card(p) for p in PROVIDERS[:8])}
      </div>
      <div style="margin-top:34px;text-align:center;">
        <a class="btn btn-outline" href="providers.html">Meet the Full Team {icon('arrow-right')}</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container podcast-band">
      <div>
        {video_frame("The MINT Condition Podcast")}
      </div>
      <div>
        <div class="eyebrow">Now Streaming</div>
        <h2 style="font-size:clamp(24px,3vw,32px);margin-top:12px;">The MINT Condition Podcast</h2>
        <p style="color:var(--ink-500);margin-top:14px;font-size:16px;">Straight talk on pain, recovery, and the stuff your provider wishes you knew &mdash; hosted by Brad Klemetson. New episodes on YouTube and Spotify.</p>
        <div class="podcast-links">
          <a class="round-link" href="{SOCIAL['youtube']}" target="_blank" rel="noopener" aria-label="Watch on YouTube">{icon('youtube')}</a>
          <a class="round-link" href="{SOCIAL['spotify']}" target="_blank" rel="noopener" aria-label="Listen on Spotify">{icon('spotify')}</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section bg-stone">
    <div class="container">
      <div class="section-head center">
        <div class="eyebrow" style="justify-content:center;">Patient Stories</div>
        <h2>Real progress, in their own words.</h2>
      </div>
      <div class="grid-4">
        {''.join(testimonial_card(t) for t in TESTIMONIALS)}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      {cta_band("Ready to start feeling like yourself again?", "Tell us what&rsquo;s going on and we&rsquo;ll help you find the right provider, clinic, or mobile visit.")}
    </div>
  </section>
'''
    return base_page("Home", "Utah-based mobile and in-clinic physical therapy. One-on-one care across nine Wasatch Front clinics, or right at your door.", body, depth="", active="home")


def locations_page():
    hero = page_hero("Nine Clinics &middot; One Standard of Care", "Find a MINT Clinic Near You",
                      "Walk-in for 1:1 care at any of our nine Wasatch Front locations, or ask about a mobile visit &mdash; we cover Ogden all the way down to Payson.",
                      ["Locations"])
    cards = "".join(location_card(l) for l in LOCATIONS)
    body = f'''{hero}
  <section class="section">
    <div class="container">
      <div class="tag" style="margin-bottom:26px;">{icon('navigate', cls='icon', extra='style="width:15px;height:15px"')} Hours are generally Monday&ndash;Friday, 7am&ndash;6pm. Please call your clinic to confirm.</div>
      <div class="grid-3">
        {cards}
      </div>
    </div>
  </section>
  <section class="section bg-forest">
    <div class="container split">
      <div>
        <div class="eyebrow on-dark">Can&rsquo;t make it in?</div>
        <h2 style="font-size:clamp(26px,3.2vw,36px);margin-top:14px;">We&rsquo;ll come to you instead.</h2>
        <p style="color:rgba(255,255,255,.75);margin-top:16px;font-size:16px;">Mobile physical therapy means the same 1:1 care, delivered at your home or office &mdash; available from Ogden to Payson.</p>
        <a class="btn btn-gold" style="margin-top:24px;" href="contact.html">Request a Mobile Visit</a>
      </div>
      <div class="panel-art dark">{topo_lines(seed=8, rows=6, w=600, h=450, stroke="rgba(84,196,110,.4)")}</div>
    </div>
  </section>
'''
    return base_page("Locations", "Nine MINT Physical Therapy clinics across Utah's Wasatch Front, plus mobile visits from Ogden to Payson.", body, active="locations")


def providers_page():
    hero = page_hero("Meet the Team", "Our Providers",
                      "Doctors of Physical Therapy and PTAs across all nine clinics &mdash; every one of them trained in MINT&rsquo;s hands-on, whole-person approach to recovery.",
                      ["Our Providers"])
    dpts = [p for p in PROVIDERS if p['cred'] == 'PT, DPT']
    ptas = [p for p in PROVIDERS if p['cred'] == 'PTA']
    body = f'''{hero}
  <section class="section">
    <div class="container">
      <div class="section-head">
        <div class="eyebrow">Doctors of Physical Therapy</div>
        <h2>Ten DPTs, one shared philosophy.</h2>
      </div>
      <div class="grid-4">{''.join(provider_card(p) for p in dpts)}</div>
    </div>
  </section>
  <section class="section bg-stone">
    <div class="container">
      <div class="section-head">
        <div class="eyebrow">Physical Therapist Assistants</div>
        <h2>The team keeping your recovery on track.</h2>
      </div>
      <div class="grid-4">{''.join(provider_card(p) for p in ptas)}</div>
    </div>
  </section>
  <section class="section">
    <div class="container">
      {cta_band("Have a provider in mind?", "Tell us who you&rsquo;d like to see, or which clinic works best, and we&rsquo;ll take care of the rest.")}
    </div>
  </section>
'''
    return base_page("Our Providers", "Meet the Doctors of Physical Therapy and PTAs at MINT Physical Therapy across Utah.", body, active="providers")


def services_page():
    hero = page_hero("Specialties", "Services & Specialties",
                      "Twelve focused programs, built from the ground up around the injuries and conditions we see most.",
                      ["Services"])
    chips = "".join(f'<span class="chip">{s}</span>' for s in EXTRA_SPECIALTIES)
    body = f'''{hero}
  <section class="section">
    <div class="container">
      <div class="grid-4">
        {''.join(service_card(s) for s in SERVICES)}
      </div>
    </div>
  </section>
  <section class="section bg-stone">
    <div class="container">
      <div class="section-head">
        <div class="eyebrow">Also Under One Roof</div>
        <h2>A few more ways we help you move better.</h2>
      </div>
      <div class="chip-row">{chips}</div>
    </div>
  </section>
  <section class="section">
    <div class="container">
      {cta_band("Not sure which service fits?", "Tell us what&rsquo;s going on &mdash; we&rsquo;ll match you with the right provider and plan.")}
    </div>
  </section>
'''
    return base_page("Services & Specialties", "MINT Physical Therapy specialties: back pain, sciatica, dry needling, concussion care, auto accident and workers' comp recovery, and more.", body, active="services")


def service_detail_page(s):
    others = [o for o in SERVICES if o['slug'] != s['slug']][:6]
    body = f'''{page_hero("Service", s['title'], s['card'], [f'<a href="../services.html">Services</a>', s['title']], depth="../")}
  <section class="section">
    <div class="container service-layout">
      <div class="service-body">
        <h2>Overview</h2>
        <p>{s['intro']}</p>

        <h2>{s['causes_label']}</h2>
        <ul class="list-check">
          {''.join(f"<li>{icon('check')} {c}</li>" for c in s['causes'])}
        </ul>

        <h2>How MINT Helps</h2>
        <ul class="list-check">
          {''.join(f"<li>{icon('check')} {a}</li>" for a in s['approach'])}
        </ul>

        <div style="margin-top:40px;display:flex;gap:14px;flex-wrap:wrap;">
          <a class="btn btn-primary" href="../contact.html">Request an Appointment</a>
          <a class="btn btn-outline" href="tel:+1{PHONE_MAIN_TEL}">{icon('phone')} {PHONE_MAIN}</a>
        </div>
      </div>

      <aside>
        <div class="sidebar-card">
          <h4>Talk to Someone Now</h4>
          <p style="font-size:14.5px;color:var(--ink-500);margin-bottom:14px;">Cash pay, workers&rsquo; comp, and auto-accident patients all welcome.</p>
          <a class="btn btn-primary btn-block" href="../contact.html">Request Appointment</a>
        </div>
        <div class="sidebar-card">
          <h4>Related Services</h4>
          <ul class="other-services">
            {''.join(f'<li><a href="{o["slug"]}.html">{o["title"]} {icon("arrow-right", extra="style=&quot;width:14px;height:14px&quot;")}</a></li>' for o in others)}
          </ul>
        </div>
      </aside>
    </div>
  </section>
'''
    return base_page(s['title'], f"{s['title']} treatment at MINT Physical Therapy: {s['card']}", body, depth="../", active="services")


def contact_page():
    hero = page_hero("We&rsquo;d Love to Help", "Contact / Request an Appointment",
                      "Fill out the form and our team will reach out to schedule your visit &mdash; in-clinic or mobile. Prefer to talk now? Give us a call.",
                      ["Contact"])
    loc_options = "".join(f'<option>{l["name"]}</option>' for l in LOCATIONS)
    body = f'''{hero}
  <section class="section">
    <div class="container split" style="align-items:start;">
      <div>
        <div class="form-card">
          <form id="appointment-form">
            <div class="form-row">
              <div class="field"><label>First Name <span class="req">*</span></label><input type="text" required></div>
              <div class="field"><label>Last Name <span class="req">*</span></label><input type="text" required></div>
            </div>
            <div class="form-row">
              <div class="field"><label>Email <span class="req">*</span></label><input type="email" required></div>
              <div class="field"><label>Phone <span class="req">*</span></label><input type="tel" required></div>
            </div>
            <div class="field">
              <label>Preferred Clinic</label>
              <select><option>Mobile visit (Ogden&ndash;Payson)</option>{loc_options}</select>
            </div>
            <div class="field"><label>What&rsquo;s going on?</label><textarea placeholder="Tell us a bit about your injury or goals"></textarea></div>
            <button class="btn btn-primary btn-block" type="submit">Request Appointment</button>
            <p class="form-note">By submitting, you agree to be contacted by MINT Physical Therapy about scheduling. We never share your information.</p>
          </form>
          <div class="form-success" id="form-success">
            <div class="icon-wrap">{icon('check')}</div>
            <h3>Thanks &mdash; we&rsquo;ve got it!</h3>
            <p style="color:var(--ink-500);margin-top:10px;">A member of our team will reach out shortly to confirm your appointment. Need us sooner? Call {PHONE_MAIN}.</p>
          </div>
        </div>
      </div>
      <div>
        <div class="sidebar-card">
          <h4>MINT Physical Therapy</h4>
          <p style="font-size:15px;margin-bottom:14px;">Phone: <a href="tel:+1{PHONE_MAIN_TEL}">{PHONE_MAIN}</a><br>Email: <a href="mailto:{EMAIL_MAIN}">{EMAIL_MAIN}</a></p>
          <p style="font-size:14.5px;color:var(--ink-500);">Mobile visits available from Ogden to Payson. Cash pay, workers&rsquo; comp, and auto-accident patients all welcome.</p>
        </div>
        <div class="sidebar-card">
          <h4>Our Clinics</h4>
          <ul class="other-services">
            {''.join(f'<li><a href="locations.html#{l["slug"]}">{l["name"]} {icon("arrow-right", extra="style=&quot;width:14px;height:14px&quot;")}</a></li>' for l in LOCATIONS)}
          </ul>
        </div>
        <div class="sidebar-card">
          <h4>Follow Along</h4>
          <div class="footer-social" style="margin-top:0;">
            <a href="{SOCIAL['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">{icon('facebook')}</a>
            <a href="{SOCIAL['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{icon('instagram')}</a>
            <a href="{SOCIAL['youtube']}" target="_blank" rel="noopener" aria-label="YouTube">{icon('youtube')}</a>
            <a href="{SOCIAL['spotify']}" target="_blank" rel="noopener" aria-label="Spotify">{icon('spotify')}</a>
          </div>
        </div>
      </div>
    </div>
  </section>
'''
    return base_page("Contact", "Request an appointment with MINT Physical Therapy — in-clinic or mobile visits across Utah's Wasatch Front.", body, active="contact")


def join_team_page():
    hero = page_hero("We&rsquo;re Hiring", "Join Our Team",
                      "MINT is growing across the Wasatch Front, and we&rsquo;re always looking for clinicians who treat patients like people, not appointments.",
                      ["Join Our Team"])
    perks = [
        dict(icon="heart", title="Patient-first culture", text="1:1 appointments mean real time with every patient — no double-booking, no rushing."),
        dict(icon="users", title="A team that mentors", text="Work alongside experienced DPTs across specialties, from dry needling to concussion care."),
        dict(icon="target", title="Room to specialize", text="Pursue certifications and focus areas that fit where you want your career to go."),
        dict(icon="award", title="Growing together", text="Nine clinics and counting across Utah, with the mobile care model built into how we work."),
    ]
    body = f'''{hero}
  <section class="section">
    <div class="container">
      <div class="grid-4">
        {''.join(f'''<div class="card-service"><div class="ico-wrap">{icon(p["icon"])}</div><h3>{p["title"]}</h3><p>{p["text"]}</p></div>''' for p in perks)}
      </div>
    </div>
  </section>
  <section class="section bg-stone">
    <div class="container split">
      <div>
        <div class="eyebrow">Open Roles</div>
        <h2 style="font-size:clamp(26px,3.2vw,36px);margin-top:14px;">Current openings</h2>
        <p style="color:var(--ink-500);margin-top:14px;font-size:16px;">We&rsquo;re currently hiring Doctors of Physical Therapy and PTAs across several Wasatch Front clinics. Don&rsquo;t see your exact fit? Reach out anyway &mdash; we&rsquo;re growing fast.</p>
        <ul class="list-check">
          <li>{icon('check')} Physical Therapist, DPT &mdash; multiple clinics</li>
          <li>{icon('check')} Physical Therapist Assistant, PTA &mdash; multiple clinics</li>
          <li>{icon('check')} Case Manager / Front Office &mdash; Davis County</li>
        </ul>
        <a class="btn btn-primary" style="margin-top:26px;" href="mailto:{EMAIL_MAIN}?subject=Career%20Interest">Send Us Your Resume</a>
      </div>
      <div class="panel-art">{topo_lines(seed=9, rows=6, w=600, h=450, stroke="rgba(35,140,68,.35)")}</div>
    </div>
  </section>
'''
    return base_page("Join Our Team", "Careers at MINT Physical Therapy — open Doctor of Physical Therapy and PTA roles across Utah.", body, active="join")


# ---------------------------------------------------------------
# Write files
# ---------------------------------------------------------------
def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)

def main():
    write("index.html", home_page())
    write("locations.html", locations_page())
    write("providers.html", providers_page())
    write("services.html", services_page())
    write("contact.html", contact_page())
    write("join-team.html", join_team_page())
    for s in SERVICES:
        write(f"services/{s['slug']}.html", service_detail_page(s))

    fav = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 52">
      <path d="M2 47 L19 7 L27.5 24 L21.5 47 Z" fill="#2FA84F"/>
      <path d="M22 47 L38 12 L54 47 Z" fill="none" stroke="#2FA84F" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/>
    </svg>'''
    write("assets/img/favicon.svg", fav)

if __name__ == "__main__":
    main()
