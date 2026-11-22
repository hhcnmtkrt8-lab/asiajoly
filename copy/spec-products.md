Write the catalogue copy for 13 products.

Return ONE JSON object: {"en":[ ...13 product objects... ], "zh":[ ...same 13, same order, same ids... ]}

Each product object:
{
  "id": "spring-01",
  "name": "Spring 01",
  "line": "Spring",
  "category": "Fountains",
  "price": 129,
  "compareAt": 0,
  "tagline": "max 10 words",
  "desc": "35-55 words",
  "bullets": ["3-6 words","3-6 words","3-6 words"],
  "specs": [{"k":"Capacity","v":"2.8 L"}, ... exactly 6 rows ...],
  "colors": [{"name":"Steel","hex":"#C7CBD0"},{"name":"Graphite","hex":"#2E3134"},{"name":"Sand","hex":"#D8CBB8"}],
  "badge": "" | "Best seller" | "New" | "Pro"
}

The exact 13 products, in this order, with these ids, names, categories and prices:
1  spring-01        Spring 01        Fountains  129   colors: Steel #C7CBD0, Graphite #2E3134, Sand #D8CBB8   badge: Best seller
2  spring-01-pro    Spring 01 Pro    Fountains  169   colors: Graphite #2E3134, Steel #C7CBD0                badge: Pro
3  spring-02        Spring 02        Fountains  99    colors: Chalk #EFE9DE, Clay #C98D6B, Moss #7A8B6F
4  spring-mini      Spring Mini      Fountains  79    colors: Chalk #EFE9DE, Steel #C7CBD0
5  feast-01         Feast 01         Feeders    149   colors: Chalk #EFE9DE, Graphite #2E3134
6  feast-01-pro     Feast 01 Pro     Feeders    229   colors: Graphite #2E3134                          badge: Pro
7  feast-mini       Feast Mini       Feeders    89    colors: Chalk #EFE9DE, Sand #D8CBB8
8  still-bowl       Still Bowl       Bowls      45    colors: Chalk #EFE9DE, Clay #C98D6B, Steel #C7CBD0
9  still-mat        Still Mat        Bowls      29    colors: Sand #D8CBB8, Moss #7A8B6F
10 play-snuffle     Play Snuffle     Play       39    colors: Oat #E4D8C3, Moss #7A8B6F
11 play-ball        Play Ball        Play       24    colors: Coral #E8734A, Oat #E4D8C3
12 filter-3         Filter 3-pack    Care       19    colors: (omit or single Chalk)
13 pump             Replaceable Pump Care       18   colors: (omit or single Graphite)

Spec rows per product must use only the real facts in the brief:
- Fountains: Capacity, Water contact, Sound, Teardown, Dishwasher-safe, Filter life, Pump life, Cable
  (choose 6 of these per product, adjusting capacity to the model).
- Feeders: Capacity, Portions, Hopper, Bowl, Power, Connectivity, Camera (Pro only), Backup.
- Still Bowl: Capacity, Material, Base, Dishwasher-safe, Dimensions, Weight.
- Still Mat: Size, Material, Lip, Dishwasher-safe, Colors, Weight.
- Play Snuffle: Size, Material, Wash, Suits, Colors, Weight.
- Play Ball: Size, Material, Treat opening, Wash, Suits, Weight.
- Care: Pack size, Fits, Life, Material, Price note, Made in.

Rules:
- `desc` must not repeat the tagline. It should say what the object is and the one thing that makes it
  good, then stop. No feature lists in prose.
- `bullets` are scannable chips, not sentences.
- Do not invent certifications, awards, review counts, or stock levels.
- Toys: say clearly they survive normal play and are washable, not indestructible.
- Keep both languages the same length within ±20%.
