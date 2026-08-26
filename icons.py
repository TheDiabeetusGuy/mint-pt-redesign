# Minimal hand-drawn line-icon set, 24x24 viewbox, stroke-based.
# Kept deliberately simple/consistent so the whole site reads as one system.

ICONS = {
"mountain": '<path d="M2 19h20L15.5 6 11 13.5 8.5 10 2 19z"/><path d="M6 19l3.2-4.8"/>',
"chev-down": '<path d="M6 9l6 6 6-6"/>',
"arrow-right": '<path d="M4 12h16"/><path d="M14 6l6 6-6 6"/>',
"phone": '<path d="M4 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v4a2 2 0 0 1-2 2C9.6 21 3 14.4 3 6a2 2 0 0 1 2-2z"/>',
"mail": '<path d="M3 5h18v14H3z"/><path d="M3 6l9 7 9-7"/>',
"pin": '<path d="M12 22s7-7.4 7-12.5A7 7 0 0 0 5 9.5C5 14.6 12 22 12 22z"/><circle cx="12" cy="9.5" r="2.4"/>',
"clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
"facebook": '<path d="M14 9h3V5.5h-3C11.8 5.5 10 7.3 10 9.5V11H8v3.5h2V21h3.5v-6.5h2.7L17 11h-3.5V9.7c0-.4.3-.7.5-.7z"/>',
"instagram": '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r="0.8" fill="currentColor" stroke="none"/>',
"youtube": '<rect x="2.5" y="5.5" width="19" height="13" rx="3.5"/><path d="M10.5 9.3v5.4l5-2.7z" fill="currentColor" stroke="none"/>',
"spotify": '<circle cx="12" cy="12" r="9.2"/><path d="M7 10.2c3-.8 7-.5 9.6 1"/><path d="M7.4 13c2.5-.6 5.7-.4 8 .9"/><path d="M8 15.6c2-.5 4.5-.3 6.2.7"/>',
"play": '<path d="M8 5.5v13l11-6.5z" fill="currentColor" stroke="none"/>',
"check": '<path d="M4 12.5l5 5L20 6.5"/>',
"menu": '<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/>',
"x": '<path d="M5 5l14 14"/><path d="M19 5L5 19"/>',
"star": '<path d="M12 3l2.6 5.9 6.4.6-4.8 4.3 1.4 6.3L12 17l-5.6 3.1 1.4-6.3-4.8-4.3 6.4-.6z"/>',
"quote": '<path d="M8 9c-2.2 0-3.8 1.8-3.8 4.4C4.2 16 6 18 8.4 18v-3.4C7 14.6 6.4 14 6.4 13c0-1 .7-1.6 1.8-1.7V9zm9 0c-2.2 0-3.8 1.8-3.8 4.4 0 2.6 1.8 4.6 4.2 4.6v-3.4c-1.4 0-2-.6-2-1.6 0-1 .7-1.6 1.8-1.7V9z" fill="currentColor" stroke="none"/>',
"plus": '<path d="M12 5v14"/><path d="M5 12h14"/>',
"spine": '<path d="M12 2v20"/><path d="M8 5h8"/><path d="M7 9h10"/><path d="M8 13h8"/><path d="M7 17h10"/>',
"leg": '<circle cx="9" cy="5" r="2.2"/><path d="M9 7.5v6l4 3.5-1 5"/><path d="M13 13l4 1.5"/>',
"pulse": '<path d="M3 12h4l2-7 4 14 2-9 2 2h4"/>',
"knee": '<path d="M9 3v7l-3 4v7"/><path d="M9 10h5l3 4v6"/><circle cx="10.5" cy="11.5" r="1.6"/>',
"shoulder": '<path d="M4 15c0-5 3.5-9 8-9s8 4 8 9"/><path d="M8 15v6"/><path d="M16 15v6"/>',
"head": '<circle cx="12" cy="10" r="6"/><path d="M9 10h.01"/><path d="M15 10h.01"/><path d="M9 20l1.5-4"/><path d="M15 20l-1.5-4"/>',
"brain": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-1 5.8A3 3 0 0 0 8 17a3 3 0 0 0 5-2V6a2 2 0 0 0-4-1z"/><path d="M15 4a3 3 0 0 1 3 3 3 3 0 0 1 1 5.8A3 3 0 0 1 16 17a3 3 0 0 1-3-2"/>',
"lungs": '<path d="M12 3v9"/><path d="M12 12c0-2-2-2-3-1L6 14c-1.5 1.5-1.5 6 1 6 2 0 3-2 3-4v-4z"/><path d="M12 12c0-2 2-2 3-1l3 3c1.5 1.5 1.5 6-1 6-2 0-3-2-3-4v-4z"/>',
"needle": '<path d="M20 4L10 14"/><path d="M15 4l5 5"/><path d="M4 20l5-2 1.5-4.5L7 10 4 20z"/>',
"waves": '<path d="M3 9c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/><path d="M3 15c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/>',
"car": '<path d="M3 16V12l2.5-5h9L17 12v4"/><path d="M3 16h14"/><circle cx="7" cy="16.5" r="1.6"/><circle cx="15" cy="16.5" r="1.6"/>',
"briefcase": '<rect x="3" y="8" width="18" height="11" rx="2"/><path d="M8 8V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
"users": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14.2A5 5 0 0 1 21 20"/>',
"award": '<circle cx="12" cy="9" r="5"/><path d="M9 13.5L8 21l4-2 4 2-1-7.5"/>',
"heart": '<path d="M12 20s-7-4.5-9.3-9C1 7 3 4 6.3 4c2 0 3.6 1.2 5.7 4 2.1-2.8 3.7-4 5.7-4C21 4 23 7 21.3 11c-2.3 4.5-9.3 9-9.3 9z"/>',
"target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r=".6" fill="currentColor" stroke="none"/>',
"calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 9.5h17"/><path d="M8 3v4"/><path d="M16 3v4"/>',
"shield": '<path d="M12 3l7 3v6c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4.5"/>',
"home-ico": '<path d="M4 11l8-7 8 7"/><path d="M6 10v9h12v-9"/>',
"navigate": '<path d="M3 11l16-7-7 16-2-7z"/>',
"squat": '<circle cx="12" cy="4" r="2"/><path d="M12 6v5"/><path d="M8 9h8"/><path d="M12 11l-4 4v4"/><path d="M12 11l4 4v4"/>',
"run": '<circle cx="15" cy="4" r="2"/><path d="M15 6l-3 6"/><path d="M15 8l3-2"/><path d="M13 9l-3 2"/><path d="M12 12l3 4-1 5"/><path d="M12 12l-4 2 1 6"/>',
}

def icon(name, cls="icon", extra=""):
    body = ICONS.get(name, "")
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" {extra}>{body}</svg>'
