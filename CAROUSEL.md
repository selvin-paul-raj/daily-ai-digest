# How JOE builds a carousel

Reference: the Oct 6 2026 sample (EmbeddingGemma 2 vs Mistral Large 4). Renderer: `tools/carousel/pro.py`.

## 1. Story first, design second
Every carousel follows a 7 to 10 slide arc:
- **hook**: one bold claim with a number ("A 740M model beat a 1 trillion one"). Under 12 words, no question. This slide does 80% of the work. Label pill = topic + date. Hero image below.
- **text** (setup): the context in 2 lines.
- **stat** x2 or x3: one huge number, one short title, one short body.
- **take**: Selvin's opinion. This is what gets comments.
- **follow**: photo, name, handles, one ask (save or share).

Rules: under 20 words per slide body, one idea per slide, every number from a source actually read this run (sources go in the first comment).

## 2. Design system
- Background: dark navy gradient #0B1220 to #111A2E, faint grid, blue glow top right.
- One accent per post: blue, teal, violet, amber or green. Never rainbow.
- One font family: Poppins. Bold titles, Regular body, Bold small CAPS labels.
- Hierarchy: label (small, accent, caps) > title (big, white) > body (light grey).
- Giant stat numbers (~210 px) in the accent colour.
- 80 px margins. Header on every content slide: avatar, name, tagline. Footer: SWIPE arrow + progress bar.
- Size 1080x1350 (4:5).

## 3. Hero image prompt (no text in the image)
> Vibrant 3D clay-style illustration of [concept, e.g. a tiny glowing chip outweighing a giant server tower on a balance scale], soft studio lighting, dark navy background, [accent colour] rim light, glossy materials, centered composition, no text, no logos

Always say "no text". Concepts only: never a real person, product screenshot or logo. Check the image before use; regenerate if it contains letters.

## 4. The tool
```
cd tools/carousel
python3 pro.py spec.json out/     # out/slide_01.png ... out/carousel.pdf
```
`spec.json` keys: `accent`, `author` {name, tagline, avatar, handles[{icon,text}]}, `slides[]` with `type` (hook | text | stat | take | follow), `label`, `title`, `stat`, `body`, `hero`. Text auto-shrinks to fit. See `spec.example.json`.

Upload `carousel.pdf` to LinkedIn as a document (sharebox `detourType=DOCUMENT`). PNGs work for X and Instagram.

## 5. Content prompt
> Turn this news into an 8-slide LinkedIn carousel for AI engineers. Slide 1: a hook with a specific number, under 12 words, no question. Slides 2 to 6: setup, then one stat per slide (big number, 4-word title, body under 20 words). Slide 7: my opinionated take. Slide 8: follow CTA. Only use numbers from this source: [source]. Output JSON with keys type, label, title, stat, body.
