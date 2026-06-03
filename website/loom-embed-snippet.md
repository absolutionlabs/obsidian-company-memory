# Loom embed snippet

Paste this above the install URL fold on the install landing page (`absolutionlabs.com/obsidian` per [overview-page.md](overview-page.md) § 2 "Loom video block").

Until the Loom is recorded (operator task), this is a placeholder spec. Scene 6 of the script no longer requires `absolutionlabs.com/privacy` to be live (v1.2.0 removed the telemetry surface that earlier scripts referenced).

---

## Embed snippet (Loom)

Loom's share modal gives you both an `<iframe>` snippet and an `<oembed>` URL. Use the `<iframe>` form for the install page — better mobile behaviour.

Replace `<LOOM_VIDEO_ID>` with the 32-char video ID from the share URL after the recording is done.

```html
<div class="loom-embed-wrapper">
  <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
    <iframe
      src="https://www.loom.com/embed/<LOOM_VIDEO_ID>?hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true"
      frameborder="0"
      webkitallowfullscreen
      mozallowfullscreen
      allowfullscreen
      style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
      title="Obsidian Company Memory — Guided Install"
      loading="lazy">
    </iframe>
  </div>
</div>
```

CSS notes:

- `padding-bottom: 56.25%` enforces a 16:9 aspect ratio.
- `loading="lazy"` defers the iframe load until scroll-in; reduces initial page weight to ~0kb for visitors who don't scroll.
- The `?hide*=true` query params strip Loom's logo bar, owner avatar, share button, and title from the embedded player. Cleaner trust artifact; the Loom title still appears in the share preview if anyone copy-pastes the URL.
- No autoplay. No muted-autoplay. Viewer clicks to play; that's the right consent shape per [install-page.md](install-page.md) §"Loom video block".

---

## Caption / title above the embed

Render the body copy from [install-page.md](install-page.md) §2 verbatim:

> A walkthrough by Rob — what the skill installs, why it asks what it asks, and the round-trip test that proves it worked. Worth watching before you install if you're in a regulated sector.

Keep this above the embed even on mobile. The line is the trust signal that makes the prospect press play.

---

## Fallback (no video yet)

Until the Loom is recorded, the install page should NOT show a broken embed or a "video coming soon" placeholder. Instead, replace section 2 of the install page with:

> A guided-install walkthrough is being prepared. It'll embed here. In the meantime, the install procedure is documented in full in the [README on GitHub](https://github.com/absolutionlabs/obsidian-company-memory#install).

Soft framing; doesn't promise a date; doesn't apologise.

---

## When the Loom is recorded

1. Upload to Loom.
2. Copy the 32-char video ID from the share URL.
3. Paste into the snippet above (replace `<LOOM_VIDEO_ID>`).
4. Drop the rendered HTML into the install page (per [install-page.md](install-page.md) §2).
5. Verify the embed renders cleanly in three browsers (Chrome, Safari, Firefox) + on mobile.
6. Test that the `?hide*=true` params strip the chrome you want stripped — Loom's params occasionally change.

---

## Loom version-pinning

When the skill version bumps and the Loom needs re-recording for the version-specific moments (Scene 6 mentions "version 1.0.0"):

- Record the new Loom against the new version.
- Update `<LOOM_VIDEO_ID>` in the snippet.
- Archive the previous video ID in a comment above the snippet — useful if a regression makes the previous version preferable until fixed.

```html
<!-- v1.0.0 Loom: <LOOM_VIDEO_ID_V1_0_0> (archived) -->
<!-- v1.1.0 Loom: <LOOM_VIDEO_ID_V1_1_0> (current) -->
```

---

## Alternative players (if Loom is later swapped)

If you ever move off Loom (to Mux, Vimeo, self-hosted, YouTube unlisted, etc.):

- Same 16:9 wrapper.
- Same lazy-load.
- Same no-autoplay rule.
- Same "click to play" consent shape.

The decision NOT to autoplay is the trust signal, not the choice of host. Don't autoplay even if the new host defaults to it.

---

*Embed spec only — the Loom recording itself is in [../loom-script.md](../loom-script.md) (operator task to record).*
