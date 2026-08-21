# MINT Physical Therapy — Website Redesign

A full redesign of the MINT Physical Therapy website (mint-pt.com): 18 static
HTML pages, no build step required, ready to publish on GitHub Pages, Netlify,
Vercel, or any static host.

## What's here

```
index.html            Home
locations.html         All 9 clinics
providers.html         All 16 providers (10 DPTs + 6 PTAs)
services.html          Services & specialties hub
contact.html           Request-an-appointment form
join-team.html         Careers page
services/*.html        12 individual service detail pages
assets/css/style.css   The entire design system (colors, type, components)
assets/js/main.js      Nav dropdowns, mobile menu, accordions, form handling
assets/img/            Favicon
build.py               Optional: regenerates all HTML from the data + templates below
icons.py                The hand-drawn icon set used across the site
```

## How to publish this on GitHub Pages

1. Create a new repository on GitHub (e.g. `mint-pt-website`).
2. Upload everything in this folder to the repo (drag-and-drop on github.com
   works fine, or `git add . && git commit -m "Redesign" && git push`).
3. In the repo, go to **Settings → Pages**, set the source to the `main`
   branch, root folder, and save.
4. Your site will be live at `https://<your-username>.github.io/mint-pt-website/`
   within a minute or two.

No npm install, no build command — the site is plain HTML/CSS/JS and works
as-is straight out of the repo.

## Editing content

Every page was generated from `build.py`, which keeps the header, footer, and
navigation identical across all 18 pages. **If you want to make a small wording
or contact-info tweak, it's fastest to just edit the HTML file directly** —
find the text and change it, no need to touch Python.

If you want to add a new clinic, add a new provider, or add a new service
page (and have it automatically show up in the nav, footer, and services hub
everywhere), it's easier to edit `build.py`:

1. Open `build.py`
2. Find the `LOCATIONS`, `PROVIDERS`, or `SERVICES` list near the top
3. Add a new entry following the same pattern as the ones around it
4. Run `python3 build.py` in this folder (requires Python 3, no other
   dependencies) — it regenerates every HTML file in a few seconds
5. Commit and push the updated files

## Things to double check / finish before launch

- **Phone numbers are placeholders.** Every phone and fax number across the
  site currently reads `555-555-5555` on purpose. Before launch, replace
  `PHONE_MAIN` near the top of `build.py` with the real main number, and
  update the `phone` / `fax` fields in the `LOCATIONS` list with each
  clinic's real number, then run `python3 build.py` to regenerate every
  page. (Or, if you'd rather not touch Python, find-and-replace
  `555-555-5555` directly in the HTML files — it appears in the nav, the
  hero, the footer, every service page's CTA, and the contact page.)
- **Brigham City Clinic** — I didn't have a street address for this location
  in the source material, so the page currently says "Call for suite
  details." Update this in `build.py` (search for `brigham-city`) once you
  have the address, or edit `locations.html` directly.
- **Provider bios** — the original site had bios hidden behind dropdown
  arrows that weren't visible in the screenshots I worked from, so I wrote
  short, warm, generic placeholder bios for all 16 providers. Swap in real
  bios whenever you have them (each one is a one-line `bio="..."` entry in
  `build.py`, or just find-and-replace the text directly in `providers.html`).
- **Photography** — the site currently uses icon-based and gradient/topo-line
  visuals instead of photos, since I didn't want to guess at or fabricate
  real photography. Swap in real clinic, team, and action photos wherever
  you have them — the design has clear spots built for it (hero, provider
  cards, location cards).
- **Video** — the homepage and podcast section have a styled placeholder
  video frame ready to go. Once you have real video, replace the
  `.video-frame` block's contents with a real `<video>` tag or embedded
  YouTube iframe.
- **Appointment form** — the Contact page form currently just shows an
  in-page "thanks" message on submit; it isn't wired up to actually send
  anywhere yet. To make it functional, sign up for a free plan on something
  like [Formspree](https://formspree.io) or use
  [Netlify Forms](https://docs.netlify.com/forms/setup/) if you host there,
  and add the `action="..."` attribute to the `<form id="appointment-form">`
  tag in `contact.html` (see the comment in `assets/js/main.js` for the
  exact spot).
- **Clinic hours** — I only had confirmed hours for the Ogden clinic
  (Mon–Fri, 7am–6pm) from the source screenshots, so that's shown as the
  assumed default for all clinics with a note asking visitors to call and
  confirm. Update per-clinic if hours actually differ.
- **Social links** — Facebook, Instagram, YouTube, and Spotify links in the
  footer and podcast section were verified against MINT's real accounts at
  the time of writing. Worth a quick check that they're still current before
  launch.

## Design notes

The visual direction ties into the existing MINT logo (a mountain mark) and
Utah setting: recovery is framed as an ascent — a steady climb back to where
you want to be, expressed through:

- A recurring topographic contour-line motif in the background of dark
  sections
- A "recovery ascent" elevation-chart graphic in the homepage hero
- A refined version of the brand's mint/forest green, paired with warm stone
  neutrals and a small amount of sunrise gold for CTAs and highlights
- Space Grotesk for headlines, Inter for body copy, IBM Plex Mono for small
  labels (trail-marker-style eyebrows, stats, addresses)

Everything is responsive down to mobile, keyboard-navigable, and respects
`prefers-reduced-motion`.
