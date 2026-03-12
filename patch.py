#!/usr/bin/env python3
"""
QIPP Dashboard — Style Patch
Run: python patch.py
Input:  paste.txt  (your file:17 — latest dashboard)
Output: dashboard_patched.html
"""

import sys, re

INPUT  = "paste.txt"
OUTPUT = "dashboard_patched.html"

with open(INPUT, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Loaded: {len(html):,} chars")
result = html
changes = []

# ─────────────────────────────────────────────
# 1. CSS VARIABLES  — add ACWA compat vars to :root
# ─────────────────────────────────────────────
OLD_ROOT_LINE = "--bg-body: #F9F7FC;"
NEW_ROOT_LINE = """--bg-body: #F9F7FC;
            /* ACWA Power website compatibility */
            --primary-shade1: 146, 115, 218;
            --primary-shade2: 46, 32, 68;
            --secondary-shade1: 210, 240, 80;
            --light-color: 255, 255, 255;
            --dark-color: 0, 0, 0;
            --common-radius: 12px;
            --border-raduis-card: 4px;"""

if OLD_ROOT_LINE in result and "--primary-shade1" not in result:
    result = result.replace(OLD_ROOT_LINE, NEW_ROOT_LINE, 1)
    changes.append("✅ CSS variables added to :root")
else:
    changes.append("⚠️  CSS variables: already present or marker not found")

# ─────────────────────────────────────────────
# 2. NAVBAR FIX  — remove conflicting padding-left
# ─────────────────────────────────────────────
OLD_NAV = ".acwa-navbar { padding-left: 2rem !important;"
NEW_NAV = ".acwa-navbar {"

if OLD_NAV in result:
    result = result.replace(OLD_NAV, NEW_NAV, 1)
    changes.append("✅ Navbar: removed conflicting padding-left")
else:
    changes.append("⚠️  Navbar: marker not found (may already be fixed)")

# ─────────────────────────────────────────────
# 3. FOOTER CSS  — inject before .brand-footer {
# ─────────────────────────────────────────────
FOOTER_CSS = """
        /* ══ ACWA POWER FOOTER (acwapower.com style) ══ */
        .acwa-footer {
            background-color: #150c24;
            font-family: 'Montserrat', sans-serif;
            margin-top: auto;
        }
        .acwa-footer .footer-top-band {
            background: linear-gradient(90deg, #2E2044 0%, #1e1333 100%);
            padding: 60px 80px 50px;
            display: grid;
            grid-template-columns: 260px 1fr;
            gap: 80px;
            align-items: start;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .acwa-footer .ft-brand { display: flex; flex-direction: column; gap: 18px; }
        .acwa-footer .ft-logo-row { display: flex; align-items: center; gap: 12px; }
        .acwa-footer .ft-logo-img { width: 34px; height: 34px; object-fit: contain; }
        .acwa-footer .ft-brand-name {
            color: #fff; font-size: 16px; font-weight: 700;
            letter-spacing: .08em; text-transform: uppercase;
        }
        .acwa-footer .ft-motto {
            color: var(--brand-lime);
            font-size: 12px; font-weight: 600;
            letter-spacing: .05em; text-transform: uppercase;
            line-height: 1.6; max-width: 190px;
        }
        .acwa-footer .ft-social { display: flex; gap: 10px; margin-top: 4px; }
        .acwa-footer .ft-social a {
            width: 34px; height: 34px;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            color: rgba(255,255,255,0.7);
            text-decoration: none; font-size: 13px;
            transition: all 0.2s;
        }
        .acwa-footer .ft-social a:hover {
            border-color: var(--brand-lime);
            color: var(--brand-lime);
            background: rgba(210,240,80,0.08);
        }
        .acwa-footer .ft-links-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 40px;
        }
        .acwa-footer .ft-col-title {
            color: var(--brand-lime);
            font-size: 11px; font-weight: 700;
            letter-spacing: .12em; text-transform: uppercase;
            margin-bottom: 14px;
        }
        .acwa-footer .ft-col-links { display: flex; flex-direction: column; gap: 10px; }
        .acwa-footer .ft-col-links a {
            color: rgba(255,255,255,0.65);
            text-decoration: none; font-size: 13px; font-weight: 500;
            transition: color 0.2s; line-height: 1.4;
        }
        .acwa-footer .ft-col-links a:hover { color: #fff; }
        .acwa-footer .footer-bottom-band {
            background: #0e0820;
            padding: 16px 80px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap; gap: 10px;
        }
        .acwa-footer .ft-copy { color: rgba(255,255,255,0.4); font-size: 12px; }
        .acwa-footer .ft-legal { display: flex; gap: 22px; }
        .acwa-footer .ft-legal a {
            color: rgba(255,255,255,0.4);
            text-decoration: none; font-size: 12px;
            transition: color 0.2s;
        }
        .acwa-footer .ft-legal a:hover { color: rgba(255,255,255,0.75); }
        @media (max-width: 1024px) {
            .acwa-footer .footer-top-band { grid-template-columns: 1fr; padding: 40px 30px; }
            .acwa-footer .ft-links-grid { grid-template-columns: repeat(2,1fr); }
            .acwa-footer .footer-bottom-band { padding: 14px 30px; }
        }
        @media (max-width: 600px) {
            .acwa-footer .ft-links-grid { grid-template-columns: 1fr 1fr; gap: 22px; }
        }
"""

MARKER = ".brand-footer {"
if MARKER in result:
    result = result.replace(MARKER, FOOTER_CSS + "\n        " + MARKER, 1)
    changes.append("✅ Footer CSS injected")
else:
    changes.append("⚠️  Footer CSS: .brand-footer marker not found")

# ─────────────────────────────────────────────
# 4. FOOTER HTML  — replace <footer class="brand-footer">...</footer>
# ─────────────────────────────────────────────
NEW_FOOTER_HTML = """<footer class="acwa-footer">
    <!-- TOP BAND -->
    <div class="footer-top-band">
        <div class="ft-brand">
            <div class="ft-logo-row">
                <img src="https://www.acwapower.com/images/favicon.png"
                     alt="ACWA Power" class="ft-logo-img">
                <span class="ft-brand-name">ACWA&nbsp;POWER</span>
            </div>
            <p class="ft-motto">Delivering power.<br>Improving lives.</p>
            <div class="ft-social">
                <a href="https://www.linkedin.com/company/acwa-power" target="_blank" title="LinkedIn">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                </a>
                <a href="https://x.com/ACWAPower" target="_blank" title="X / Twitter">
                    <svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.746l7.73-8.835L1.254 2.25H8.08l4.253 5.622L18.244 2.25zm-1.161 17.52h1.833L7.084 4.126H5.117L17.083 19.77z"/></svg>
                </a>
                <a href="https://www.youtube.com/@ACWAPower" target="_blank" title="YouTube">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M23.495 6.205a3.007 3.007 0 00-2.088-2.088c-1.87-.501-9.396-.501-9.396-.501s-7.507-.01-9.396.501A3.007 3.007 0 00.527 6.205a31.247 31.247 0 00-.522 5.805 31.247 31.247 0 00.522 5.783 3.007 3.007 0 002.088 2.088c1.868.502 9.396.502 9.396.502s7.506 0 9.396-.502a3.007 3.007 0 002.088-2.088 31.247 31.247 0 00.5-5.783 31.247 31.247 0 00-.5-5.805zM9.609 15.601V8.408l6.264 3.602z"/></svg>
                </a>
            </div>
        </div>
        <div class="ft-links-grid">
            <div>
                <p class="ft-col-title">Company</p>
                <div class="ft-col-links">
                    <a href="https://www.acwapower.com/en/who-we-are/" target="_blank">Who We Are</a>
                    <a href="https://www.acwapower.com/en/what-we-do/" target="_blank">What We Do</a>
                    <a href="https://www.acwapower.com/en/sustainability/" target="_blank">Sustainability</a>
                    <a href="https://www.acwapower.com/en/investors/" target="_blank">Investors</a>
                </div>
            </div>
            <div>
                <p class="ft-col-title">Solutions</p>
                <div class="ft-col-links">
                    <a href="#">Power Generation</a>
                    <a href="#">Water Desalination</a>
                    <a href="#">Green Hydrogen</a>
                    <a href="#">Energy Storage</a>
                </div>
            </div>
            <div>
                <p class="ft-col-title">QIPP Systems</p>
                <div class="ft-col-links">
                    <a href="https://www.successfactors.com" target="_blank">SuccessFactors</a>
                    <a href="https://www.synergilife.com" target="_blank">Synergi Life</a>
                    <a href="https://www.sap.com/products/erp/s4hana.html" target="_blank">SAP S/4HANA</a>
                    <a href="https://qipp-ops.github.io/calendar" target="_blank">Ops Calendar</a>
                </div>
            </div>
            <div>
                <p class="ft-col-title">Life at ACWA</p>
                <div class="ft-col-links">
                    <a href="https://www.acwapower.com/en/life-at-acwa-power/" target="_blank">Our Culture</a>
                    <a href="https://www.acwapower.com/en/life-at-acwa-power/careers/" target="_blank">Careers</a>
                    <a href="#">Planned Leaves</a>
                    <a href="#">HR Policies</a>
                </div>
            </div>
        </div>
    </div>
    <!-- BOTTOM BAND -->
    <div class="footer-bottom-band">
        <span class="ft-copy">
            &copy; 2026 ACWA Power. All rights reserved. &nbsp;|&nbsp; QIPP — Operations Dashboard
        </span>
        <div class="ft-legal">
            <a href="https://www.acwapower.com/en/privacy-policy/" target="_blank">Privacy Policy</a>
            <a href="https://www.acwapower.com/en/terms-and-conditions/" target="_blank">Terms &amp; Conditions</a>
            <a href="#">Cookie Settings</a>
        </div>
    </div>
</footer>"""

footer_start = result.find('<footer class="brand-footer">')
footer_end   = result.find('</footer>', footer_start) + len('</footer>')
if footer_start >= 0:
    result = result[:footer_start] + NEW_FOOTER_HTML + result[footer_end:]
    changes.append("✅ Footer HTML replaced")
else:
    changes.append("⚠️  Footer HTML: <footer class=\"brand-footer\"> not found")

# ─────────────────────────────────────────────
# WRITE OUTPUT
# ─────────────────────────────────────────────
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(result)

print("\n".join(changes))
print(f"\n✔  Saved → {OUTPUT}  ({len(result):,} chars)")
