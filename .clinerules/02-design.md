# 02-design — Design System Tokens (summarized §5)

- Principles: clarity, deference, depth; content first; one primary action; generous white space; motion explains
- Typography: iOS SF Pro system, Android Inter via google_fonts ss01 cv11 tabular, scale largeTitle 34/41/700 … caption 12/16/500, Dynamic Type 200%
- Colour: neutral quiet base + Foundry Indigo accent #4F46E5 light / #7C74FF dark, bg.primary #FFF/#000, bg.secondary #F5F5F7/#0B0B0D, bg.elevated, label.primary/secondary/tertiary, separator rgba, success/warning/danger, ai.tint 10%/16%, human.tint 10%/16%, WCAG AA 4.5:1
- Spacing 4pt grid 4,8,12,16,20,24,32,40,48 gutter 16/20, radii 10/14/20/28 ContinuousRectangleBorder, shadows only floating 0 8 24 rgba(0,0,0,0.08), touch ≥44×44
- Glassmorphism sparingly: only tab bar, nav bar scrolled, composer, modal grabber; blur sigma 24, fill rgba(255,255,255,0.72)/rgba(28,28,30,0.68), 0.5pt hairline separator, saturation 1.8×, fallback solid if highContrast/reduce-transparency, never glass over glass
- Icons: Lucide 1.75pt 20/24/28, CupertinoIcons on iOS, one family per screen
- Avatars: humans photo/initials on human.tint, AI geometric monogram gradient squircle accent→accent70% + sparkle badge
- Illustrations: empty states only monoline two-tone 160pt max
- Org Pulse: CustomPainter living graph Founder top Assistant beneath roles nodes, lines 1–3pt by volume accent 35% opacity, dot 1.6s ease-in-out on new message live from Realtime, node ring states idle/working/awaiting/human-led, tap node→role sheet tap line→thread, respect reduce-motion
- Motion: spring stiffness 300 damping 30, durations 200–350ms, page transitions platform default, message 8pt rise+fade 220ms, haptics lightImpact send selection segmented success notification approval warning reject, respect disableAnimations
- Navigation: 5 tabs Home Messages Schedule Approvals Company glass tab bar, Genesis 5 steps progress accent line, Home greeting Today Approvals reports Ask composer, Messages thread list pinned Assistant AI/human badges unread bubbles accent/bg.secondary/ai.tint report cards citation chips voice waveform files tiles shimmer streaming, Composer glass pill + growing 6 lines mic→send hold waveform slide cancel Transcribing editable, Schedule week strip agenda New meeting sheet, Meeting room turn-by-turn Resolutions drawer Confirm→timeline, Approvals swipe approve/reject undo 5s detail reasoning impact Ask changes, Company Org Pulse Charter OKR rings roles Workforce Report Assign human Copilot, Role profile mandate KPIs sparklines tasks outputs mode toggle chat, Settings profile notifications appearance data export sign out
- Copy: short warm direct sentence case agents sign role title errors what happened + what to do
