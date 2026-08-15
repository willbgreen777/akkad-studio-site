// Builds Desktop/SEND-THESE.md — one paste-ready message per prospect,
// each containing a link that builds THAT business a website on open.
// Re-run after editing prospects.csv:  node akkad-studio-site/make-send-file.js
const fs = require('fs');
const path = require('path');
const DESK = path.join(require('os').homedir(), 'Desktop');

const TRADE = {
  1:'engine', 2:'auto', 3:'pet', 4:'auto', 5:'pet', 6:'pet', 7:'barber', 8:'barber',
  9:'barber', 10:'shop', 11:'fence', 12:'weld', 13:'weld', 14:'weld', 15:'tire',
  16:'clean', 17:'tattoo', 18:'barber', 19:'cafe', 20:'salon', 21:'barber', 22:'barber',
  23:'barber', 24:'auto', 25:'weld', 26:'nails', 27:'barber', 28:'barber', 29:'barber',
  30:'pet', 31:'pet', 32:'tattoo', 33:'auto', 34:'uphol', 35:'uphol', 36:'shop',
  37:'tire', 38:'auto', 39:'lawn', 40:'uphol'
};

// minimal CSV parser (handles quoted fields)
function parseCSV(text){
  const rows=[]; let row=[], cur='', q=false;
  for(let i=0;i<text.length;i++){
    const c=text[i];
    if(q){ if(c==='"'){ if(text[i+1]==='"'){cur+='"';i++;} else q=false; } else cur+=c; }
    else if(c==='"') q=true;
    else if(c===','){ row.push(cur); cur=''; }
    else if(c==='\n'){ row.push(cur); rows.push(row); row=[]; cur=''; }
    else if(c!=='\r') cur+=c;
  }
  if(cur.length||row.length){ row.push(cur); rows.push(row); }
  return rows.filter(r=>r.length>1);
}

const raw  = fs.readFileSync(path.join(DESK,'prospects.csv'),'utf8');
const rows = parseCSV(raw);
const head = rows.shift();
const col  = n => head.indexOf(n);

// %27 the apostrophes too — some chat clients cut a link short at a bare '
const link = (name, trade) =>
  'https://akkadstudio.com/?b=' + encodeURIComponent(name).replace(/'/g,'%27') + '&t=' + trade;

// The opening line has to be TRUE for that specific business, or they stop reading.
function opener(name, presence){
  const p = (presence || '').toLowerCase();
  if (p.includes('wordpress') || p.includes('microsite') || p.includes('setmore') || p.includes('booksy'))
    return `We came across ${name} and had a look at what you've got online right now. It works, but it isn't really yours — it's on somebody else's address, you can't change much, and it doesn't look like the business you actually run.`;
  if (p.includes('instagram') && !p.includes('facebook'))
    return `We noticed ${name} runs on Instagram without a website. That's fine until somebody searches Google instead — then you're invisible to them.`;
  if (p.includes('facebook'))
    return `We noticed ${name} runs on Facebook without a website. That works right up until somebody searches Google instead of Facebook — then you're invisible to them.`;
  return `We noticed ${name} doesn't have a website anywhere we could find. Everyone who looks you up on a phone is deciding based on nothing.`;
}

const msgFB = (name, link, presence) =>
`Hi — this is Akkad Studio, a small web design shop here in Northwest Arkansas.

${opener(name, presence)}

Easier to show you than explain it. Open this and it'll build ${name} a website on screen in about four seconds:

${link}

If you like where that's going, say the word and we'll build the real one — your services, your hours, your photos — and send it to you to look at. Sites are $500, and you don't pay a cent until you've seen it finished and told us you want it. If you don't, you owe nothing and we'll leave you alone.`;

const msgTXT = (name, link) =>
`Hi — Akkad Studio here, a web design shop in Northwest Arkansas. Open this and it builds ${name} a website on screen so you can see it: ${link} — say the word and we'll build the real one and send it over. $500, and nothing to pay until you've seen it and said yes.`;

let out = `# SEND THESE

*Generated ${new Date().toISOString().slice(0,10)} by \`akkad-studio-site/make-send-file.js\`.*
*Every link below builds that exact business a website the second they open it.*

---

## How to use this file

1. Scroll to a business.
2. Copy the message.
3. Paste it into their Facebook page's **Message** box. Send.
4. Put an **x** in the Contacted column of \`prospects.csv\`.

**Five is a full week.** Not five a day — five, total. A week with five sends and five nos
is a successful week. The only failed week is zero.

You don't have to write anything. You don't have to answer anything on the spot.
Anything they ask, you send to me and I write the reply.

---

## Check one link first

Before you send anything, open this in your own browser so you know what they'll see:

https://akkadstudio.com/?b=Lowell%20Small%20Engine&t=engine

That is exactly what lands on their screen. If that doesn't feel worth sending, tell me and
I'll change it before you send a single message.

---
`;

const groupA = [], groupB = [];
for (const r of rows){
  const pri   = parseInt(r[col('Priority')],10);
  const name  = r[col('Business')].trim();
  const city  = r[col('City')].trim();
  const cat   = r[col('Category')].trim();
  const phone = (r[col('Phone')]||'').trim();
  const chan  = (r[col('Best channel')]||'').trim();
  const notes = (r[col('Notes')]||'').trim();
  const email = (r[col('Email')]||'').trim();
  const trade = TRADE[pri] || 'shop';
  const url   = link(name, trade);
  const pres  = (r[col('Their web presence')]||'').trim();
  const rec   = { pri, name, city, cat, phone, chan, notes, email, url, pres };
  (chan.toLowerCase().includes('facebook') || chan.toLowerCase().includes('instagram'))
    ? groupA.push(rec) : groupB.push(rec);
}

function block(r, kind){
  let s = `\n### ${r.pri}. ${r.name}\n`;
  s += `*${r.cat} · ${r.city}${r.phone ? ' · ' + r.phone : ''}*\n`;
  if (r.notes) s += `\n> ${r.notes}\n`;
  if (r.email) s += `\nEmail on file: \`${r.email}\`\n`;
  s += `\n**Their link:** ${r.url}\n`;
  s += `\n\`\`\`\n${kind === 'fb' ? msgFB(r.name, r.url, r.pres) : msgTXT(r.name, r.url)}\n\`\`\`\n`;
  return s;
}

out += `\n## GROUP A — message these on Facebook or Instagram (${groupA.length})\n\n`;
out += `These have a page with a **Message** button. You are typing into a box that exists to be\ntyped into. Work these first. Start at number 1.\n`;
groupA.forEach(r => { out += block(r, 'fb'); });

out += `\n---\n\n## GROUP B — no online presence at all (${groupB.length})\n\n`;
out += `**You do not have to do these.** They are here because they are real businesses, not because\nthey are your job. Every one needs a phone call or a walk-in, and you have said you will not do\nthat — so skip them. They are written out only so that if one ever falls in your lap, the words\nalready exist.\n\nIf you ever do send one, it is a text, typed by you, one at a time. Never a batch, never automated.\n`;
groupB.forEach(r => { out += block(r, 'txt'); });

out += `
---

## When one replies

Send me exactly what they said. I write the answer.

**If they say yes** — and "yes" here just means *go ahead and build it*, not *here's money* —
send me their name, their trade, and anything they gave you: hours, phone, services, photos.
I build the real site. Two or three days. You send them the link.

**Then they look at it, and only then does money come up.**

> Glad you like it. It's $500 and it goes live on your domain today. Zelle, Venmo or Cash App,
> whichever is easiest — send it over and I'll flip it on this afternoon.

**The site goes live when the money lands, not before.** That's your protection, and it's the
normal way this works — nobody is offended by it.

**If they don't like it:** "No problem at all — nothing owed, and we won't chase you. If you
ever change your mind it's still here." Then stop. That is the whole promise we made and we keep
it, because the promise is the only reason a stranger said yes in the first place.

### Why we're building before we get paid
Building costs you almost nothing — I do it. It costs a normal agency a week of salary, which is
why nobody else offers this. It removes the one thing that kills every cold message: *why would
I send money to someone I've never met?* You're not being generous. You're spending the one
resource you have a surplus of.
`;

fs.writeFileSync(path.join(DESK,'SEND-THESE.md'), out);
console.log('SEND-THESE.md written —', groupA.length, 'group A,', groupB.length, 'group B');

// also keep a "Their build link" column in prospects.csv — idempotent, never duplicates
const LINKCOL = 'Their build link';
const li = head.indexOf(LINKCOL);
const newHead = li === -1 ? head.concat([LINKCOL]) : head.slice();
const outRows = [newHead];
for (const r of rows){
  const pri = parseInt(r[col('Priority')],10);
  const url = link(r[col('Business')].trim(), TRADE[pri] || 'shop');
  const row = r.slice();
  while (row.length < newHead.length) row.push('');
  row[li === -1 ? newHead.length - 1 : li] = url;
  outRows.push(row);
}
const csv = outRows.map(r => r.map(f =>
  /[",\n]/.test(f) ? '"' + f.replace(/"/g,'""') + '"' : f).join(',')).join('\n') + '\n';
fs.writeFileSync(path.join(DESK,'prospects.csv'), csv);
console.log('prospects.csv updated with a Their build link column');
