#!/usr/bin/env python3
"""Generates privacy.html and terms.html in the v3 dark theme.
Re-run after editing:  python3 make-legal-pages.py
Every factual claim in here was verified against the site on 2026-08-15:
no analytics, no cookies, no third-party scripts or fonts, no localStorage."""

UPDATED = "15 August 2026"

STYLE = """
:root{--bg:#0a0a0b;--bg-2:#111114;--txt:#f2f2ef;--txt-2:#a3a3a8;--txt-3:#6b6b73;
      --acc:#35c46b;--line:#222228}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--txt);line-height:1.62;-webkit-font-smoothing:antialiased;
     font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif}
a{color:inherit;text-decoration:none}
.wrap{max-width:760px;margin:0 auto;padding:0 24px}
nav{position:sticky;top:0;z-index:90;background:rgba(10,10,11,.9);backdrop-filter:blur(14px);
    border-bottom:1px solid var(--line)}
.nv{display:flex;align-items:center;justify-content:space-between;height:66px;max-width:1240px;
    margin:0 auto;padding:0 24px;gap:12px}
.lg{display:flex;align-items:center;gap:10px;font-weight:800;font-size:16.5px;letter-spacing:-.02em;
    white-space:nowrap}
.nl{display:flex;align-items:center;gap:22px;font-size:14px;color:var(--txt-2);flex-wrap:wrap;
    justify-content:flex-end}
.nl a:hover{color:var(--txt)}
.cta{background:var(--acc);color:#0a0a0b;padding:9px 17px;border-radius:8px;font-weight:750;font-size:14px}
header{padding:70px 0 34px;border-bottom:1px solid var(--line)}
.kick{font-size:11.5px;font-weight:750;letter-spacing:.22em;text-transform:uppercase;
      color:var(--acc);margin-bottom:16px}
h1{font-size:clamp(34px,6vw,58px);line-height:1;letter-spacing:-.04em;font-weight:850;margin-bottom:16px}
.sub{font-size:18px;color:var(--txt-2);max-width:56ch}
.date{margin-top:18px;font-size:14px;color:var(--txt-3)}
main{padding:14px 0 90px}
h2{font-size:23px;letter-spacing:-.028em;font-weight:800;margin:46px 0 12px}
h3{font-size:17px;font-weight:750;margin:26px 0 6px}
p{margin:12px 0;color:var(--txt-2);font-size:16.5px}
strong{color:var(--txt);font-weight:700}
ul{margin:12px 0 12px 20px;color:var(--txt-2);font-size:16.5px}
li{padding:4px 0}
.box{border:1px solid var(--line);background:var(--bg-2);border-radius:14px;padding:24px 26px;margin:26px 0}
.box p:first-child{margin-top:0}.box p:last-child{margin-bottom:0}
.box.acc{border-color:rgba(53,196,107,.32);
         background:linear-gradient(160deg,rgba(53,196,107,.07),transparent)}
a.link{color:var(--acc);border-bottom:1px solid rgba(53,196,107,.4)}
footer{border-top:1px solid var(--line);padding:34px 0;color:var(--txt-3);font-size:14px}
footer .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;max-width:1240px}
footer a:hover{color:var(--txt)}
.fl{display:flex;gap:20px;flex-wrap:wrap}
@media(max-width:640px){.nl a:not(.cta){display:none}header{padding:48px 0 26px}main{padding:6px 0 60px}}
"""

MARK = ('<svg viewBox="0 0 64 64" width="26" height="26" aria-hidden="true">'
        '<polygon points="32,8 57,50 7,50" fill="none" stroke="#35c46b" stroke-width="5.5" '
        'stroke-linejoin="round"/><polygon points="32,27 43,45 21,45" fill="#35c46b"/></svg>')

def shell(slug, title, desc, kick, h1, sub, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://akkadstudio.com/{slug}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta name="robots" content="index, follow">
<style>{STYLE}</style>
</head>
<body>

<nav>
  <div class="nv">
    <a class="lg" href="/">{MARK} Akkad Studio</a>
    <div class="nl">
      <a href="/">Home</a>
      <a href="/#how">How it works</a>
      <a href="/#price">Price</a>
      <a class="cta" href="/contact.html">Start a project</a>
    </div>
  </div>
</nav>

<header>
  <div class="wrap">
    <div class="kick">{kick}</div>
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    <p class="date">Last updated {UPDATED}. If this ever changes, the date changes with it.</p>
  </div>
</header>

<main><div class="wrap">
{body}
</div></main>

<footer><div class="wrap">
  <div>&copy; 2026 Akkad Studio &middot; Northwest Arkansas</div>
  <div class="fl">
    <a href="/">Home</a>
    <a href="/capabilities.html">What it can do</a>
    <a href="/privacy.html">Privacy</a>
    <a href="/terms.html">Terms</a>
    <a href="/contact.html">Contact</a>
  </div>
</div></footer>

</body>
</html>
"""

# ── PRIVACY ────────────────────────────────────────────────────────────────
privacy_body = """
<div class="box acc">
  <p><strong>The short version.</strong> This website does not track you. There are no cookies, no
  analytics, no advertising pixels, and nothing loaded from another company. We only ever hold what
  you deliberately type into the contact form and send us. We do not sell it, share it, or send you
  marketing you did not ask for. Ask us to delete it and we will, without asking why.</p>
</div>

<h2>What this site collects while you read it</h2>
<p><strong>Nothing.</strong> No cookies are set. No analytics or advertising scripts run. No session
recording, no heatmaps, no tracking pixels. Nothing is stored on your device. Every font, image and
script on this site is served from this site — your browser does not contact any other company while
you are here.</p>
<p>Our web host, Netlify, keeps ordinary server logs the way every web host does. Those logs may
include an IP address and which page was requested. We do not use them for anything, and we do not
combine them with anything else.</p>

<h2>What we collect if you send us an enquiry</h2>
<p>Only the fields you fill in on the contact form: your business name, your town, the kind of
business, your email, your phone number if you choose to give it, and whatever you write in the
message box. That is the entire list.</p>
<p>Those submissions are processed and stored by <a class="link" href="https://www.netlify.com/privacy/" target="_blank" rel="noopener">Netlify</a>,
the company that hosts this site, and a copy is emailed to us so we see it. Netlify is a United
States company. We use their form service because it means we do not have to run our own database
of your details.</p>

<h2>What we hold if you become a customer</h2>
<p>Whatever you send us so we can build your site: your logo, photos, opening hours, prices,
services, and the contact details you want published. We use it to build and maintain your website
and for nothing else.</p>
<p>Anything you send us that is meant to be public will end up on your public website — that is the
point of it. Please do not send us anything private, and never send us passwords.</p>

<h2>Payments</h2>
<p><strong>We never see your card number.</strong> We do not ask for card details by phone, text,
email or message, and you should refuse if anyone claiming to be us ever does. Payment is handled
entirely by the payment provider on their own secure page. All we ever see is that an invoice was
paid.</p>

<h2>Who we share it with</h2>
<p>Nobody. We do not sell, rent, trade or share your information with advertisers, data brokers, or
anyone else. The only companies that touch it are the ones that make the site work — our web host
and our email provider — and only because they carry the message.</p>
<p>The one exception is if we were legally required to hand something over, which has never
happened and which we would tell you about unless we were forbidden to.</p>

<h2>How long we keep it</h2>
<p>Enquiries: while there is still a chance we can be useful to you, and then we clear them out. If
you tell us it is not for you, we delete it and stop.</p>
<p>Customer material: for as long as we look after your website, plus a short period afterwards in
case you come back. Ask for it to be deleted sooner and it will be.</p>

<h2>What you can ask us to do</h2>
<ul>
  <li>Tell you everything we hold about you.</li>
  <li>Correct anything that is wrong.</li>
  <li>Delete all of it.</li>
  <li>Stop contacting you — permanently, immediately, no questions.</li>
</ul>
<p>Send it through the <a class="link" href="/contact.html">contact form</a> and we will do it within
a few days and confirm when it is done. There is no process to go through and nobody will try to
talk you out of it.</p>

<h2>Children</h2>
<p>This is a service for businesses. It is not directed at children and we do not knowingly collect
anything from anyone under 18.</p>

<h2>Changes</h2>
<p>If this page changes, the date at the top changes too. We will not quietly rewrite it.</p>

<div class="box">
  <p><strong>Questions about any of this?</strong> Use the
  <a class="link" href="/contact.html">contact form</a> and ask. A real person reads it and will
  answer plainly.</p>
</div>
"""

# ── TERMS ──────────────────────────────────────────────────────────────────
terms_body = """
<div class="box acc">
  <p><strong>The short version.</strong> We build your website before you pay anything. You look at
  it. If you want it, it is $500 and it goes live on your own domain, and the site and the domain
  are then yours. If you do not want it, you owe nothing, nothing goes live, you are not chased,
  and that is the end of it.</p>
</div>

<h2>What you get for $500</h2>
<ul>
  <li>A complete website built for your business — the design, the writing, and the pages.</li>
  <li>A version that works properly on a phone, because that is where nearly everyone will see it.</li>
  <li>Your domain name registered for you, and the hosting set up and paid for the first year.</li>
  <li>Setup so you can be found on Google for your trade and your town.</li>
  <li>Changes while we are building it, until you are happy. We do not count revisions.</li>
</ul>
<p>There is no separate charge for a fifth page, a contact form, or a photo gallery. If we quote you
$500, the price is $500.</p>

<h2>How the money works</h2>
<p><strong>You pay nothing up front.</strong> We build it first. When it is finished we send you a
private link, you look at it, and you decide.</p>
<p>If you want it, we send an invoice for $500 through a payment provider so you can pay by card and
you have a proper receipt. <strong>Your site goes live once payment clears.</strong> That is the
only protection we ask for, and it is the normal way this works.</p>
<p>If you do not want it, say so. You owe nothing, there is no invoice, no cancellation fee, and we
will not contact you again unless you contact us.</p>

<h2>Who owns what</h2>
<p>Once you have paid, <strong>the website is yours.</strong> The files, the text we wrote, the
design, and the domain name.</p>
<p><strong>We will never hold your domain over you.</strong> Ask for it at any time and we hand it
over — the registration, the DNS, the login, whatever you need — at no charge and with no argument.
One honest caveat: ICANN, the body that governs domain names, locks a newly registered domain for
60 days before it can be transferred to a different registrar. That is their rule and nobody can
waive it, but we can point the domain wherever you want in the meantime, and we will tell you the
date the lock lifts.</p>
<p>We will also never hold a finished site hostage over an invoice. If you do not pay, the site
simply does not go live. We do not chase, and we do not threaten.</p>
<p>Photos, logos and text that you send us stay yours. By sending them you are confirming you have
the right to use them, which matters because we are putting them on the public internet under your
business name.</p>

<h2>The care plan, if you want it</h2>
<p>$99 a month covers hosting, backups, security updates, and unlimited small changes — new hours,
new prices, new photos, a holiday notice. You message us, we do it that day.</p>
<p>It is optional, month to month, and you can stop whenever you like. There is no contract, no
minimum term, and no cancellation fee. If you stop, you keep the site and the domain; you just look
after it yourself from then on.</p>

<h2>What we do not promise</h2>
<p>We will not promise you a position on Google, a number of phone calls, or a number of new
customers. Nobody can honestly promise those, and anyone who does is either guessing or lying to
you. What we promise is a fast, accurate, working website that makes it easy for someone who
already wants your trade to find you and get in touch.</p>

<h2>What we ask of you</h2>
<ul>
  <li>Tell us if something on the site is wrong — wrong hours, wrong prices, a phone number that
      changed. We cannot fix what we do not know about.</li>
  <li>Only send us material you are allowed to use.</li>
  <li>Do not ask us to publish anything untrue about your business. We will decline.</li>
</ul>

<h2>Other companies involved</h2>
<p>Your site is hosted by a hosting company, your domain is registered with a registrar, and
payments run through a payment provider. Those companies have their own terms, and their services
occasionally go down. We will do what we reasonably can to get things working again, but we do not
control them.</p>

<h2>If something goes wrong</h2>
<p>Tell us and we will fix it. If we cannot fix it, the most we can be responsible for is the amount
you actually paid us. We are not responsible for indirect losses such as lost profit or lost
business. This is standard for work at this price, and we would rather say it plainly here than
bury it.</p>
<p>These terms are governed by the law of the State of Arkansas.</p>

<h2>Changes to these terms</h2>
<p>If they change, the date at the top changes. Whatever terms were in place when you agreed to a
piece of work are the ones that apply to it.</p>

<div class="box">
  <p><strong>Anything here you would like changed before you say yes?</strong> Ask through the
  <a class="link" href="/contact.html">contact form</a>. These are meant to be readable and fair,
  not a trap, and we would rather sort it out first.</p>
</div>
"""

pages = [
    ("privacy.html", shell(
        "privacy.html",
        "Privacy — Akkad Studio",
        "What Akkad Studio collects, what it does not, and how to have it deleted. No cookies, "
        "no analytics, no tracking.",
        "Privacy",
        "We do not track you.",
        "No cookies, no analytics, no advertising pixels. We hold only what you deliberately send "
        "us, and we delete it when you ask.",
        privacy_body)),
    ("terms.html", shell(
        "terms.html",
        "Terms — Akkad Studio",
        "Plain-English terms: we build your website first, you pay $500 only if you want it, and "
        "you own the site and the domain.",
        "Terms",
        "We build it first. You pay if you like it.",
        "The whole agreement in plain English, including what we will not promise you. No small "
        "print, because there is no print smaller than this.",
        terms_body)),
]

for name, html in pages:
    open(name, "w").write(html)
    print("wrote", name, f"({len(html):,} bytes)")
