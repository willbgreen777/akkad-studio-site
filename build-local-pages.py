#!/usr/bin/env python3
"""
Generates the local landing pages for Akkad Studio.

WHY THESE EXIST: the whole point is that a business owner searching
"web designer near me" lands on a page, reads it, and types into a form.
The first human move is theirs. Nobody has to be cold-contacted.

Run:  python3 build-local-pages.py
"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).parent

CITIES = [
    dict(slug="springdale",  city="Springdale",  county="Washington County",
         near="Fayetteville, Rogers and Lowell",
         blurb="Springdale runs on trades and family businesses — shops, salons, contractors, restaurants along Thompson and Sunset."),
    dict(slug="fayetteville", city="Fayetteville", county="Washington County",
         near="Springdale, Farmington and Greenland",
         blurb="Fayetteville customers look you up before they walk in. On Dickson, on College, near the square — the phone search happens first."),
    dict(slug="rogers",      city="Rogers",      county="Benton County",
         near="Bentonville, Lowell and Bella Vista",
         blurb="Rogers has grown fast, and plenty of good businesses here still have a website built years before the growth."),
    dict(slug="bentonville", city="Bentonville", county="Benton County",
         near="Rogers, Centerton and Bella Vista",
         blurb="Bentonville holds businesses to a high standard on presentation. A dated site costs you more here than almost anywhere."),
]

NAV_SVG = ('<svg viewBox="0 0 100 100" width="40" height="40" aria-hidden="true">'
           '<polygon points="50,12 88,86 12,86" fill="none" stroke="#35c46b" stroke-width="7" stroke-linejoin="round"/>'
           '<polygon points="50,42 66,72 34,72" fill="#35c46b"/></svg>')

STYLE = """
  :root{--navy:#0a0a0b;--navy-2:#111114;--navy-3:#17171c;--gold:#35c46b;--gold-soft:#7ee0a4;--muted:#a3a3a8;--line:rgba(255,255,255,.10);--card:#111114}
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif;background:var(--navy);color:#f2f2ef;line-height:1.65;-webkit-font-smoothing:antialiased}
  .wrap{max-width:900px;margin:0 auto;padding:0 24px}
  a{color:inherit;text-decoration:none}
  header.nav{position:sticky;top:0;z-index:50;background:rgba(10,10,11,.82);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
  .nav-inner{display:flex;align-items:center;justify-content:space-between;height:72px;max-width:1120px;margin:0 auto;padding:0 24px}
  .brand{display:flex;align-items:center;gap:12px;font-weight:bold;letter-spacing:.5px}
  .brand b{font-size:19px}
  .brand span.k{color:var(--gold);font-size:12px;letter-spacing:2px;display:block;font-family:'Helvetica Neue',Arial,sans-serif}
  nav.links{display:flex;gap:24px;font-family:'Helvetica Neue',Arial,sans-serif;font-size:14px;color:var(--muted);flex-wrap:wrap;justify-content:flex-end;row-gap:4px}
  @media(max-width:720px){.nav-inner{height:auto;padding:12px 20px;flex-wrap:wrap;gap:8px}nav.links{gap:16px;font-size:13.5px;width:100%;justify-content:flex-start}}
  nav.links a:hover{color:var(--gold)}
  .eyebrow{font-family:'Helvetica Neue',Arial,sans-serif;font-size:12px;letter-spacing:3px;color:var(--gold);text-transform:uppercase;margin-bottom:14px}
  h1{font-size:clamp(30px,5vw,46px);line-height:1.15;letter-spacing:-.5px;margin-bottom:16px}
  h1 em{color:var(--gold-soft);font-style:italic}
  h2{font-size:26px;margin:38px 0 12px;letter-spacing:-.2px}
  h3{font-size:17px;margin:0 0 6px;color:var(--gold-soft);font-family:'Helvetica Neue',Arial,sans-serif}
  p{color:#c8c8ce;margin:12px 0}
  .sub{font-size:19px;color:var(--muted)}
  section{padding:54px 0}
  .hero{padding:70px 0 40px;border-bottom:1px solid var(--line)}
  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin-top:22px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px}
  .card p{font-size:15px;margin:0}
  .price{background:var(--navy-2);border:1px solid var(--line);border-radius:14px;padding:26px;margin-top:22px}
  .price .big{font-size:34px;color:var(--gold);font-weight:bold}
  ul{margin:12px 0 12px 22px;color:#c8c8ce}
  li{padding:4px 0}
  .btn{display:inline-block;padding:14px 26px;border-radius:10px;font-family:'Helvetica Neue',Arial,sans-serif;font-size:15px;font-weight:600;letter-spacing:.3px;border:1px solid var(--gold);margin:6px 8px 6px 0}
  .btn-gold{background:var(--gold);color:#0a0a0b}
  .btn-ghost{color:var(--gold)}
  form{background:var(--navy-2);border:1px solid var(--line);border-radius:14px;padding:26px;margin-top:20px}
  label{display:block;font-family:'Helvetica Neue',Arial,sans-serif;font-size:13px;letter-spacing:.4px;color:var(--muted);margin:14px 0 6px}
  input,textarea,select{width:100%;padding:12px 14px;background:#17171c;border:1px solid var(--line);border-radius:8px;color:#f2f2ef;font-family:'Helvetica Neue',Arial,sans-serif;font-size:15px}
  textarea{min-height:110px;resize:vertical}
  button{margin-top:18px;padding:14px 28px;background:var(--gold);color:#0a0a0b;border:0;border-radius:10px;font-family:'Helvetica Neue',Arial,sans-serif;font-size:16px;font-weight:700;cursor:pointer}
  .fineprint{font-size:13px;color:var(--muted);margin-top:14px}
  footer{border-top:1px solid var(--line);padding:34px 0;color:var(--muted);font-size:14px;margin-top:30px}
  .near{font-size:14px;color:var(--muted);margin-top:26px}
  .near a{color:var(--gold-soft)}
"""

def nav(depth=""):
    return f"""<header class="nav"><div class="nav-inner">
  <a class="brand" href="{depth}index.html">{NAV_SVG}<div><b>AKKAD STUDIO</b><span class="k">WEB &amp; DIGITAL DESIGN</span></div></a>
  <nav class="links"><a href="{depth}index.html">Home</a><a href="{depth}index.html#work">Our work</a><a href="{depth}index.html#how">How it works</a><a href="{depth}index.html#price">Price</a><a href="{depth}contact.html">Start a project</a></nav>
</div></header>"""

FOOTER = """<footer><div class="wrap">
  Akkad Studio — web &amp; digital design for small businesses in Northwest Arkansas.<br>
  We work by email so everything you agree to is in writing. © 2026 Akkad Studio.
</div></footer>"""

def page(c):
    t = f"Web Design in {c['city']}, AR — Akkad Studio"
    d = (f"Website design for {c['city']}, Arkansas small businesses. Sites from $500, "
         f"optional $99/month care plan. See a working example before you decide.")
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="https://akkadstudio.com/web-design-{c['slug']}.html">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="https://akkadstudio.com/web-design-{c['slug']}.html">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"ProfessionalService",
"name":"Akkad Studio","description":"Website design and maintenance for small businesses in {c['city']}, Arkansas.",
"url":"https://akkadstudio.com/web-design-{c['slug']}.html",
"areaServed":{{"@type":"City","name":"{c['city']}","containedInPlace":{{"@type":"State","name":"Arkansas"}}}},
"serviceType":"Web design","priceRange":"$$",
"makesOffer":[{{"@type":"Offer","name":"Small business website","priceCurrency":"USD","price":"500"}},
{{"@type":"Offer","name":"Care Plan","priceCurrency":"USD","price":"99"}}]}}
</script>
<style>{STYLE}</style></head><body>
{nav()}
<main>
<section class="hero"><div class="wrap">
  <div class="eyebrow">{c['city']}, Arkansas</div>
  <h1>Website design for <em>{c['city']}</em> small businesses.</h1>
  <p class="sub">Sites from $500. An optional $99/month plan if you'd rather never think about it again. We work entirely by email, so everything you agree to is in writing.</p>
  <div style="margin-top:22px">
    <a class="btn btn-gold" href="contact.html">Start a project</a>
    <a class="btn btn-ghost" href="index.html#work">See working examples</a>
  </div>
</div></section>

<section><div class="wrap">
  <h2>Built for how {c['city']} actually finds you</h2>
  <p>{c['blurb']} Almost all of them start the same way — someone pulls out a phone, searches, and picks from what loads fast and looks trustworthy.</p>
  <p>If your site is slow, hard to read on a phone, or missing entirely, that decision gets made without you in it. That's the whole problem we fix.</p>
  <div class="cards">
    <div class="card"><h3>Loads fast on a phone</h3><p>Most of your visitors are on a phone, often on mobile data. Every page we build is quick and readable there first.</p></div>
    <div class="card"><h3>Says what you do</h3><p>What you offer, where you are, when you're open, and how to reach you — visible without scrolling or hunting.</p></div>
    <div class="card"><h3>Found on Google</h3><p>Set up properly so searches for your kind of business in {c['city']} can actually turn you up.</p></div>
    <div class="card"><h3>Kept current</h3><p>Hours change, prices change, seasons change. On a care plan you email us and it's done — no dashboard to learn.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>What it costs</h2>
  <div class="price">
    <div class="big">$500</div>
    <p>A complete small-business site. Includes the build, your domain, and getting it live. Half up front, half when it goes live.</p>
    <ul>
      <li>Up to five pages, written for you — you don't have to supply copy</li>
      <li>Your photos, hours, location and contact details</li>
      <li>Mobile-first, fast, and set up to be findable</li>
      <li>Ready in about a week from when you send your photos</li>
    </ul>
  </div>
  <div class="price">
    <div class="big">$99<span style="font-size:17px;color:var(--muted)">/month</span></div>
    <p><b>Optional.</b> Hosting, security, backups, and unlimited small changes — you email what you want changed and we do it. Cancel any time.</p>
  </div>
</div></section>

<section><div class="wrap">
  <h2>Look before you decide</h2>
  <p>We'd rather show you than describe it. These are real working examples, not screenshots:</p>
  <div class="cards">
    <div class="card"><h3>Café / restaurant</h3><p><a href="demos/coffee.html" style="color:var(--gold-soft)">Open the example →</a></p></div>
    <div class="card"><h3>Salon / barber</h3><p><a href="demos/salon.html" style="color:var(--gold-soft)">Open the example →</a></p></div>
    <div class="card"><h3>Retail / nursery</h3><p><a href="demos/plants.html" style="color:var(--gold-soft)">Open the example →</a></p></div>
  </div>
  <p style="margin-top:26px"><a class="btn btn-gold" href="contact.html">Start a project</a></p>
  <p class="near">Also serving {c['near']}. &nbsp;·&nbsp; {" &nbsp;·&nbsp; ".join(f'<a href="web-design-{o["slug"]}.html">{o["city"]}</a>' for o in CITIES if o["slug"] != c["slug"])}</p>
</div></section>
</main>
{FOOTER}
</body></html>"""

CONTACT = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Start a project — Akkad Studio</title>
<meta name="description" content="Tell us about your business and we'll reply by email within one working day. No phone calls required — we work in writing.">
<link rel="canonical" href="https://akkadstudio.com/contact.html">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta name="robots" content="index, follow">
<style>{STYLE}</style></head><body>
{nav()}
<main>
<section class="hero"><div class="wrap">
  <div class="eyebrow">Start a project</div>
  <h1>Tell us about your business.</h1>
  <p class="sub">Fill this in and we'll come back by email within one working day with a straight answer and a price. No calls, no meeting, no pressure — and no follow-up if you'd rather we didn't.</p>
</div></section>

<section><div class="wrap">
  <form name="project" method="POST" action="/thanks.html" data-netlify="true" netlify-honeypot="company-website">
    <input type="hidden" name="form-name" value="project">
    <p style="display:none"><label>Leave this empty: <input name="company-website"></label></p>

    <label for="biz">Business name</label>
    <input id="biz" name="business" required>

    <label for="kind">What kind of business?</label>
    <input id="kind" name="kind" placeholder="Café, salon, auto shop, landscaping…" required>

    <label for="city">Town</label>
    <input id="city" name="city" placeholder="Springdale, Fayetteville, Rogers…">

    <label for="email">Your email</label>
    <input id="email" name="email" type="email" required>

    <label for="phone">Phone (optional — we'll still reply by email)</label>
    <input id="phone" name="phone">

    <label for="current">Do you have a website now?</label>
    <select id="current" name="current">
      <option>No website at all</option>
      <option>Facebook page only</option>
      <option>Yes, but it's old or hard to use</option>
      <option>Yes, and it's fine — I want something else</option>
    </select>

    <label for="notes">Anything you want us to know</label>
    <textarea id="notes" name="notes" placeholder="What you'd want the site to do, or anything you've been stuck on."></textarea>

    <button type="submit">Send it</button>
    <p class="fineprint">We reply by email within one working day. We don't share your details with anyone, we won't add you to a mailing list, and if you say you're not interested we stop — first time, no persuading.</p>
  </form>
</div></section>
</main>
{FOOTER}
</body></html>"""

def main():
    written = []
    for c in CITIES:
        p = ROOT / f"web-design-{c['slug']}.html"
        p.write_text(page(c), encoding="utf-8"); written.append(p.name)
    (ROOT / "contact.html").write_text(CONTACT, encoding="utf-8"); written.append("contact.html")

    # thank-you page Netlify redirects to after a submit
    ty = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Thanks — Akkad Studio</title>
<meta name="robots" content="noindex"><style>{STYLE}</style></head><body>{nav()}
<main><section class="hero"><div class="wrap"><div class="eyebrow">Got it</div>
<h1>Thanks — that came through.</h1>
<p class="sub">We'll reply by email within one working day. Nothing else is needed from you in the meantime.</p>
<p style="margin-top:20px"><a class="btn btn-ghost" href="index.html">Back to the site</a></p>
</div></section></main>{FOOTER}</body></html>"""
    (ROOT / "thanks.html").write_text(ty, encoding="utf-8"); written.append("thanks.html")

    # sitemap
    urls = ["", "contact.html"] + [f"web-design-{c['slug']}.html" for c in CITIES]
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>https://akkadstudio.com/{u}</loc></url>\n" for u in urls)
          + "</urlset>\n")
    (ROOT / "sitemap.xml").write_text(sm, encoding="utf-8"); written.append("sitemap.xml")

    print("wrote:")
    for w in written:
        print(f"  {w}  ({(ROOT/w).stat().st_size} bytes)")

if __name__ == "__main__":
    main()
