#!/usr/bin/env python3
"""Build the deployable static site in ./site from the page source in ./web.

The page in web/index.html is written as a body fragment (the Claude artifact
format). This wraps it in a full HTML document and copies only the assets the
page actually references, so drafts and raw exports never ship.
"""
import re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "web", ROOT / "site"

body = (SRC / "index.html").read_text(encoding="utf-8")
body = re.sub(r'^<meta charset="utf-8">\s*', "", body)
m = re.search(r"<title>.*?</title>", body, re.S)
title = m.group(0) if m else "<title>Pukaar.ai Case Study</title>"
body = body.replace(title, "", 1)

head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title}
<meta name="theme-color" content="#F5F6FA">
<meta property="og:title" content="Pukaar.ai Case Study">
<meta property="og:description" content="How Pukaar.ai was designed: a doctor-led co-parent for a baby's first 1,000 days.">
<meta property="og:image" content="img/cover-hand.webp">
<link rel="icon" href="icons/logo-mark.svg" type="image/svg+xml">
<style>
:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
body{{margin:0}}
[hidden]{{display:none!important}}
</style>
</head>
<body>
"""
html = head + body.strip() + "\n</body>\n</html>\n"

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
(OUT / "index.html").write_text(html, encoding="utf-8")

refs = set(re.findall(r"(?:img|icons|fonts)/[\w.@-]+\.(?:webp|svg|woff2|png|jpg)", html))
refs |= {f"img/m-{i}.webp" for i in range(1, 9)}  # built in script
missing = []
for r in sorted(refs):
    src = SRC / r
    if not src.exists():
        missing.append(r); continue
    (OUT / r).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, OUT / r)
print(f"site/ built: {len(refs) - len(missing)} assets" + (f", missing: {missing}" if missing else ""))
