# Dashboard design

Software: a market analytics workspace. Main action: Compare assets.
Taste palette: charcoal-room-sage, selected as the first fintech deal; subdued sage keeps emphasis on plotted data. Pairing: Chivo and Chivo Mono. Retain the generated color and font tokens.

This is the working analytics application, with a compact navigation rail, filters, chart, metric table, correlation matrix, and query browser. Full-screen marketing heroes, decorative shaders, looping charts and photo sections do not serve this workflow. Data provenance labels and chart labels remain visible because they are essential to interpreting the analysis.

Emil principles: fast 160ms control feedback, explicit focus rings, native labeled inputs, press feedback, no animated financial data, reduced-motion support, and hover effects restricted to pointer devices.

Functional checks cover date filters, invalid windows, exports, SQLite filtering/pagination, provenance, and responsive overflow. Browser math is also compared against Python output for every exported metric. Taste gate outcome will be recorded after the production build.

## Gate result
GATE: ERROR. The Taste checker could not reserve a local port in 5200–5299, so consistency/layout reports and rendered-copy lint did not run. The checker instructed not to rerun. This is not a claimed design-gate pass. Production Playwright screenshots and functional checks are recorded separately.

## Browser validation
Production build succeeded. Six Playwright checks passed locally, including all five viewport widths (1440, 1024, 768, 390 and 320), database exports, filters and reduced motion. Three Node tests passed, including numerical agreement with all Python-exported metrics. Screenshots were reviewed at desktop and phone sizes. An exact-label selector initially failed; explicit asset labels corrected it. Mobile SVG labels were enlarged before the final passing run.
