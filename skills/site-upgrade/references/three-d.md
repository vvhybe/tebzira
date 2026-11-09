# 3D, when it earns its place

3D is a signature, not a texture. Use it when the idea needs an object or a character the visitor will remember: a mascot drawn from the logo, the product as a physical thing, a scene that carries the story. Don't use it for a spinning blob, a floating abstract shape or "because WebGL is impressive".

## Contents

1. Where the model comes from
2. The exactness gate
3. From a Blender file to the web
4. Runtime
5. Personality
6. Verify
7. A scene laid out from the page

## 1. Where the model comes from

Take the highest rung that exists. Ask the owner before you build anything: "do you have the source file?"

1. **The owner's own model** (`.blend`, `.glb`, `.fbx`, `.usdz`). Always best: it is the brand. A cloud company's helmet mascot was approved only once it came from the owner's own Blender file.
2. **A procedural reconstruction from a reference image**, when no model exists and the subject is an object or a simple character. [img2threejs](https://github.com/img2threejs/img2threejs) rebuilds the object in a reference image as code-only Three.js through staged passes (blockout, structure, form, material, surface, lighting, interaction, optimization), with a detail inventory and a vision review after each pass. Feed it the logo or a clean render, not a photo of a screen.
3. **An image-to-3D generator.** Check the licence and the export before you invest: free tiers often show the model, then put the export behind a paywall. Clean up topology and materials afterwards.
4. **Hand-built primitives,** only for abstract or geometric forms. For anything that represents the brand, approximations get rejected ("a cheap replica with a wide head").

People are never primitives, in 3D or in SVG. A drawn figure of the owner was called cheap; cutting the real person out of their own film was the fix (media.md § 10).

## 2. The exactness gate

Before anything ships, render the model at the reference's own view (for a logo mark, usually a three-quarter view with a long lens and the camera slightly below) and compare them side by side:

- **Silhouette and proportions:** head width to height, the visor's shape, the ring's thickness. Owners read proportions first.
- **Materials by part:** what is glass, what is shell, what is matte. Match the brand's colors under neutral light.
- **What the owner asked to drop or keep:** no body, a black visor (not a mirror), no glowing rim, two soft eyes sized to the head (about an eighth of its height).

Iterate on the screenshot until a stranger would say it is the logo come alive.

**A flat logo as layers.** Trace the largest source with potrace at about 1200 px wide, one mask per color. To animate petals, wings or letters, split the traced outline at its valleys, so every outer edge stays exactly as traced and only hidden edges are invented. Overlay the cut on the real logo at 100% before you use it. A logo at any size inside a scene or an illustration is this vector, never a small redraw.

## 3. From a Blender file to the web

- **Blender without installing it.** A portable LTS tarball from download.blender.org (verify its checksum) runs headless: `blender -b -Y model.blend --python scripts/export.py`. `-Y` keeps the file's embedded scripts from running.
- **Export parts by name** to one `.glb`, so the site can assign materials and animate pieces (eyes, visor, props) by name.
- **Fix the normals.** Faces that point inward look fine in Cycles and show as grooves on the web. Recalculate or flip them in the export script.
- **Optimize** with `@gltf-transform/cli`: `weld`, a gentle `simplify` (start near a ratio that keeps the silhouette) and `quantize`. Draco and meshopt decoders need WebAssembly; a site whose CSP lacks `'wasm-unsafe-eval'` can't load them, so either skip them or add that one directive on purpose.
- Keep the export script in the repo (`scripts/export-model.py`) so the model can be regenerated when the owner edits the source.

## 4. Runtime

- **three.js** directly, or React Three Fiber when the site is React and the scene is component-shaped.
- **Lazy-start** the renderer when the canvas nears the viewport; dynamic-import three.js so it isn't in the first-load bundle.
- **Pause** the render loop off screen and when the tab is hidden; dispose geometries, materials and the renderer on unmount.
- **Cap `devicePixelRatio` at 2.** Use one environment light setup for every placement, so the mascot looks the same in each section.
- **Fallbacks:** a poster image rendered from the same scene for no-WebGL, reduced motion, slow devices and server rendering. The poster is the first paint; the canvas fades in over it.
- **Stills for everything else.** Render stills from the same scene for social cards, blog covers and posters: a temporary studio page with the scene at a fixed pose, captured with Playwright at 2×, exported as WebP plus a small PNG. Re-render them whenever the model changes.

## 5. Personality

- Poses and props per section (a wrench for maintenance, a shield for security, a headset for support, a flag for the finale), and tones per act (an earth tone in the hero, copper in the story).
- A glance at the pointer (fine pointers only), a blink, an idle bob. Small and slow.
- Eyes and details are sized to the model, not to the screen.
- Never let markers, progress bars or copy overlap the character on phones (verification.md).

## 6. Verify

- Frame time in DevTools with 4× CPU slowdown; memory after scrolling the page twice.
- The phone layout at 390 and 320: the model fits, nothing overlaps it.
- WebGL disabled (`--disable-webgl` or a context-loss test): the poster shows.
- Reduced motion: no idle animation, poster or static pose.
- The CSP console scan (verification.md) shows no blocked WebAssembly, workers or blob URLs.

## 7. A scene laid out from the page

A full-screen three.js hero that shipped: the logo standing on water at sunrise, the headline reflected in it, and the scroll flying the camera through the logo into a real film.

- **Measure the DOM, then place the world.** Server-render the logo and headline as plain HTML in their final places. Read their rects, set the camera distance so one logo unit equals its CSS size, and draw the headline into a canvas texture at the spans' own rects (a zero-height inline-block probe gives each baseline). First paint and canvas then match at every width, and the phone layout stays in CSS.
- **Keep the real `<h1>` under the canvas.** Don't fade it to `opacity: 0`; hide it only when the canvas fades away at the end. `page-audit.js` reports zero headings otherwise.
- **Lens shift, not tilt.** `camera.setViewOffset(W, H, 0, H / 2 - horizonY, W, H)` moves the horizon without keystoning, so the plane at `z = 0` still maps linearly to pixels.
- **A planar reflection in a dozen lines.** Mirror the camera to `-y`, copy the projection and negate `elements[5]`, render everything above the water into a half-size target, and sample it in the water shader at `gl_FragCoord.xy / resolution` plus a ripple offset. Fade the ripple with distance, or far water aliases into a comb.
- **Painter's order for layered flat scenes.** `depthTest: false`, `depthWrite: false`, `side: DoubleSide` and `renderOrder`. No z-fighting between layers a hair apart.
- **Exact brand colors.** `ColorManagement.enabled = false`, `renderer.outputColorSpace = LinearSRGBColorSpace`, textures `NoColorSpace`.
- **Canvas text:** `texture.premultiplyAlpha = true`, or edges get a white fringe.
- **Lettering:** `ShapePath.toShapes()` filled the counters of a script face. Sort the rings by area, nest them by point-in-polygon, and treat odd depth as a hole.
- **Film through a window.** Sample the video in screen space with the same maths as `object-fit: cover`. When the window covers the screen, fade the canvas: the `<video>` beneath is pixel-identical.
- **The still page.** No WebGL, data saver, reduced motion or `webglcontextlost` all fall back to the server-rendered page.
- **First-paint picture.** Capture it from the scene itself, without the logo and text meshes. Never `display: none` the DOM boxes the scene measures, or the capture comes out blank.
