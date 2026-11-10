# Feedback: what owners say, and what to change

Owners rarely speak in design terms. They say "not enough spice" or "it looks cheap", and the fix is almost never what the words suggest at first. These are real reactions from shipped upgrades, what they turned out to mean, and what fixed them. Read this whenever the owner reacts, and save new reactions to memory.

## Contents

1. The decoder
2. How owners like to work
3. What owners approved

## 1. The decoder

| The owner says | It means | Do |
| --- | --- | --- |
| "Not enough spice. It's just 'we added a video'." | The change is an addition, not an upgrade. The site still doesn't show off the product. | More product, more interaction, more depth: a live demo, real artifacts, a story that moves. Not more decoration. |
| "It feels like PowerPoint, not a website." | Stacked centered blocks that each fade in. | Composition: pinned stories, layered depth, interactive demos, state-driven motion (motion.md). |
| "I want #upgrade, not #update." | A plain label where a crafted moment belongs. | Turn the call to action into a moment: a live preview capsule with a progress ring and chapter captions instead of "Watch in 23 seconds". |
| "Not the kind of spice I'm looking for. I want a full renovation." | A light-touch pass was offered for a request that wanted a new direction. | Start from discovery and the idea sentence again; propose a whole direction, palette to mascot. |
| "The colors are out of balance. We need color theory." | Proportion and temperature are off, not one hex. | A temperature contrast (complementary warm against cool) and 60/30/10 proportions; accents with single jobs (direction.md § 3). |
| "All indigo is boring, the average purple AI style." | One generated hue everywhere. | The product's own palette and icon tones, varied per topic. |
| "The contrast looks forced." | A saturated brand color slammed against white. | Tints and mid-tones between them; keep contrast natural. |
| "It's a cheap replica with a wide head." | An approximation of the brand's own mark. | Get the source asset (the owner's model) and pass the exactness gate (three-d.md). |
| "You used a cheap trick." | A shortcut that looks like the real thing at a glance (a logo pasted over a QR code). | Do it properly (media.md § 6), or ask for the asset you need. |
| "This is a dull, flat display." | Numbers or facts set as plain text in a row. | Make them a designed moment: floating cards that count up, with real swatches or icons. |
| "Templates aren't a background for your data; each has its own personality." | The differentiator is shown as an image gallery. | Spotlight behavior: group items by what they do, from their own descriptions (building-blocks.md § Spotlighting). |
| "That language switch hanging there is awful." | A default control in a crafted page. | A segmented `FR \| EN` control that belongs to the design. |
| "It's jerky." | Motion that performs (a 3D flip) where a calm one answers. | Sheets that slide, short eased transitions; motion that shows what changed. |
| "The illustration looks smaller on mobile; it could take the full screen." | The phone version is the desktop squeezed. | Give the phone its own composition: full-bleed art, its own crop. |
| "Poor in illustrations of our clients' problems." | The site lists services; it doesn't show the visitor's situation. | Problem-to-answer illustrations (building-blocks.md § Company and B2B). |
| "We should speak directly to them." | The copy talks about the company. | Second person, the visitor's pains in their words, then the relief. |
| "Not generic." | Category defaults. | Back to the subject inventory: the owner's words, their name, their place. |
| "I don't have those numbers now, but we can add them later." | Unknown, not zero. | Remove the figure, make the component accept an empty value, and send a fact-check form. |
| "Why add them as secrets? They're links." | Over-engineering public config. | Public values are plain env values; only real secrets are secrets. |
| "Make it an env, to make things standard." | A boolean switch or a hardcoded constant. | An env var that holds the value (a URL); empty means off (a greyed "Coming soon"). |
| "The idea is good but it's not practical. It feels stuttery, slow, awkward." | The concept is approved and the mechanism is rejected. | Keep the idea and what they praised. Replace how it moves (motion.md § 2). Don't defend it and don't restart. |
| "Creepy noise sound." | Sound nobody asked for. | Remove it. |
| "It's a joint SVG, that's cheap these days." | A drawn character. | Real material: cut the person out of their own footage (media.md § 10). |
| "The name is actually X." "Use the exact logo, not a miniature." | Brand details taken from a weak source or redrawn. | Go to the brand file and fix every instance. Drop any copy built on the wrong reading. |
| A batch of screenshots with short notes | They are pointing at pixels. | Fix each one, then hunt the same class of defect elsewhere: the same images held two more. |
| "A small overlap on mobile" (their phone's screenshot) | The layout was checked at a 390×844 viewport, not at the height a phone browser leaves. | Measure at 553 to 760 px tall and fix the coupling: something placed by height next to something sized by width (verification.md § 3). |
| "The mark doesn't look like the original, at least the same flower and the same figure." | The header mark was cropped by its viewBox and recoloured. | Frame the whole mark from its bounding box, in its own colours, with a keyline for light grounds; regenerate the icons from it. |
| "The accent color dominates the negative space." | Large flat areas in one brand color. | The brand's own geometry from the owner's other products, pooled in the open space and fading before the words, slow and faint (motion.md § 4). |
| "People who want to stay and watch get an in-between frame." | The clean state of a scroll scene exists only at its last pixel. | A pinned stop after the hand-over, and a timed fade at a threshold instead of a scroll-tied blend. |
| "Don't let this masterpiece be shy in the menu." | A signature hidden behind a link. | Its own page with SEO, a door on the home page, and the 404 (building-blocks.md § A minute the visitor can do). |
| "We're missing sound for this." (after "creepy noise" elsewhere) | Sound inside an experience the visitor starts is welcome; ambient sound is not. | Sound made in the browser, started by their click, with a visible mute that is remembered (media.md § 11). |
| "What's the point of that sticky line?" | A component that outlived the concept it was built for. | Keep its best idea in the smallest form (a scroll sensor that appears only when rushed) or remove it. |

## 2. How owners like to work

- **Iterations, home page first.** "Let's focus on the home page for now; once we're good, you can do the other pages."
- **A plan before code** on big moves; a short status ("where are we now?") on request, without a wall of text.
- **One question at a time, with options.** Owners answer numbered questions quickly ("1: yes, 2: leave it open, 3: me").
- **A second direction on its own branch** when they want to compare, and the losing one archived, never deleted.
- **Short, paste-ready updates** for the team after each PR, and a living before/after report when a boss is watching.
- **Stacked PRs** for separable work (the redesign, then SEO), and a merge order when there are several.
- **Their consent is specific.** "Push and open PRs" is not "merge" and not "change the domain". Ask for each new kind of outward step.
- **Explanations for them only** when they ask how something works ("elaborate for me so I can follow along"): plain, short, no jargon.
- **Ideas arrive mid-build, and they are often better than yours.** A hand-drawn trail map with a tiny walking character came in the middle of a turn. Say yes in one line, fold it in, keep going.
- **"Tell me if you need a tool."** Answer with one recommendation, the exact file, source and size or price, and a no-tool fallback. Check balances first; a connected service may have no credits.
- **Numbered questions at the end of a report** come back as numbered answers within minutes.
- **"I'll leave it to you."** When the owner hands you a decision, make it, give the reason in a sentence, and keep it reversible.
- **They review previews on their phone.** Send the preview link with the exact addresses to try (the page, a made-up address for the 404, a `?sky=` hour); Cloudflare cuts branch aliases to 28 characters.

## 3. What owners approved

- A real A4 invoice as the demo, instead of an abstract "math done" section.
- Story progress bars of equal length that advance on their own when the visitor lingers.
- Ambient video muted and looping.
- FAQ and Contact in the navbar; a stable footer on every page; a contact form that really delivers, with fixed `Website:` subjects and a designed email.
- The SEO and standards work as a separate stacked PR.
- A countdown the visitor walks through by scrolling, instead of tabs they can skip.
- A catalog of real brand logos that leads to a prefilled contact form.
- A 404 that is a game (a singularity, a press-and-hold big bang) or a joke in the product's own language (a NOT FOUND stamp on an invoice).
- A corporate direction inspired by large infrastructure sites, with the first direction's best moments kept.
- A help center that relates every guide to a real screen, in the app's own icons and tones.
- The logo standing in a live scene built from art the owner already had.
- The real person, cut out of their own film, walking a hand-drawn map, with their own words in speech bubbles.
- A 404 that is a tiny game in the site's own world.
- A one-minute guided breath as the signature: the logo breathing over a ground that goes from noise to clarity, with its own sound, its own page, a door on the home page, and the 404.
- The hero's sky following the real hour and place: the sun where it is, the moon in its phase.
- The brand's sacred geometry in flat sections, faint and slow: "that's the right portion".
- A scroll sensor that says "gently" only when the visitor rushes.
