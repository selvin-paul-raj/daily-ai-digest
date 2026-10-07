# Post conventions

Rules the daily post follows. These come from Selvin directly.

## Media

Every post carries visual media when a story has any. In order of preference:

1. **The original image or video from the X post** that broke or best illustrates the story. Read the public post page at `https://x.com/<handle>/status/<id>`, pull the media, upload it to the LinkedIn composer.
2. **A carousel** when the digest covers three or more stories worth showing. LinkedIn renders carousels from an uploaded PDF, so build a multi-page PDF in the sandbox (one story per page, large readable type, consistent theme) and upload that as the document.
3. **A generated visual** only when neither of the above exists: a clean chart or diagram of the actual numbers in the story. Never a stock illustration, never a fake screenshot.

## Credit

Any media or framing taken from someone else's X post gets credited in the post body, on its own line, as:

```
Credit: @handle
```

Several sources on one post get one line: `Credit: @handle, @handle`. This is non-negotiable. Reposting someone's visual without the handle is white-labeling their work.

## Links

No links in the post body. LinkedIn suppresses reach on posts with outbound links, so every source URL goes into the **first comment** on the post, added immediately after publishing, formatted as:

```
Sources:
1. <headline> <url>
2. <headline> <url>
```

## Voice

900 to 1300 characters. A real hook on line one. Concrete verified numbers. One genuine opinion or synthesis. Two smaller "also worth your time" items. One discussion question to close. Four or five hashtags. No em dashes, no emoji, no hype adjectives, no AI tells. Craft conventions follow https://github.com/sergebulaev/linkedin-skills.

## Carousel format (from 2026-10-07)
Every carousel follows CAROUSEL.md and is rendered with tools/carousel/pro.py (hook, setup, 2-3 stat slides, my take, follow). Do not hand-draw slides.
