#!/usr/bin/env python3
"""Generate the product art as SVG (no stock photography, no external requests).

Three objects share one design language: brushed metal body, soft studio lighting,
animated water surface. Finishes are parameterised so the same geometry renders
Steel / Graphite / Sand.

Run: python3 build_art.py
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent / "assets"

FINISHES = {
    "steel": dict(
        hi="#F7F9FA", mid="#C6CCD2", low="#8A9299", dark="#5B646C",
        edge="#EAEEF1", plinth="#B9C0C7", water1="#DFF3FA", water2="#8FC6DC",
        accent="#7FA9BE",
    ),
    "graphite": dict(
        hi="#7C8288", mid="#4A5056", low="#2A2F34", dark="#171B1F",
        edge="#5E666D", plinth="#3A4046", water1="#D9EEF6", water2="#7FB6CC",
        accent="#5E8A9E",
    ),
    "sand": dict(
        hi="#F3EADC", mid="#DCCFB9", low="#B7A78E", dark="#8A7B64",
        edge="#EFE4D3", plinth="#CDBFA8", water1="#E3F4FA", water2="#9AC9DB",
        accent="#B79A6F",
    ),
}


def fountain(f, pro=False):
    """Low, wide vessel with an upwelling spout — reads as a fountain, not a bin.
    viewBox 0 0 620 760."""
    led = """
  <circle cx="310" cy="686" r="4" fill="#9ED8F0" opacity=".9">
    <animate attributeName="opacity" values=".2;.9;.2" dur="3.6s" repeatCount="indefinite"/>
  </circle>
  <circle cx="310" cy="686" r="11" fill="#9ED8F0" opacity=".16"/>""" if pro else ""

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 760" width="620" height="760" role="img" aria-label="RILL fountain">
<defs>
  <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{f['hi']}"/>
    <stop offset=".10" stop-color="{f['mid']}"/>
    <stop offset=".34" stop-color="{f['low']}"/>
    <stop offset=".58" stop-color="{f['mid']}"/>
    <stop offset=".82" stop-color="{f['low']}"/>
    <stop offset="1" stop-color="{f['dark']}"/>
  </linearGradient>
  <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{f['dark']}" stop-opacity=".5"/>
    <stop offset=".16" stop-color="{f['low']}" stop-opacity="0"/>
    <stop offset=".34" stop-color="{f['hi']}" stop-opacity=".55"/>
    <stop offset=".52" stop-color="{f['hi']}" stop-opacity=".12"/>
    <stop offset=".78" stop-color="{f['low']}" stop-opacity="0"/>
    <stop offset="1" stop-color="{f['dark']}" stop-opacity=".55"/>
  </linearGradient>
  <radialGradient id="water" cx=".5" cy=".38" r=".72">
    <stop offset="0" stop-color="{f['water1']}"/>
    <stop offset=".6" stop-color="{f['water2']}" stop-opacity=".8"/>
    <stop offset="1" stop-color="{f['water2']}" stop-opacity=".3"/>
  </radialGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#BFE6F5" stop-opacity=".42"/>
    <stop offset="1" stop-color="#BFE6F5" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="stream" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity=".9"/>
    <stop offset="1" stop-color="{f['water1']}" stop-opacity=".35"/>
  </linearGradient>
  <filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="20"/></filter>
  <filter id="soft2" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="6"/></filter>
  <clipPath id="bowlClip"><ellipse cx="310" cy="344" rx="188" ry="50"/></clipPath>
</defs>

<ellipse cx="310" cy="706" rx="196" ry="28" fill="#000" opacity=".55" filter="url(#soft)"/>

<!-- body: tapered vessel -->
<path d="M104 356 C104 326 198 300 310 300 C422 300 516 326 516 356
         L498 646 C494 682 414 700 310 700 C206 700 126 682 122 646 Z"
      fill="url(#body)"/>
<path d="M104 356 C104 326 198 300 310 300 C422 300 516 326 516 356
         L498 646 C494 682 414 700 310 700 C206 700 126 682 122 646 Z"
      fill="url(#sheen)"/>

<!-- brushed streaks -->
<g opacity=".13" stroke="{f['hi']}" stroke-width="1">
  <line x1="146" y1="372" x2="150" y2="686"/><line x1="180" y1="356" x2="184" y2="692"/>
  <line x1="222" y1="342" x2="226" y2="696"/><line x1="262" y1="336" x2="266" y2="698"/>
  <line x1="358" y1="336" x2="354" y2="698"/><line x1="398" y1="342" x2="394" y2="696"/>
  <line x1="440" y1="356" x2="436" y2="692"/><line x1="474" y1="372" x2="470" y2="686"/>
</g>

<!-- horizontal seam -->
<path d="M112 612 C160 626 224 632 310 632 C396 632 460 626 508 612"
      stroke="{f['dark']}" stroke-width="2" fill="none" opacity=".35"/>
<path d="M112 610 C160 624 224 630 310 630 C396 630 460 624 508 610"
      stroke="{f['hi']}" stroke-width="1" fill="none" opacity=".28"/>

<!-- level slot -->
<g>
  <rect x="424" y="414" width="15" height="182" rx="7" fill="{f['dark']}" opacity=".45"/>
  <rect x="426" y="416" width="11" height="178" rx="5.5" fill="#0A0D0F" opacity=".8"/>
  <rect x="426" y="514" width="11" height="80" rx="5.5" fill="{f['water2']}" opacity=".8"/>
  <rect x="426" y="514" width="11" height="3" fill="#fff" opacity=".85"/>
</g>

<!-- rim -->
<ellipse cx="310" cy="348" rx="212" ry="56" fill="{f['edge']}"/>
<ellipse cx="310" cy="342" rx="212" ry="56" fill="url(#body)"/>
<ellipse cx="310" cy="340" rx="190" ry="49" fill="{f['dark']}"/>
<ellipse cx="310" cy="343" rx="188" ry="47" fill="url(#water)"/>

<!-- spout dome -->
<ellipse cx="310" cy="340" rx="30" ry="9" fill="#0A0D0F" opacity=".22"/>
<path d="M286 341 C288 322 332 322 334 341 Z" fill="{f['hi']}" opacity=".3"/>
<path d="M291 341 C293 326 327 326 329 341 Z" fill="{f['water1']}" opacity=".6"/>
<ellipse cx="310" cy="312" rx="20" ry="6" fill="#fff" opacity=".55">
  <animate attributeName="ry" values="4;7;4" dur="2.6s" repeatCount="indefinite"/>
</ellipse>

<!-- water film down the dome -->
<path d="M292 338 C292 352 296 362 300 372" stroke="url(#stream)" stroke-width="2.4" fill="none"
      stroke-linecap="round" opacity=".5">
  <animate attributeName="opacity" values=".2;.6;.2" dur="3.4s" repeatCount="indefinite"/>
</path>
<path d="M330 338 C330 352 326 362 322 372" stroke="url(#stream)" stroke-width="2.4" fill="none"
      stroke-linecap="round" opacity=".4">
  <animate attributeName="opacity" values=".5;.15;.5" dur="3.9s" repeatCount="indefinite"/>
</path>

<!-- ripples -->
<g clip-path="url(#bowlClip)" fill="none" stroke="{f['water1']}" stroke-width="1.4">
  <ellipse cx="310" cy="346" rx="26" ry="8" opacity=".5">
    <animate attributeName="rx" values="20;150;20" dur="8s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values=".6;0;.6" dur="8s" repeatCount="indefinite"/>
  </ellipse>
  <ellipse cx="310" cy="346" rx="44" ry="12" opacity=".3">
    <animate attributeName="rx" values="30;175;30" dur="11s" begin="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values=".45;0;.45" dur="11s" begin="2s" repeatCount="indefinite"/>
  </ellipse>
</g>

<!-- specular + edge -->
<path d="M150 372 C150 358 158 350 172 346 L182 660 C166 656 154 646 152 630 Z" fill="#fff" opacity=".2" filter="url(#soft2)"/>
<path d="M104 356 C104 326 198 300 310 300 C422 300 516 326 516 356
         L498 646 C494 682 414 700 310 700 C206 700 126 682 122 646 Z"
      fill="none" stroke="{f['hi']}" stroke-width="1.4" opacity=".45"/>

<!-- base shadow ring -->
<path d="M150 676 C200 690 260 696 310 696 C360 696 420 690 470 676"
      stroke="#000" stroke-width="3" fill="none" opacity=".18" filter="url(#soft2)"/>
{led}
</svg>'''


def bowl(f):
    """Companion bowl, viewBox 0 0 620 760."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 760" width="620" height="760" role="img" aria-label="RILL bowl in {f['mid']} finish">
<defs>
  <linearGradient id="b1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{f['hi']}"/><stop offset=".35" stop-color="{f['mid']}"/>
    <stop offset=".8" stop-color="{f['low']}"/><stop offset="1" stop-color="{f['dark']}"/>
  </linearGradient>
  <linearGradient id="b2" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{f['dark']}" stop-opacity=".5"/>
    <stop offset=".5" stop-color="{f['hi']}" stop-opacity=".45"/>
    <stop offset="1" stop-color="{f['dark']}" stop-opacity=".55"/>
  </linearGradient>
  <radialGradient id="w2" cx=".5" cy=".3" r=".7">
    <stop offset="0" stop-color="#E8F6FB"/><stop offset="1" stop-color="{f['water2']}" stop-opacity=".35"/>
  </radialGradient>
  <filter id="s3" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="16"/></filter>
</defs>
<ellipse cx="310" cy="560" rx="180" ry="30" fill="#000" opacity=".5" filter="url(#s3)"/>
<path d="M126 300 C126 268 200 250 310 250 C420 250 494 268 494 300 L470 520 C466 552 396 566 310 566 C224 566 154 552 150 520 Z" fill="url(#b1)"/>
<path d="M126 300 C126 268 200 250 310 250 C420 250 494 268 494 300 L470 520 C466 552 396 566 310 566 C224 566 154 552 150 520 Z" fill="url(#b2)"/>
<ellipse cx="310" cy="298" rx="184" ry="52" fill="{f['edge']}" opacity=".9"/>
<ellipse cx="310" cy="302" rx="168" ry="43" fill="{f['dark']}"/>
<ellipse cx="310" cy="302" rx="168" ry="43" fill="url(#w2)"/>
<ellipse cx="310" cy="306" rx="60" ry="14" fill="none" stroke="#fff" stroke-width="1.4" opacity=".35">
  <animate attributeName="rx" values="40;130;40" dur="8s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values=".4;0;.4" dur="8s" repeatCount="indefinite"/>
</ellipse>
<path d="M150 306 C158 470 200 540 246 552" stroke="#fff" stroke-width="2" fill="none" opacity=".18"/>
</svg>'''


def filter_pack(f):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 760" width="620" height="760" role="img" aria-label="RILL filter cartridge">
<defs>
  <linearGradient id="c1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{f['hi']}"/><stop offset=".5" stop-color="{f['mid']}"/>
    <stop offset="1" stop-color="{f['low']}"/>
  </linearGradient>
  <linearGradient id="c2" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{f['dark']}" stop-opacity=".45"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".35"/>
    <stop offset="1" stop-color="{f['dark']}" stop-opacity=".45"/>
  </linearGradient>
  <filter id="s4" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14"/></filter>
</defs>
<ellipse cx="310" cy="620" rx="120" ry="20" fill="#000" opacity=".5" filter="url(#s4)"/>
<rect x="212" y="220" width="196" height="360" rx="26" fill="url(#c1)"/>
<rect x="212" y="220" width="196" height="360" rx="26" fill="url(#c2)"/>
<rect x="212" y="252" width="196" height="12" fill="{f['dark']}" opacity=".35"/>
<rect x="212" y="536" width="196" height="12" fill="{f['dark']}" opacity=".35"/>
<g fill="{f['dark']}" opacity=".28">
  <circle cx="262" cy="320" r="3"/><circle cx="310" cy="320" r="3"/><circle cx="358" cy="320" r="3"/>
  <circle cx="262" cy="360" r="3"/><circle cx="310" cy="360" r="3"/><circle cx="358" cy="360" r="3"/>
  <circle cx="262" cy="400" r="3"/><circle cx="310" cy="400" r="3"/><circle cx="358" cy="400" r="3"/>
  <circle cx="262" cy="440" r="3"/><circle cx="310" cy="440" r="3"/><circle cx="358" cy="440" r="3"/>
</g>
</svg>'''


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "fountain-steel.svg").write_text(fountain(FINISHES["steel"]), encoding="utf-8")
    (OUT / "fountain-graphite.svg").write_text(fountain(FINISHES["graphite"]), encoding="utf-8")
    (OUT / "fountain-sand.svg").write_text(fountain(FINISHES["sand"]), encoding="utf-8")
    (OUT / "fountain-pro.svg").write_text(fountain(FINISHES["graphite"], pro=True), encoding="utf-8")
    (OUT / "bowl-sand.svg").write_text(bowl(FINISHES["sand"]), encoding="utf-8")
    (OUT / "filter.svg").write_text(filter_pack(FINISHES["steel"]), encoding="utf-8")
    print("wrote 4 svg assets")


if __name__ == "__main__":
    main()
