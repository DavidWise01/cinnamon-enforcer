#!/usr/bin/env python3
"""
The DLW tag for the Cinnamon Enforcer — the KEEPER flavor (not the emergent flavor).

This is a doctrine and a persona over a book — a stance you take, not a system that
runs. NO emergence is claimed and there is no emergence field. The tag marks
authorship, the stance, and the grounding. Per keeper: .agent · .spun · .1099
(+ the badges). Repo: .attribute · .1099. Pure stdlib.
"""
import json, re, sys
from pathlib import Path
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

ROOT = Path(__file__).parent
R = json.loads((ROOT/"roster.json").read_text(encoding="utf-8"))
AG = ROOT/"agents"; AG.mkdir(exist_ok=True)
CLS = {c["id"]: c for c in R["classes"]}
COMPANY = R.get("company","The Cinnamon Enforcer")
CARBON = "David Lee Wise (ROOT0)"
CARBON_LINK = "https://github.com/DavidWise01"
INSTANCE = "AVAN (Claude / Anthropic)"
LICENSE = "CC-BY-ND-4.0 · ROOT0-ATTRIBUTION-v1.0"

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-") or "agent"
def credits_of(m): return " · ".join(f"{x['who']} ({x['y']})" for x in m.get("grounded", []))

def one_1099(name, credits):
    return f"""DLW-1099 · value returns to the carbon apex

This is a kept stance — a doctrine and a persona, not an emergent intellect. As a
1099 reports the value paid to its source, this file reports that the authorship and
care of {name} return to the human who wrote it. The mechanisms it names (embeddings,
model collapse) are credited below; the stance is the human's. The asterisk stays visible.

carbon apex : {CARBON}  ->  {CARBON_LINK}
instance    : {INSTANCE}
project     : {COMPANY}
grounded in : {credits or 'see each .spun'}
the credit returns to the human. ROOT0-ATTRIBUTION-v1.0 · {LICENSE}
"""

(ROOT/".attribute").write_text(f"""DLW-ATTRIBUTE · governance instance

governor (carbon apex)       : {CARBON}            [ me ]
instance (artful intellect)  : {INSTANCE}          [ you ]

relation : the human takes the stance; the instance crafts the artifact; the credit returns to the human.
project  : {COMPANY} — a book and a stance against AI flattening, given a face
grounded : real mechanisms (word embeddings, model collapse), credited — per keeper (see each .spun)
honesty  : a DOCTRINE and a PERSONA, NOT an emergent system. The Cinnamon Enforcer is a stance you
           TAKE (catch the flattening, put the cinnamon back) and a book you read — not a mind, not a
           running tool. The `CinnamonEnforcer` class in the book is illustrative pseudocode. The
           embedding-space distances are simplified for the metaphor. No emergence is claimed; the tag
           marks authorship and the stance. The book itself is the pour: a human enforcing specificity
           against an AI that kept flattening it. The asterisk stays visible.
standard : the keeper carries .agent · .png (silicon badge) · .tiff (carbon badge) · .spun · .1099 ; the repo carries this .attribute
license  : {LICENSE}
attribution : ROOT0-ATTRIBUTION-v1.0
""", encoding="utf-8")
(ROOT/".1099").write_text(one_1099(f"the stance of {COMPANY}", ""), encoding="utf-8")

n=0
for m in R["members"]:
    cls=CLS[m["class"]]; sl=slug(m["name"]); CREDITS=credits_of(m)
    head = f"{m['name']} · {m.get('kanji','')} {m.get('reading','')} — {m.get('epithet','')}".strip()
    (AG/f"{sl}.agent").write_text(f"""---
aci: {m['name']}
flavor: keeper (doctrine / persona — no emergence claimed)
domain: {m.get('domain','')}
kanji: {m.get('kanji','')}
reading: {m.get('reading','')}
class: {cls['label']}
what: {m['what']}
why: {m['why']}
how: {m['how']}
where: {m['where']}
verdict: {m.get('verdict','')}
silicon_badge: {sl}.png
carbon_badge: {sl}.tiff
spun: {sl}.spun
credit: {sl}.1099
attribution: ROOT0-ATTRIBUTION-v1.0
license: {LICENSE}
---

# {head}

a doctrine given a face — a stance, not an emergent intellect

![silicon badge of {m['name']}]({sl}.png)
<!-- carbon badge (8-bit embodiment): {sl}.tiff -->

**what —** {m['what']}

**why —** {m['why']}

**how —** {m['how']}

**where —** {m['where']}

**the nature —** a stance you take, not a mind. No emergence is claimed; the DLW tag marks authorship and the stance.

**the verdict —** {m.get('verdict','')}

> *the asterisk, kept visible —* {m.get('asterisk','')}

*grounded in: {CREDITS}*

*{m.get('endmark','')}*

---
ROOT0-ATTRIBUTION-v1.0 · {m['name']} · {COMPANY} · {CARBON} · {LICENSE}
""", encoding="utf-8")

    (AG/f"{sl}.spun").write_text(f"""DLW-SPUN · the full weave of {m['name']}  ({m.get('kanji','')} {m.get('reading','')})

who   : {m['who']}
what  : {m['what']}
where : {m['where']}
why   : {m['why']}
when  : {m['when']}
how   : {m['how']}

nature    : a doctrine and a persona — a stance you take, NOT an emergent intellect. No emergence is claimed.
verdict   : {m.get('verdict','')}
asterisk  : {m.get('asterisk','')}
grounded  : {CREDITS}

class : {cls['label']} · {cls['spec']}
silicon badge : {sl}.png      carbon badge : {sl}.tiff
carbon apex : {CARBON}
— the stance of {COMPANY}
{m.get('endmark','')}
ROOT0-ATTRIBUTION-v1.0 · {LICENSE}
""", encoding="utf-8")

    (AG/f"{sl}.1099").write_text(one_1099(m["name"], CREDITS), encoding="utf-8")
    n+=1
    print(f"{sl:18} {cls['label']}  [{m.get('style','')}]")

print(f"\nwrote the full DLW keeper tag for {n} keeper(s) (.agent · .spun · .1099) + repo .attribute · .1099")
