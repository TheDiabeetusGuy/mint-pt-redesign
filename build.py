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
# Bump this any time style.css or main.js changes. It's appended as a
# ?v= query string on both files so browsers/CDNs treat an updated file
# as a brand-new URL instead of serving a cached copy of the old one.
ASSET_VERSION = "18"

# ---------------------------------------------------------------
# Logo mark (recreated as scalable SVG from the client's existing
# two-peak "M" mountain logo, so it stays crisp at every size)
# ---------------------------------------------------------------
# NOTE: the client's real logo (assets/img/logo.png, background removed,
# assets/img/logo-icon.png icon-only crop) is used everywhere instead of a
# recreated mark, per instruction to keep the logo exactly as-is.

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
      <text x="4" y="208" fill="rgba(255,255,255,.55)" font-family="Nunito Sans, sans-serif" font-weight="700" font-size="11">DAY 1</text>
      <text x="352" y="14" fill="#fff" font-family="Nunito Sans, sans-serif" font-weight="700" font-size="11">GOAL</text>
    </svg>'''

# ---------------------------------------------------------------
# Content data
# ---------------------------------------------------------------
LOCATIONS = [
    dict(slug="ogden", name="Ogden Clinic", addr1="533 26th St. #202", city="Ogden, UT 84401",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com", hours="Mon&ndash;Fri: 7am&ndash;6pm<br>Sat&ndash;Sun: Closed"),
    dict(slug="clearfield", name="Clearfield Clinic", addr1="1030 University Park Blvd, Suite 1", city="Clearfield, UT 84015",
         phone="555-555-5555", fax="555-555-5555", email="daviscounty@mint-pt.com", hours="Mon&ndash;Fri: 7am&ndash;6pm<br>Sat&ndash;Sun: Closed"),
    dict(slug="brigham-city", name="Brigham City Clinic", addr1="60 S Main St", city="Brigham City, UT 84302",
         phone="555-555-5555", fax="555-555-5555", email=EMAIL_MAIN, hours="Mon&ndash;Fri: 7am&ndash;6pm<br>Sat&ndash;Sun: Closed"),
    dict(slug="murray", name="Murray Clinic", addr1="6095 S Fashion Blvd, STE 120", city="Murray, UT 84107",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com", hours="Mon&ndash;Fri: 7am&ndash;6pm<br>Sat&ndash;Sun: Closed"),
    dict(slug="riverton", name="Riverton Clinic", addr1="12427 4000 W #202", city="Riverton, UT 84096",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com", hours="Mon&ndash;Fri: 7am&ndash;6pm<br>Sat&ndash;Sun: Closed"),
    dict(slug="west-valley-city", name="West Valley City Clinic", addr1="3451 S 5600 W", city="West Valley City, UT 84120",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com", hours="Mon&ndash;Fri: 7am&ndash;6pm<br>Sat&ndash;Sun: Closed"),
    dict(slug="lehi", name="Lehi Clinic", addr1="120 W Main St", city="Lehi, UT 84043",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com", hours="Mon&ndash;Fri: 7am&ndash;6pm<br>Sat&ndash;Sun: Closed"),
    dict(slug="american-fork", name="American Fork Clinic", addr1="476 N 900 W, Suite B", city="American Fork, UT 84003",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com", hours="Mon&ndash;Fri: 7am&ndash;6pm<br>Sat&ndash;Sun: Closed"),
    dict(slug="provo", name="Provo Clinic", addr1="1807 N 1120 W", city="Provo, UT 84604",
         phone="555-555-5555", fax="555-555-5555", email="info@mint-pt.com", hours="Mon&ndash;Fri: 7am&ndash;6pm<br>Sat&ndash;Sun: Closed"),
]

SERVICES = [
    dict(slug="back-pain", title="Back Pain", icon="spine",
         card="Relief and long-term strength for acute strains, chronic tension, and everything in between.",
         intro="Back pain can start suddenly or build slowly, and it has a way of shrinking your world — cutting out favorite activities, hobbies, even a good night's sleep. At MINT, we look past the pain itself to find what's actually driving it, then build a plan that gets you moving again with confidence.",
         causes_label="Common Causes",
         causes=["Muscle strain or ligament sprain", "Herniated or bulging discs", "Poor posture and prolonged sitting",
                 "Degenerative changes or spinal stenosis", "Past injury, including auto accidents"],
         approach=["Manual therapy — joint mobilization and soft-tissue work to ease pain and restore movement",
                   "A personalized strengthening plan targeting your core and spine",
                   "Targeted stretching to release the tight muscles feeding the pain",
                   "Posture and body-mechanics coaching for how you sit, stand, and lift",
                   "Heat, cold, or other modalities to calm pain and inflammation early on",
                   "Dry needling for stubborn muscle knots and trigger points",
                   "Functional rehab to rebuild the strength your work and daily life demand",
                   "A gradual, guided return to the activities you miss"]),
    dict(slug="sciatica", title="Sciatica", icon="leg",
         card="Real relief from nerve pain that radiates through the hip, leg, or foot — treated at the source, not just the symptom.",
         intro="That sharp, shooting pain down your leg has a root cause — usually pressure or irritation somewhere along the sciatic nerve. We find where it starts and treat it there, so relief actually lasts.",
         causes_label="Common Causes",
         causes=["Herniated disc pressing on the nerve", "Spinal stenosis", "Piriformis muscle tightness",
                 "Pregnancy-related nerve pressure", "Prolonged sitting or poor movement patterns"],
         approach=["Targeted nerve-gliding and mobility exercises to reduce nerve irritation",
                   "Manual therapy to release the tight muscles compressing the nerve",
                   "Core and hip strengthening to take pressure off the lower spine",
                   "Dry needling for stubborn muscle tension along the nerve's path",
                   "Heat or cold therapy to calm acute flare-ups",
                   "Posture and movement coaching for sitting, standing, and daily habits",
                   "A gradual return to the activities flare-ups put on hold"]),
    dict(slug="chronic-pain", title="Chronic Pain", icon="pulse",
         card="A steady, whole-person plan for pain that's stuck around longer than it should.",
         intro="Pain that lingers for months or years changes how you move, sleep, and live. Our approach treats the whole picture — body and habits together — so you can build momentum instead of just managing symptoms.",
         causes_label="Common Contributors",
         causes=["Old injuries that never fully resolved", "Ongoing inflammation or joint changes", "Nervous system sensitization",
                 "Compensating movement patterns", "Stress, poor sleep, and inactivity feeding the cycle"],
         approach=["A graded activity plan that rebuilds tolerance without triggering flare-ups",
                   "Manual therapy, including myofascial release and joint mobilization, to ease tension",
                   "Advanced modalities — E-stim, KT-tape, the BEMER mat, and massage guns — to calm pain and speed healing",
                   "Functional rehab exercises that restore natural movement patterns",
                   "Education on pain science, so you understand what's actually happening",
                   "Personalized strength and conditioning matched to your current capacity",
                   "Ongoing check-ins so we can adjust the plan as you improve"]),
    dict(slug="knee-pain", title="Knee Pain", icon="knee",
         card="Stronger, steadier knees — whether you're dealing with an old injury, arthritis, or overuse.",
         intro="Knees carry a lot of weight, literally and figuratively. Whether it's a sports injury, post-surgical recovery, or pain that crept in over time, we build the strength and mechanics your knee needs to trust itself again.",
         causes_label="Common Causes",
         causes=["Ligament or meniscus injury", "Overuse or tendinitis", "Osteoarthritis",
                 "Muscle imbalances at the hip or ankle", "Post-surgical stiffness"],
         approach=["Targeted strengthening for the muscles that support the knee",
                   "Manual therapy to restore joint and soft-tissue mobility",
                   "Advanced modalities — ultrasound, electrical stimulation, and cold laser — to ease pain and speed tissue repair",
                   "Balance and mobility training to rebuild confidence in the joint",
                   "Gait and movement analysis to correct mechanics that stress the knee",
                   "Sport- and activity-specific return-to-motion training",
                   "Bracing, taping, or lifestyle guidance to support long-term joint health"]),
    dict(slug="shoulder-pain", title="Shoulder Pain", icon="shoulder",
         card="Restoring reach, strength, and sleep-through-the-night comfort to a cranky shoulder.",
         intro="Shoulder pain has a way of showing up in everything — reaching for a cabinet, sleeping on your side, throwing a ball. We rebuild strength and mobility through the whole shoulder complex, not just the sore spot.",
         causes_label="Common Causes",
         causes=["Rotator cuff strain or tear", "Impingement or bursitis", "Frozen shoulder",
                 "Instability or a past dislocation", "Postural strain from desk work"],
         approach=["Manual therapy to restore joint and soft-tissue mobility",
                   "A progressive strengthening program for the rotator cuff and scapula",
                   "Range-of-motion exercises to reverse stiffness and rebuild flexibility",
                   "Postural correction for lasting relief, especially after desk work",
                   "Dry needling for trigger points that refer pain into the shoulder",
                   "A guided, gradual return to lifting, throwing, or reaching overhead"]),
    dict(slug="headaches-migraines", title="Headaches & Migraines", icon="head",
         card="Getting to the root of tension headaches and migraines — often hiding in the neck.",
         intro="Many headaches and migraines are connected to tension and restriction in the neck and upper back. We assess that connection and treat it directly, often bringing relief other approaches miss.",
         causes_label="Common Triggers",
         causes=["Neck and upper-back muscle tension", "Poor posture, especially from screen time", "TMJ dysfunction",
                 "Stress and muscle guarding", "Cervicogenic (neck-related) triggers"],
         approach=["Manual therapy for the neck, jaw, and upper back",
                   "Dry needling for trigger-point release",
                   "Postural retraining for desk, driving, and screen-time habits",
                   "TMJ-specific treatment when jaw tension is contributing",
                   "Gentle mobility and strengthening exercises for the neck and upper back",
                   "Guidance on identifying and managing your personal triggers between visits"]),
    dict(slug="concussion-tbi", title="Concussion / Mild TBI", icon="brain",
         card="A careful, step-by-step return to clear thinking, balance, and daily life.",
         intro="Recovering from a concussion or mild traumatic brain injury isn't one-size-fits-all. We assess balance, vision, and neck function together, then guide a safe, steady return to school, work, and sport.",
         causes_label="Common Symptoms We Treat",
         causes=["Neck pain and headaches following the injury", "Balance, coordination, and vestibular issues (dizziness, vertigo)",
                 "Vision changes or difficulty with eye tracking", "Exercise or activity intolerance",
                 "Orthostatic intolerance and dysautonomia, including POTS", "Persistent fatigue"],
         approach=["Vestibular and visual training for balance, dizziness, and eye-tracking issues",
                   "Manual therapy — massage, joint mobilization, and stretching — for neck-related symptoms",
                   "Dry needling for muscle tension contributing to headaches",
                   "Strengthening, balance, and coordination training",
                   "Cardiovascular exercise introduced at a pace your symptoms can tolerate",
                   "Autonomic reconditioning for dysautonomia and orthostatic intolerance",
                   "Hot/cold and compression therapy for symptom relief",
                   "Graded exertion protocols with close coordination with your physician or care team"]),
    dict(slug="long-covid", title="Long COVID / Post-COVID Syndrome", icon="lungs",
         card="Rebuilding stamina and function after long COVID or a tough post-viral recovery.",
         intro="Long COVID and post-viral syndromes can leave you fatigued, short of breath, or simply not yourself. We build a pacing and conditioning plan that respects your limits while steadily expanding them — with providers specifically trained in Long COVID, POTS, ME/CFS, and dysautonomia.",
         causes_label="Common Symptoms We Address",
         causes=["Post-exertional malaise (PEM) and post-viral fatigue", "Orthostatic intolerance and dysautonomia, including POTS",
                 "Breathing pattern changes and reduced cardiovascular tolerance", "Muscle weakness from extended rest or illness",
                 "Brain fog, headache, and generalized pain", "Mast Cell Activation Syndrome (MCAS) symptoms"],
         approach=["Careful, symptom-guided pacing that avoids triggering PEM",
                   "For ME/CFS, a collaborative approach that does not default to prescribed exercise",
                   "Breathing retraining exercises",
                   "Autonomic and orthostatic tolerance training for POTS and dysautonomia",
                   "Gradual, individualized reconditioning when it's appropriate for your condition",
                   "Energy conservation strategies for daily life",
                   "Ongoing monitoring so we adjust before you crash",
                   "Both in-person and virtual visit options"]),
    dict(slug="dry-needling", title="Dry Needling", icon="needle",
         card="A thin-needle technique that releases tight, irritable muscle knots fast.",
         intro="Dry needling targets the small, contracted knots in muscle tissue — often called trigger points — that cause pain, stiffness, and referred discomfort elsewhere in the body. It's a precise, effective tool we use alongside hands-on and exercise-based care.",
         causes_label="Commonly Used For",
         causes=["Muscle tightness and trigger points", "Chronic tension patterns", "Sports-related muscle strain",
                 "Headaches originating in the neck and shoulders", "Slow-healing overuse injuries"],
         approach=["A focused evaluation to find the muscles actually driving your pain",
                   "Thin filament needles placed directly into trigger points for fast relief",
                   "Improved muscle function and range of motion as tight bands release",
                   "Increased local blood flow that speeds the body's natural healing",
                   "Reduced inflammation in the treated muscle",
                   "Often paired with stretching or strengthening the same visit",
                   "A clear plan for how many sessions typically help"]),
    dict(slug="winback-diathermy", title="WinBack TECAR Therapy", icon="waves",
         card="Deep, therapeutic heat that speeds tissue healing and eases stiffness — applied while we treat you.",
         intro="WinBack TECAR therapy delivers gentle radiofrequency energy deep into muscle and connective tissue — well beyond what a heating pad can reach — to boost circulation, ease pain, and speed recovery. Most patients describe it as comfortable and relaxing, with a mild warming sensation.",
         causes_label="Well Suited For",
         causes=["Muscle strains and sports injuries", "Tendon and ligament injuries, including sprains",
                 "Back, neck, shoulder, hip, and knee pain", "Joint stiffness and limited mobility",
                 "Chronic muscle and joint pain", "Recovery following certain surgeries or injuries"],
         approach=["Gentle radiofrequency energy that creates therapeutic heat deep in the tissue",
                   "Used live, during manual therapy, stretching, or mobility work — not a stand-alone sit-and-wait treatment",
                   "Increased local circulation to speed the body's natural healing",
                   "A comfortable, non-invasive treatment — no needles, no downtime",
                   "Intensity customized to your tissue and tolerance",
                   "One more tool in a broader plan, not a quick fix on its own"]),
    dict(slug="auto-accidents", title="Auto Accident Recovery", icon="car",
         card="Full-picture recovery after a collision, from whiplash to lasting nerve pain.",
         intro="Car accidents can leave injuries that aren't obvious right away — whiplash, joint strain, nerve irritation — that show up hours or days later. We evaluate thoroughly, document your recovery, and work directly with your claim so you can focus on healing.",
         causes_label="What We Treat",
         causes=["Whiplash-associated neck injuries", "Back and joint strain from impact", "Headaches and concussion-like symptoms",
                 "Nerve compression or irritation", "Soft-tissue injury that worsens without early treatment"],
         approach=["A thorough initial evaluation, even if pain seems mild at first",
                   "Pain management using manual therapy, heat/cold, and therapeutic exercise",
                   "Personalized exercises to restore flexibility, strength, and range of motion",
                   "Balance and coordination training when the accident has affected either",
                   "Cognitive rehab support for concussion or traumatic brain injury, coordinated with your other providers",
                   "Detailed documentation to support your claim",
                   "Coordination with attorneys, case managers, or insurers",
                   "A steady, educated path back to full, pain-free function — with guidance on preventing re-injury"]),
    dict(slug="workers-comp", title="Workers' Comp", icon="briefcase",
         card="Getting you back to work safely, with care coordinated around your claim.",
         intro="A workplace injury shouldn't leave your recovery — or your paycheck — in question. We evaluate the injury, build a treatment plan around the physical demands of your specific job, and coordinate directly with your employer, case manager, and insurance carrier at every step.",
         causes_label="What We Treat",
         causes=["Overuse and repetitive strain injuries", "Lifting and back injuries", "Slip, trip, and fall injuries",
                 "Post-surgical work injuries", "Re-aggravated prior injuries"],
         approach=["Direct communication with your case manager and employer", "Work conditioning that simulates your actual job tasks",
                   "Ergonomic recommendations to help prevent re-injury", "Clear documentation to support your claim",
                   "A safe, graded return-to-work plan aimed at full duty"]),
]

EXTRA_SPECIALTIES = ["Active Release Therapy (ASTYM)", "Manual Therapy & Massage", "Occupational Therapy Services",
                      "Orthopedic Certified Specialists", "Return-to-Sport Conditioning", "Sports Medicine",
                      "TMJ/TMD Therapy", "Work Conditioning"]

PROVIDERS = [
    dict(name="Brad Klemetson", cred="PT, DPT", role="Founder & Clinical Director",
         short_bio="The steady hand behind MINT — patients call him relentless in the best way, staying on a problem until it's actually solved.",
         bio="Brad earned his Doctorate of Physical Therapy from UNLV in 2017 and has published research on balance and Parkinson's disease. He treats neck pain, dizziness, headaches, and migraines, using dry needling and manual therapy to speed recovery, and is certified in FCE, FJA, POET, and FFD testing. He also takes time to walk patients through their MRI findings and treatment options. Special interests: headaches, migraines, radiculopathies, auto accident and workplace injury care, and injury prevention."),
    dict(name="Ryan Rindlesbacher", cred="PT, DPT", role="Physical Therapist",
         short_bio="Brings a calm, methodical approach to complex cases, breaking recovery into steps that make sense.",
         bio="Ryan grew up in northern Utah and earned his degree in Human Movement Science from Utah State University before completing his Doctorate of Physical Therapy at Touro University Nevada. He's trained in dry needling, FCE, FJA, POET, and FFD testing, and focuses on reducing workplace injury risk and helping injured workers return to the job. Ryan is fluent in Spanish and enjoys serving Utah's Hispanic community."),
    dict(name="Joseph Zeigler", cred="PT, DPT", role="Physical Therapist · Ogden",
         short_bio="Focused on function first — getting patients back to the specific movements their life and work demand.",
         bio="Joseph grew up in Mesa, AZ playing soccer, swimming, cross country, and ultimate frisbee — recovering from his own sports injuries is what drew him to physical therapy. He earned a B.S. in Athletic Training from BYU and his Doctorate of Physical Therapy from Northern Arizona University. He's worked with collegiate and high school athletic teams, skilled nursing facilities, general orthopedics, and home health, with additional training in dry needling, myofascial release, joint manipulation, KT taping, and cupping. Special interests: shoulder and rotator cuff injuries, neck pain, headaches, knee pain, and low back pain."),
    dict(name="Christian Bentley", cred="PT, DPT", role="Physical Therapist",
         short_bio="Blends manual therapy with hands-on coaching, with an eye for the small details that speed recovery.",
         bio="Christian earned his B.S. in Kinesiology, exercise science emphasis, from the University of Utah, and his Doctorate of Physical Therapy from Rocky Mountain University of Health Professions in 2024. He's trained in dry needling, spinal manipulation, and manual therapy, pairing that with exercise science to help patients reach their goals. Outside the clinic, he's usually with his wife and two kids, playing sports, or debating Lord of the Rings lore."),
    dict(name="Grace Waters", cred="PT, DPT", role="Physical Therapist",
         short_bio="Brings warmth and patience to every session, with a gift for making a hard recovery feel manageable.",
         bio="Grace has been a physical therapist since 2019, specializing in pelvic health while treating all conditions with a whole-body, person-specific approach. She builds creative, activity-specific exercises to rebuild strength and confidence in the movements patients find hardest. Outside the clinic, she's an avid reader and traveler — she's lived in 16 states — and enjoys yoga, biking, and mountain time."),
    dict(name="Adam Gilbert", cred="PT, DPT", role="Physical Therapist · Ogden",
         short_bio="Direct and encouraging, with a strength-and-conditioning background that shows in his treatment plans.",
         bio="Direct and encouraging, with a strength-and-conditioning background that shows in his treatment plans."),
    dict(name="Kate Light", cred="PT, DPT", role="Physical Therapist",
         short_bio="Approaches every patient as an individual, tailoring pace and technique to what actually works for them.",
         bio="Kate studied Exercise Science at Ohio State and the University of Alabama as a Division I student-athlete, then earned her Doctorate of Physical Therapy from George Washington University with advanced pediatric certification from Georgetown. A former NFL cheerleader and current Utah Jazz dancer, she draws on that background to help patients perform at their best. Special interests: dance-related injuries, hypermobility, injury prevention, reflex integration, and pediatric neurodevelopmental care."),
    dict(name="Casey Snell", cred="PT, DPT", role="Physical Therapist",
         short_bio="Combines a sharp clinical eye with genuine encouragement — patients leave sessions knowing their why.",
         bio="Combines a sharp clinical eye with genuine encouragement — patients leave sessions knowing their why."),
    dict(name="Andrew Mitchell", cred="PT, DPT", role="Physical Therapist",
         bio="Detail-oriented and thorough, with a knack for catching what other evaluations miss."),
    dict(name="Josh", cred="PT, DPT", role="Physical Therapist · Ogden",
         bio="Josh earned his Kinesiology degree from the University of Utah and his Doctor of Physical Therapy from Duke University. He's treated a wide range of orthopedic and neurological conditions and post-surgical patients across outpatient, home health, and hospital settings, and takes a practical, patient-centered approach tailored to each person's goals. Outside the clinic, he's a husband and father of three who enjoys fishing, playing drums, and getting outdoors."),
    dict(name="Sandy Larson", cred="PTA", role="Physical Therapist Assistant",
         bio="Sandy has worked in healthcare for over 10 years and graduated from Salt Lake Community College's PTA program in 2022. She's passionate about getting to know her patients and helping them reach their health goals. Outside of work, she's a mother of three who enjoys softball, running, and yoga with her family."),
    dict(name="Maryn Christensen", cred="PTA", role="Physical Therapist Assistant",
         bio="Maryn grew up in Boise, ID and earned her Kinesiology degree at Utah State before completing her PTA degree in 2022. She's passionate about improving patients' wellbeing and advocating for their health every step of the way. Outside of work, she's a mom to one little boy and loves spending time outdoors with him."),
    dict(name="Tawny Cruz", cred="PTA", role="Physical Therapist Assistant",
         bio="Tawny earned an Associate Degree in Exercise Science before completing the PTA program at Provo College in 2023. She's worked across inpatient rehab, outpatient therapy, and home health, and finds it rewarding to make a difference for patients and their families. Outside of work, she's a health and fitness enthusiast, married 12 years with three kids, who enjoys the outdoors as much as a good movie night in."),
    dict(name="Natoshia Diffendaffer", cred="PTA", role="Physical Therapist Assistant",
         bio="Detail-focused and supportive, helping translate the treatment plan into real daily progress."),
    dict(name="Amber Hankes", cred="PTA", role="Physical Therapist Assistant",
         bio="Patient and thorough, with a talent for putting nervous first-time patients at ease."),
    dict(name="Gabby Willardsen", cred="PTA", role="Physical Therapist Assistant",
         bio="Brings consistency and care to every session, cheering on every bit of progress along the way."),
    dict(name="Jason Gubler", cred="PT, DPT", role="Physical Therapist · Brigham City",
         bio="Combines technical precision with genuine care, making sure every plan fits the person in front of him."),
    dict(name="Skyler Little", cred="PT, DPT", role="Physical Therapist · Riverton",
         bio="Approaches every recovery with patience and a clear plan, so patients know exactly what to expect next."),
]

# Which providers see patients at which clinic, drawn from the per-location
# staff photos in the original site. Names must match PROVIDERS entries above.
CLINIC_PROVIDERS = {
    "ogden": ["Joseph Zeigler", "Adam Gilbert", "Josh"],
    "clearfield": ["Joseph Zeigler", "Adam Gilbert", "Josh"],
    "brigham-city": ["Jason Gubler"],
    "murray": ["Brad Klemetson", "Christian Bentley", "Grace Waters"],
    "riverton": ["Skyler Little", "Sandy Larson", "Amber Hankes"],
    "west-valley-city": ["Ryan Rindlesbacher", "Brad Klemetson"],
    "lehi": ["Casey Snell", "Natoshia Diffendaffer"],
    "american-fork": ["Casey Snell", "Natoshia Diffendaffer"],
    "provo": ["Andrew Mitchell", "Natoshia Diffendaffer"],
}

def providers_for_clinic(slug):
    names = CLINIC_PROVIDERS.get(slug, [])
    by_name = {p["name"]: p for p in PROVIDERS}
    return [by_name[n] for n in names if n in by_name]

# Append each provider's primary clinic city to their role (e.g. "Physical
# Therapist · Ogden"), based on CLINIC_PROVIDERS. Providers who work at more
# than one clinic get the first one listed below (in LOCATIONS order); a
# provider with no CLINIC_PROVIDERS entry is left without a city.
CITY_LABELS = {l["slug"]: l["name"].replace(" Clinic", "") for l in LOCATIONS}
for p in PROVIDERS:
    if " · " in p["role"]:
        continue
    for l in LOCATIONS:
        if p["name"] in CLINIC_PROVIDERS.get(l["slug"], []):
            p["role"] = f"{p['role']} · {CITY_LABELS[l['slug']]}"
            break

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

def maps_embed_src(loc):
    # Falls back to just the city when the street address isn't on file yet
    # (e.g. Brigham City), so the map still resolves to a sensible pin.
    if "call for" in loc.get("addr1", "").lower():
        q = f"{loc['name']} {loc['city']}"
    else:
        q = f"{loc['name']} {loc['addr1']} {loc['city']}"
    q = q.replace(" ", "+")
    return f"https://www.google.com/maps?q={q}&output=embed"

def city_label(loc):
    return loc["name"].replace(" Clinic", "")

# ---------------------------------------------------------------
# Header / Footer / Base layout
# ---------------------------------------------------------------
def nav_html(depth="", active=""):
    def a(href, label, key):
        cls = ' class="active"' if active == key else ""
        return f'<a href="{depth}{href}"{cls}>{label}</a>'

    loc_links = "".join(f'<a href="{depth}locations.html#{l["slug"]}">{l["name"]}</a>' for l in LOCATIONS)
    svc_links = "".join(
        f'<a href="{depth}services/{s["slug"]}.html"{" class=\"svc-more\"" if i >= 5 else ""}>{s["title"]}</a>'
        for i, s in enumerate(SERVICES)
    )
    svc_links += f'<a href="{depth}services.html" class="dropdown-viewall">Explore All Services</a>'

    return f'''<header class="site-header">
    <div class="container nav">
      <a href="{depth}index.html" class="brand">
        <img src="{depth}assets/img/logo.png" alt="MINT Physical Therapy" class="brand-logo">
      </a>

      <nav aria-label="Primary" class="main-nav">
        <ul class="nav-links" id="navLinks">
          <li>{a("index.html", "Home", "home")}</li>
          <li class="has-dropdown">
            <button type="button" aria-haspopup="true">Locations {icon("chev-down", cls="icon chev")}</button>
            <div class="dropdown">{loc_links}</div>
          </li>
          <li>{a("providers.html", "Our Providers", "providers")}</li>
          <li class="has-dropdown split{' is-active' if active == 'services' else ''}">
            {a("services.html", "Services", "services")}
            <button type="button" class="dropdown-toggle" aria-haspopup="true" aria-expanded="false" aria-label="Show services menu">{icon("chev-down", cls="icon chev")}</button>
            <div class="dropdown wide">{svc_links}</div>
          </li>
          <li>{a("join-team.html", "Join Our Team", "join")}</li>
          <li>{a("contact.html", "Contact", "contact")}</li>
        </ul>
      </nav>

      <div class="nav-cta">
        <a class="btn btn-primary btn-sm" href="{depth}contact.html"><span class="btn-label-full">Request Appointment</span><span class="btn-label-short">Appointment</span></a>
        <button class="menu-toggle" aria-label="Open menu" aria-expanded="false">{icon("menu")}</button>
      </div>
    </div>
  </header>'''

def footer_html(depth=""):
    return f'''<footer class="site-footer">
    <div class="container footer-top">
      <div class="footer-row">
        <div class="footer-brand-block">
          <a class="footer-brand" href="#" id="footerBrandTop" aria-label="Back to top"><img src="{depth}assets/img/logo.png" alt="MINT Physical Therapy" class="footer-logo"></a>
          <p class="footer-tagline">Utah-based, one-on-one physical therapy — in one of our clinics, or at your door. Mobile visits available from Ogden to Payson.</p>
        </div>
        <nav class="footer-labels" aria-label="Footer">
          <a href="{depth}locations.html">Clinics</a>
          <a href="{depth}services.html">Services</a>
          <a href="{depth}contact.html">Get in Touch</a>
        </nav>
      </div>
      <div class="footer-social-row">
        <div class="footer-social">
          <a href="{SOCIAL['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">{icon("facebook")}</a>
          <a href="{SOCIAL['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{icon("instagram")}</a>
          <a href="{SOCIAL['youtube']}" target="_blank" rel="noopener" aria-label="YouTube">{icon("youtube")}</a>
          <a href="{SOCIAL['spotify']}" target="_blank" rel="noopener" aria-label="Spotify">{icon("spotify")}</a>
        </div>
      </div>
    </div>
    <div class="container footer-bottom">
      <span>&copy; 2026 MINT Physical Therapy. All rights reserved.</span>
      <nav class="footer-legal" aria-label="Legal">
        <a href="{depth}privacy-policy.html">Privacy Policy</a>
        <a href="{depth}terms-and-conditions.html">Terms &amp; Conditions</a>
      </nav>
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
<link rel="icon" href="{depth}assets/img/favicon.png?v=2" type="image/png">
<link rel="stylesheet" href="{depth}assets/css/style.css?v={ASSET_VERSION}">
{extra_head}
</head>
<body>
<a href="#main" class="skip-link">Skip to content</a>
{nav_html(depth, active)}
<main id="main">
{body}
</main>
{footer_html(depth)}
<script src="{depth}assets/js/main.js?v={ASSET_VERSION}"></script>
</body>
</html>'''

def page_hero(eyebrow, title, lead, crumbs=None, depth="", extra_class=""):
    cls = f"page-hero {extra_class}".strip()
    return f'''<section class="{cls}">
    {topo_lines(seed=3, rows=5)}
    <div class="container">
      <div class="eyebrow on-dark">{eyebrow}</div>
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

def short_bio(text, limit=100):
    # A short, consistent-length teaser for cards that show the bio
    # permanently (Home page) rather than the full paragraph used on the
    # Providers page — keeps every card roughly the same height regardless
    # of how long that provider's full bio happens to be.
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;: ")
    return cut + "…"

def provider_card(p, mode="static"):
    # mode "static":     no bio, no interaction (Locations page team sections)
    # mode "hover":      short bio teaser always visible (Home page)
    # mode "photo-only": just the color/initials square, no overlay at all —
    #                    used wherever the name/role/bio already appears
    #                    right next to the photo (Providers page detail card
    #                    and mobile carousel), so it isn't shown twice.
    idx = sum(ord(c) for c in p['name']) % len(AVATAR_COLORS)
    color = AVATAR_COLORS[idx]
    if mode == "photo-only":
        return f'''<div class="provider-card" style="background:{color};">
      <span class="provider-initials">{initials(p['name'])}</span>
    </div>'''
    bio_html = ""
    card_cls = "provider-card"
    if mode == "hover":
        card_cls = "provider-card has-bio"
        bio_html = f'<p class="provider-overlay-bio">{p.get("short_bio", short_bio(p["bio"]))}</p>'
    return f'''<div class="{card_cls}" style="background:{color};">
      <span class="provider-initials">{initials(p['name'])}</span>
      <div class="provider-overlay">
        <h3>{p['name']}, {p['cred']}</h3>
        <div class="role">{p['role']}</div>
        {bio_html}
      </div>
    </div>'''

def prov_slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

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

def hz_carousel(cards_html, extra_class=""):
    # Generic mobile-only swipe carousel: one card per slide, auto-advances
    # with a real sliding motion (not a fade) — used to replace a grid of
    # cards on narrow screens. Desktop keeps the original grid.
    slides = "".join(f'<div class="hz-carousel-slide">{c}</div>' for c in cards_html)
    bars = "".join(f'<span class="hz-carousel-bar{" is-active" if i == 0 else ""}"></span>' for i in range(len(cards_html)))
    return f'''<div class="hz-carousel {extra_class}">
      <div class="hz-carousel-viewport">
        <div class="hz-carousel-track">{slides}</div>
        <button type="button" class="hz-carousel-arrow hz-carousel-prev" aria-label="Previous">{icon('chevron-left')}</button>
        <button type="button" class="hz-carousel-arrow hz-carousel-next" aria-label="Next">{icon('chevron-right')}</button>
      </div>
      <div class="hz-carousel-progress">{bars}</div>
    </div>'''

def cta_band(heading, sub, depth="", plain=False):
    cls = "cta-band cta-band-plain" if plain else "cta-band"
    phone_cls = "btn btn-outline" if plain else "btn btn-outline on-dark"
    return f'''<div class="{cls}">
      <div>
        <h2>{heading}</h2>
        <p>{sub}</p>
      </div>
      <div class="actions">
        <a class="btn btn-gold" href="{depth}contact.html">Request Appointment</a>
        <a class="{phone_cls}" href="tel:+1{PHONE_MAIN_TEL}">{icon('phone')} {PHONE_MAIN}</a>
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
        dict(n="01", title="Reduces pain naturally", text="Hands-on care and targeted movement calm inflammation and pain without relying on medication.", img="journey-1.jpg", alt="A physical therapist gently guiding a patient through a shoulder stretch"),
        dict(n="02", title="Speeds up recovery", text="A plan built around your specific injury gets you back to normal faster than resting and hoping.", img="journey-2.jpg", alt="A physical therapist coaching a patient through a resistance-band lunge"),
        dict(n="03", title="Prevents future injuries", text="Strengthening the muscles and joints around an injury keeps it from happening again.", img="journey-3.jpg", alt="A physical therapist guiding a patient's knee alignment during a kettlebell lunge"),
    ]
    body = f'''
  <section class="home-hero">
    <div class="home-carousel" id="homeCarousel">
      <div class="hc-slide is-active" style="background:linear-gradient(135deg, var(--forest-800), var(--forest-600));">
        {topo_lines(seed=1, rows=5, stroke="rgba(255,255,255,.12)")}
        <div class="hc-content">{icon('squat', cls='icon hc-icon')}<div class="hc-label">Move</div></div>
        <span class="hc-caption">Photo/video coming soon</span>
      </div>
      <div class="hc-slide" style="background:linear-gradient(135deg, var(--forest-700), var(--forest-500));">
        {topo_lines(seed=2, rows=5, stroke="rgba(255,255,255,.12)")}
        <div class="hc-content">{icon('run', cls='icon hc-icon')}<div class="hc-label">Improve</div></div>
        <span class="hc-caption">Photo/video coming soon</span>
      </div>
      <div class="hc-slide" style="background:linear-gradient(135deg, var(--forest-900), var(--forest-700));">
        {topo_lines(seed=3, rows=5, stroke="rgba(255,255,255,.12)")}
        <div class="hc-content">{icon('heart', cls='icon hc-icon')}<div class="hc-label">Nurture</div></div>
        <span class="hc-caption">Photo/video coming soon</span>
      </div>
      <div class="hc-slide" style="background:linear-gradient(135deg, var(--forest-800), var(--forest-500));">
        {topo_lines(seed=4, rows=5, stroke="rgba(255,255,255,.12)")}
        <div class="hc-content">{icon('users', cls='icon hc-icon')}<div class="hc-label">Teach</div></div>
        <span class="hc-caption">Photo/video coming soon</span>
      </div>
    </div>
  </section>

  <section class="home-intro">
    <div class="container home-intro-grid">
      <p class="home-intro-text">Helping you move better, feel better, and get back to what you love through one-on-one care &mdash; mobile or in-clinic across Utah. Cash-pay, workers&rsquo; comp, and auto-accident patients welcome. Let&rsquo;s get you back to MINT condition.</p>
    </div>
    <div class="container home-ig-video">{video_frame("Instagram video coming soon")}</div>
    <div class="container"><div class="intro-divider"></div></div>
  </section>

  <section class="section" style="padding-top:clamp(20px,3.5vw,48px);">
    <div class="container">
      <div class="section-head center">
        <div class="eyebrow" style="justify-content:center;">Why Physical Therapy</div>
        <h2>Three reasons people choose to move first, not last.</h2>
      </div>
      <div class="journey">
        {''.join(f"""<div class="journey-step"><div class="n">{s['n']}</div><h3>{s['title']}</h3><p>{s['text']}</p><div class="journey-photo"><img src="assets/img/{s['img']}" alt="{s['alt']}" loading="lazy"></div></div>""" for s in steps)}
      </div>
    </div>
  </section>

  <section class="section bg-stone" style="padding:clamp(28px,4.5vw,60px) 0;">
    <div class="container">
      <div class="section-head">
        <div class="eyebrow">What We Treat</div>
        <h2>Specialized care for the injuries that slow you down.</h2>
        <p>From everyday aches to complex, claim-based recovery &mdash; here&rsquo;s where we spend most of our time.</p>
      </div>
      <div class="grid-4 grid-mobile-hide">
        {''.join(service_card(s) for s in top_services)}
      </div>
      {hz_carousel([service_card(s) for s in top_services])}
      <div style="margin-top:34px;text-align:center;">
        <a class="btn btn-outline" href="services.html">View All Services &amp; Specialties {icon('arrow-right')}</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding:clamp(28px,4.5vw,60px) 0;">
    <div class="container split">
      <div class="panel-art dark">
        <img src="assets/img/mobile-pt.jpg" alt="A physical therapist guiding a patient through a shoulder stretch in her living room" style="width:100%;height:100%;object-fit:cover;display:block;">
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

  <section class="section bg-mint team-section" style="padding:clamp(28px,4.5vw,60px) 0;">
    <div class="container">
      <div class="section-head center">
        <div class="eyebrow" style="justify-content:center;">Our Team</div>
        <p style="font-size:clamp(26px,3.6vw,40px); line-height:1.1; margin-top:14px;">All trained in the same hands-on, whole-person approach.</p>
      </div>
      <div class="grid-4 grid-mobile-hide">
        {''.join(provider_card(p, mode="hover") for p in PROVIDERS[:8])}
      </div>
      {hz_carousel([provider_card(p, mode="hover") for p in PROVIDERS[:8]], extra_class="hz-carousel-on-photo")}
      <div style="margin-top:34px;text-align:center;">
        <a class="btn btn-outline" href="providers.html">Meet the Full Team {icon('arrow-right')}</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding:clamp(28px,4.5vw,60px) 0;">
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

  <section class="section bg-stone" style="padding:clamp(28px,4.5vw,60px) 0;">
    <div class="container">
      <div class="section-head center">
        <div class="eyebrow" style="justify-content:center;">Patient Stories</div>
        <h2>Real progress, in their own words.</h2>
      </div>
      <div class="tc-carousel grid-mobile-hide" id="testimonialCarousel">
        {''.join(f'<div class="tc-page{" is-active" if i == 0 else ""}"><div class="grid-4">{"".join(testimonial_card(t) for t in page)}</div></div>' for i, page in enumerate([TESTIMONIALS[j:j+4] for j in range(0, len(TESTIMONIALS), 4)]))}
      </div>
      {hz_carousel([testimonial_card(t) for t in TESTIMONIALS])}
    </div>
  </section>

  <section class="section" style="padding:clamp(28px,4.5vw,60px) 0;">
    <div class="container">
      {cta_band("Ready to start feeling like yourself again?", "Tell us what&rsquo;s going on and we&rsquo;ll help you find the right provider, clinic, or mobile visit.", plain=True)}
    </div>
  </section>
'''
    return base_page("Home", "Utah-based mobile and in-clinic physical therapy. One-on-one care across nine Wasatch Front clinics, or right at your door.", body, depth="", active="home")


def locations_page():
    hero = f'''<section class="page-hero loc-hero">
    {topo_lines(seed=3, rows=5)}
    <div class="container">
      <h1>Find a MINT Clinic Near You</h1>
      <p class="lead">Walk-in for 1:1 care at any of our nine Wasatch Front locations, or ask about a mobile visit &mdash; we cover Ogden all the way down to Payson.</p>
    </div>
  </section>'''

    list_items = "".join(
        f'<li class="loc-list-item{" is-active" if i == 0 else ""}" data-target="loc-{l["slug"]}">{city_label(l)}</li>'
        for i, l in enumerate(LOCATIONS)
    )
    list_items += '<li class="loc-list-item loc-list-item-mobile" data-target="loc-mobile">Mobile Visit</li>'

    select_options = "".join(
        f'<option value="{l["slug"]}"{" selected" if i == 0 else ""}>{city_label(l)}</option>'
        for i, l in enumerate(LOCATIONS)
    )
    select_options += '<option value="mobile">Mobile Visit</option>'
    mobile_select = f'''<select class="loc-mobile-select" id="locMobileSelect" aria-label="Choose a clinic">{select_options}</select>'''

    def detail_panel(l, i):
        provs = providers_for_clinic(l["slug"])
        provider_cards = "".join(provider_card(p) for p in provs)
        providers_block = f'''<div class="loc-providers-wrap">
        <div class="loc-providers-heading">Meet the {city_label(l)} Team</div>
        <div class="loc-providers-grid grid-mobile-hide-860">{provider_cards}</div>
        <div class="loc-providers-carousel-wrap">{hz_carousel([provider_card(p) for p in provs], extra_class="hz-carousel-on-photo")}</div>
      </div>''' if provs else ""
        return f'''<div class="loc-detail{" is-active is-visible" if i == 0 else ""}" id="loc-{l['slug']}">
      <div class="loc-detail-card">
        <div class="loc-detail-info">
          <h3>{icon('pin', cls='icon', extra='style="width:17px;height:17px;color:var(--forest-600);flex:none"')}{l['name']}</h3>
          <p class="loc-detail-addr">{l['addr1']}, {l['city']}</p>
          <div class="loc-detail-meta">
            <div><span>Phone</span>{l['phone']}</div>
            <div><span>Fax</span>{l['fax']}</div>
            <div><span>Email</span>{l['email']}</div>
            <div><span>Hours</span>{l['hours']}</div>
          </div>
          <a class="btn btn-primary" href="contact.html">Request an Appointment</a>
        </div>
        <div class="loc-detail-map">
          <iframe data-src="{maps_embed_src(l)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map to {l['name']}"></iframe>
          <a class="loc-map-chip" href="{maps_href(l)}" target="_blank" rel="noopener">{icon('navigate', cls='icon', extra='style="width:13px;height:13px"')} Get Directions</a>
        </div>
      </div>
      {providers_block}
    </div>'''

    panels = "".join(detail_panel(l, i) for i, l in enumerate(LOCATIONS))
    panels += '''<div class="loc-detail loc-mobile-panel" id="loc-mobile">
      <div class="eyebrow">Can&rsquo;t make it in?</div>
      <h2>We&rsquo;ll come to you instead.</h2>
      <p>Mobile physical therapy means the same 1:1 care, delivered at your home or office &mdash; available from Ogden to Payson.</p>
      <a class="btn btn-primary" href="contact.html">Request a Mobile Visit</a>
    </div>'''

    body = f'''{hero}
  <section class="section loc-list-section">
    <div class="container loc-container">
      <div class="loc-split">
        <div>
          <ul class="loc-list">{list_items}</ul>
          {mobile_select}
        </div>
        <div class="loc-detail-wrap">{panels}</div>
      </div>
    </div>
  </section>
'''
    return base_page("Locations", "Nine MINT Physical Therapy clinics across Utah's Wasatch Front, plus mobile visits from Ogden to Payson.", body, active="locations")


def providers_page():
    dpts = [p for p in PROVIDERS if p['cred'] == 'PT, DPT']
    ptas = [p for p in PROVIDERS if p['cred'] == 'PTA']

    def list_and_detail(providers, default_name):
        default_slug = prov_slug(default_name)
        list_items = "".join(
            f'''<li class="prov-list-item{" is-active" if prov_slug(p['name']) == default_slug else ""}"
          data-target="prov-{prov_slug(p['name'])}" tabindex="0" role="button">
        <span class="prov-list-name">{p['name']}, {p['cred']}</span>
        <span class="prov-list-role">{p['role']}</span>
      </li>'''
            for p in providers
        )
        panels = "".join(
            f'''<div class="prov-detail{" is-active is-visible" if prov_slug(p['name']) == default_slug else ""}" id="prov-{prov_slug(p['name'])}">
        <div class="prov-detail-card">
          <div class="prov-detail-visual">{provider_card(p, mode="photo-only")}</div>
          <div class="prov-detail-info">
            <h3>{p['name']}, {p['cred']}</h3>
            <div class="prov-detail-role">{p['role']}</div>
            <p class="prov-detail-bio">{p['bio']}</p>
          </div>
        </div>
      </div>'''
            for p in providers
        )
        slides = "".join(
            f'''<div class="prov-carousel-slide{" is-active is-visible" if prov_slug(p['name']) == default_slug else ""}">
          <div class="prov-detail-card">
            <div class="prov-detail-visual">{provider_card(p, mode="photo-only")}</div>
            <div class="prov-detail-info">
              <h3>{p['name']}, {p['cred']}</h3>
              <div class="prov-detail-role">{p['role']}</div>
              <p class="prov-detail-bio">{p['bio']}</p>
            </div>
          </div>
        </div>'''
            for p in providers
        )
        carousel = f'''<div class="prov-carousel">
        <button type="button" class="prov-carousel-arrow prov-carousel-prev" aria-label="Previous provider">{icon('chevron-left')}</button>
        <div class="prov-carousel-viewport">
          <div class="prov-carousel-track">{slides}</div>
        </div>
        <button type="button" class="prov-carousel-arrow prov-carousel-next" aria-label="Next provider">{icon('chevron-right')}</button>
      </div>'''
        return list_items, panels, carousel

    dpt_list, dpt_panels, dpt_carousel = list_and_detail(dpts, "Brad Klemetson")
    pta_list, pta_panels, pta_carousel = list_and_detail(ptas, ptas[0]['name'])

    hero = page_hero("Meet the Team", "Our Providers",
                      "Doctors of Physical Therapy and PTAs across all nine clinics &mdash; every one of them trained in MINT&rsquo;s hands-on, whole-person approach to recovery.",
                      ["Our Providers"], extra_class="prov-hero")

    body = f'''{hero}
  <section class="section prov-first-section">
    <div class="container prov-container">
      <div class="prov-tabs" role="tablist">
        <button type="button" class="prov-tab is-active" role="tab" aria-selected="true" data-tab-target="prov-panel-dpt">Doctors of Physical Therapy</button>
        <button type="button" class="prov-tab" role="tab" aria-selected="false" data-tab-target="prov-panel-pta">Physical Therapist Assistants</button>
      </div>
      <div class="prov-tab-panel is-active" id="prov-panel-dpt" role="tabpanel">
        <div class="prov-list-section">
          <div class="prov-split">
            <ul class="prov-list">{dpt_list}</ul>
            <div class="prov-detail-wrap">{dpt_panels}</div>
          </div>
          {dpt_carousel}
        </div>
      </div>
      <div class="prov-tab-panel" id="prov-panel-pta" role="tabpanel" hidden>
        <div class="prov-list-section">
          <div class="prov-split">
            <ul class="prov-list">{pta_list}</ul>
            <div class="prov-detail-wrap">{pta_panels}</div>
          </div>
          {pta_carousel}
        </div>
      </div>
    </div>
  </section>
  <section class="section prov-cta-section">
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
        <div class="accordion">
          <div class="accordion-item open">
            <button type="button" aria-expanded="true"><span>Overview</span>{icon('plus', cls='icon')}</button>
            <div class="panel" style="max-height:2000px"><div class="panel-inner"><p>{s['intro']}</p></div></div>
          </div>
          <div class="accordion-item">
            <button type="button" aria-expanded="false"><span>{s['causes_label']}</span>{icon('plus', cls='icon')}</button>
            <div class="panel"><div class="panel-inner">
              <ul class="list-check">
                {''.join(f"<li>{icon('check')} {c}</li>" for c in s['causes'])}
              </ul>
            </div></div>
          </div>
          <div class="accordion-item">
            <button type="button" aria-expanded="false"><span>How MINT Helps</span>{icon('plus', cls='icon')}</button>
            <div class="panel"><div class="panel-inner">
              <ul class="list-check">
                {''.join(f"<li>{icon('check')} {a}</li>" for a in s['approach'])}
              </ul>
            </div></div>
          </div>
        </div>

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
  <section class="section" style="padding:clamp(28px,4.5vw,60px) 0;">
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
  <section class="section" style="padding:clamp(28px,4.5vw,60px) 0;">
    <div class="container">
      <div class="grid-4">
        {''.join(f'''<div class="card-service"><div class="ico-wrap">{icon(p["icon"])}</div><h3>{p["title"]}</h3><p>{p["text"]}</p></div>''' for p in perks)}
      </div>
    </div>
  </section>
  <section class="section bg-stone" style="padding:clamp(28px,4.5vw,60px) 0;">
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
def terms_page():
    hero = page_hero("Legal", "Terms &amp; Conditions",
                      "Please read these terms carefully before using our website or scheduling services with us.",
                      ["Terms &amp; Conditions"])
    murray = next(l for l in LOCATIONS if l["slug"] == "murray")
    sections = [
        ("1. Acceptance of Terms",
         f'''<p>By accessing or using the website of MINT Physical Therapy (&ldquo;MINT PT,&rdquo; &ldquo;we,&rdquo; &ldquo;us,&rdquo; or &ldquo;our&rdquo;), located at <a href="https://www.mint-pt.com">www.mint-pt.com</a> (the &ldquo;Site&rdquo;), or by scheduling or receiving services from us, you agree to be bound by these Terms &amp; Conditions (&ldquo;Terms&rdquo;). If you do not agree to these Terms, please do not use the Site or our services.</p>'''),
        ("2. Use of This Website",
         '''<p>You agree to use the Site only for lawful purposes. You may not: use the Site in any way that violates applicable law; attempt to gain unauthorized access to our systems or data; copy, scrape, reproduce, or distribute Site content without permission; or interfere with the Site&rsquo;s operation or security. All content on the Site, including text, graphics, logos, and images, is the property of MINT PT or its licensors and may not be used without our written permission.</p>'''),
        ("3. Medical Disclaimer",
         '''<p>The content on this Site, including articles, blog posts, videos, and other materials, is provided for general informational and educational purposes only. It is not intended as, and should not be relied upon as, medical advice, diagnosis, or treatment. It does not replace the relationship between you and your physical therapist or other healthcare provider. Always consult a qualified healthcare professional before starting any exercise program or making decisions about your health. Individual results from physical therapy vary, and MINT PT makes no guarantee of specific outcomes.</p>'''),
        ("4. Emergency Situations",
         '''<p>This Site is not intended for use in medical emergencies. If you are experiencing a medical emergency, call 911 or go to your nearest emergency room immediately.</p>'''),
        ("5. Appointment Scheduling &amp; Cancellation Policy",
         '''<p>Appointments may be scheduled online, by phone, or in person. We require at least [24 hours] notice to cancel or reschedule an appointment. Late cancellations or missed appointments (&ldquo;no-shows&rdquo;) may be subject to a fee of [$XX]. Repeated no-shows may result in changes to our scheduling policy for your account. Arriving late to an appointment may result in a shortened session to accommodate the next scheduled patient.</p>'''),
        ("6. Payment &amp; Insurance",
         '''<p>Payment is due at the time services are rendered unless other arrangements have been made in advance. We accept [list accepted payment methods]. If we bill your insurance on your behalf, coverage and reimbursement are not guaranteed, and you remain responsible for any portion of charges not covered by your insurance plan, including deductibles, copays, and coinsurance. It is your responsibility to understand your insurance benefits.</p>'''),
        ("7. Patient Responsibilities",
         '''<p>To help ensure safe and effective care, you agree to: provide accurate and complete information about your health history and current condition; inform your treating clinician of any changes in your condition; follow your prescribed treatment plan and home exercise program; and communicate any concerns or adverse reactions to your care team promptly.</p>'''),
        ("8. Telehealth Services",
         '''<p>If you receive services via telehealth, you acknowledge that virtual visits have inherent limitations compared to in-person care, that a stable internet connection and compatible device are required, and that telehealth is not appropriate for medical emergencies. Additional telehealth consent may be required prior to your first virtual visit.</p>'''),
        ("9. Privacy &amp; HIPAA",
         '''<p>MINT PT is committed to protecting your personal and health information in accordance with the Health Insurance Portability and Accountability Act (HIPAA) and applicable state law. For details on how we collect, use, and protect your information, see our <a href="privacy-policy.html">Privacy Policy</a>.</p>'''),
        ("10. Text Message (SMS) Communications",
         '''<p>If you opt in to receive text messages from us, that program is governed by our separate SMS Terms &amp; Conditions.</p>'''),
        ("11. Testimonials &amp; Reviews",
         '''<p>Any patient testimonials or reviews shared on the Site reflect individual experiences and results, which vary from person to person. Testimonials are not a guarantee or prediction of the outcome you will experience.</p>'''),
        ("12. Third-Party Links",
         '''<p>The Site may contain links to third-party websites for your convenience. We do not control and are not responsible for the content, accuracy, or privacy practices of those sites. Use of any third-party site is at your own risk and subject to that site&rsquo;s own terms.</p>'''),
        ("13. Limitation of Liability",
         '''<p>To the fullest extent permitted by law, MINT PT and its owners, employees, and agents will not be liable for any indirect, incidental, special, or consequential damages arising from your use of the Site or our services. Nothing in these Terms is intended to limit any liability that cannot be limited under applicable law.</p>'''),
        ("14. Indemnification",
         '''<p>You agree to indemnify and hold harmless MINT PT, its owners, employees, and agents from any claims, damages, or expenses arising out of your violation of these Terms or misuse of the Site.</p>'''),
        ("15. Governing Law",
         '''<p>These Terms are governed by the laws of the State of Utah, without regard to conflict-of-law principles. Any disputes arising from these Terms or your use of the Site will be resolved in the state or federal courts located in Salt Lake City, Utah.</p>'''),
        ("16. Changes to These Terms",
         '''<p>We may revise these Terms from time to time. The updated version will be posted on this page with a revised effective date. Your continued use of the Site or our services after changes are posted constitutes acceptance of the updated Terms.</p>'''),
        ("17. Contact Us",
         f'''<p>If you have questions about these Terms, please contact us:</p>
         <ul>
           <li><strong>Business Name:</strong> Mint Physical Therapy</li>
           <li><strong>Address:</strong> {murray['addr1']}, {murray['city']}</li>
           <li><strong>Phone:</strong> <a href="tel:+1{PHONE_MAIN_TEL}">{PHONE_MAIN}</a></li>
           <li><strong>Email:</strong> <a href="mailto:{EMAIL_MAIN}">{EMAIL_MAIN}</a></li>
           <li><strong>Website:</strong> www.mint-pt.com</li>
         </ul>'''),
    ]
    sections_html = "".join(f"<h2>{title}</h2>{body}" for title, body in sections)
    body = f'''{hero}
  <section class="section">
    <div class="container">
      <div class="legal-content">
        <div class="legal-updated">Effective Date: August 5, 2026</div>
        {sections_html}
      </div>
    </div>
  </section>
'''
    return base_page("Terms & Conditions", "Terms and conditions for using the MINT Physical Therapy website and services.", body, active="")


def privacy_page():
    hero = page_hero("Legal", "Privacy Policy",
                      "How we collect, use, and protect your information.",
                      ["Privacy Policy"])
    murray = next(l for l in LOCATIONS if l["slug"] == "murray")
    sections = [
        ("1. Introduction",
         '''<p>This Privacy Policy explains how Mint Physical Therapy (&ldquo;MINT PT,&rdquo; &ldquo;we,&rdquo; &ldquo;us,&rdquo; or &ldquo;our&rdquo;) collects, uses, and shares information when you visit our website at www.mint-pt.com (the &ldquo;Site&rdquo;), submit a web form, schedule an appointment, or opt in to receive text messages from us. By using the Site or providing your information to us, you agree to the practices described in this Policy.</p>'''),
        ("2. Information We Collect",
         '''<p>We may collect the following types of information:</p>
         <ul>
           <li>Contact information: name, mailing address, email address, and phone number (including mobile number if you opt in to SMS)</li>
           <li>Health and treatment information: medical history, condition details, and treatment records provided as part of your care</li>
           <li>Insurance and payment information: insurance provider, policy details, and billing information</li>
           <li>Website usage information: pages visited, browser type, and device information, collected automatically through cookies or similar technologies</li>
           <li>Communication preferences: including your consent to receive text messages, email, or phone communications</li>
         </ul>'''),
        ("3. How We Use Your Information",
         '''<p>We use the information we collect to:</p>
         <ul>
           <li>Schedule, confirm, and remind you of appointments</li>
           <li>Provide physical therapy treatment and coordinate your care</li>
           <li>Process billing and insurance claims</li>
           <li>Communicate with you by phone, email, mail, or text message about your account or appointments</li>
           <li>Send practice updates and, where you have opted in, marketing or promotional messages</li>
           <li>Improve our website, services, and patient experience</li>
           <li>Comply with legal, regulatory, and recordkeeping obligations</li>
         </ul>'''),
        ("4. How We Share Your Information",
         '''<p>We do not sell your personal information. We may share your information only in the following circumstances:</p>
         <ul>
           <li>With your treating clinicians and staff at MINT PT to provide care</li>
           <li>With insurance companies, as needed to process claims and billing</li>
           <li>With service providers who perform functions on our behalf (such as scheduling software, billing, or text messaging platforms), under agreements that require them to protect your information</li>
           <li>When required by law, court order, or to protect the safety of a patient or others</li>
           <li>With your consent, or as otherwise described at the time you provide your information</li>
         </ul>'''),
        ("5. Text Messaging (SMS) Privacy",
         '''<p><strong>SMS consent is not shared with third parties or affiliates for marketing purposes.</strong> If you opt in to receive text messages from MINT PT, your mobile number and consent are used solely to send you the messages described in our SMS Terms &amp; Conditions (for example, appointment reminders, account notifications, practice updates, and where applicable, promotional messages). We do not share your phone number or SMS opt-in status with third parties or affiliates for their own marketing purposes.</p>
         <ul>
           <li>Message frequency may vary.</li>
           <li>Message and data rates may apply.</li>
           <li>To opt out at any time, text STOP.</li>
         </ul>
         <p>For assistance, text HELP or visit our website at www.mint-pt.com.</p>'''),
        ("6. Cookies &amp; Website Analytics",
         '''<p>Our Site may use cookies and similar tracking technologies to understand how visitors use the Site and to improve your experience. You can adjust your browser settings to refuse cookies, though some parts of the Site may not function properly without them.</p>'''),
        ("7. Data Security",
         '''<p>We use reasonable administrative, technical, and physical safeguards to protect your information from unauthorized access, use, or disclosure. However, no method of transmission or storage is completely secure, and we cannot guarantee absolute security.</p>'''),
        ("8. Your Choices &amp; Rights",
         '''<p>You may:</p>
         <ul>
           <li>Opt out of text messages at any time by replying STOP</li>
           <li>Opt out of marketing emails by using the unsubscribe link in any email</li>
           <li>Request access to, correction of, or a copy of your personal or health information by contacting us directly</li>
         </ul>
         <p>Protected health information (PHI) is additionally governed by our HIPAA Notice of Privacy Practices, available upon request.</p>'''),
        ("9. Children&rsquo;s Privacy",
         '''<p>Our Site and text messaging program are not directed to children under 13, and we do not knowingly collect personal information from children under 13 without parental consent. If you believe a child has provided us with personal information without appropriate consent, please contact us so we can remove it.</p>'''),
        ("10. Changes to This Policy",
         '''<p>We may update this Privacy Policy from time to time. Updates will be posted on this page with a revised effective date. Your continued use of the Site or our services after changes are posted constitutes acceptance of the updated Policy.</p>'''),
    ]
    sections_html = "".join(f"<h2>{title}</h2>{body}" for title, body in sections)
    body = f'''{hero}
  <section class="section">
    <div class="container">
      <div class="legal-content">
        <div class="legal-updated">Effective Date: August 5, 2026</div>
        {sections_html}
        <h2>Questions About This Policy?</h2>
        <p>If you have questions about this Privacy Policy, please contact us:</p>
        <ul>
          <li><strong>Business Name:</strong> Mint Physical Therapy</li>
          <li><strong>Address:</strong> {murray['addr1']}, {murray['city']}</li>
          <li><strong>Phone:</strong> <a href="tel:+1{PHONE_MAIN_TEL}">{PHONE_MAIN}</a></li>
          <li><strong>Email:</strong> <a href="mailto:{EMAIL_MAIN}">{EMAIL_MAIN}</a></li>
          <li><strong>Website:</strong> www.mint-pt.com</li>
        </ul>
      </div>
    </div>
  </section>
'''
    return base_page("Privacy Policy", "How MINT Physical Therapy collects, uses, and protects your information.", body, active="")


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
    write("privacy-policy.html", privacy_page())
    write("terms-and-conditions.html", terms_page())
    for s in SERVICES:
        write(f"services/{s['slug']}.html", service_detail_page(s))
    # favicon uses the real logo icon (assets/img/favicon-src.png, cropped
    # from the client's actual logo) — see generate_logo_assets.py

if __name__ == "__main__":
    main()
