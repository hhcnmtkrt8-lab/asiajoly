#!/usr/bin/env python3
"""Check that this repo can be cloned straight into a web root (Hostinger / cPanel / Pages).

Run from the repository root:  python3 tools/preflight.py
Exit code 0 = deployable, 1 = something needs fixing.
"""
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
fails, warns = [], []


def check(cond, msg, hard=True):
    if cond:
        print(f"  ok    {msg}")
    else:
        (fails if hard else warns).append(msg)
        print(f"  {'FAIL' if hard else 'warn'}  {msg}")


print("Entry point")
check((ROOT / "index.html").exists(), "index.html exists at repository root")
check((ROOT / ".htaccess").exists(), ".htaccess present (index.html before index.php)", hard=False)
check((ROOT / "404.html").exists(), "404.html exists", hard=False)

print("\nPortability")
html = sorted(ROOT.glob("*.html"))
check(len(html) >= 20, f"{len(html)} HTML pages generated")
abs_hits = []
for p in html:
    t = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r'(?:src|href)="(/[^/][^"]*)"', t):
        abs_hits.append(f"{p.name}: {m.group(1)}")
check(not abs_hits, "no root-absolute asset paths (subfolder-safe)", hard=False)
if abs_hits:
    print("        " + "; ".join(abs_hits[:5]))

print("\nBuild-free")
for pointless in ("package.json", "composer.json"):
    check(not (ROOT / pointless).exists(), f"no {pointless} (so no build step can be required)", hard=False)
check((ROOT / "assets" / "styles.css").exists(), "assets/styles.css present")
check((ROOT / "assets" / "app.js").exists(), "assets/app.js present")

print("\nRepo hygiene")
check(not (ROOT / ".gitmodules").exists(), "no git submodules")
big = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts and p.stat().st_size > 2_000_000]
check(not big, "no files over 2 MB", hard=False)
count = sum(1 for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts)
print(f"  info  {count} files tracked in the working tree")

print("\nServer-side leftovers (only relevant once deployed to Hostinger)")
print("  info  delete public_html/index.php and any coming-soon.* after the first deploy,")
print("        otherwise Apache will serve PHP before index.html")

print()
for w in warns:
    print("warn:", w)
for f in fails:
    print("FAIL:", f)
print("deployable" if not fails else "not deployable")
sys.exit(1 if fails else 0)
