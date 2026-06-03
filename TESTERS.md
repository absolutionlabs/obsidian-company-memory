# Obsidian Company Memory — Tester Instructions (Private Beta)

Thank you for taking 30 minutes to try this. You're one of a small handful of testers we're sending it to before it goes public. Your feedback shapes what we ship.

This document is the install + use + feedback loop. Nothing in here is permanent — anything you scaffold is yours to keep or delete.

---

## Before you start

You will need:
- **20–30 minutes of uninterrupted time.** The install itself takes ~5 min; the rest is reading what's there + watching the round-trip test work.
- **A laptop running macOS 12+ or Windows 10/11.** Linux works but is less tested for v1.
- **Obsidian installed.** Free download at [obsidian.md/download](https://obsidian.md/download). Install it, then close it — don't create a vault yet.
- **An empty folder inside Dropbox, iCloud, OneDrive, or Google Drive.** Name it something like `CompanyMemory-Test/`. Must be empty.
- **One AI tool:** either Cowork (browser, easiest) or Claude Code (terminal, also fine).

You will not need:
- A credit card. The skill is free.
- A sign-up. No account creation, no email gate.
- Any prior technical experience beyond "I've used ChatGPT."

---

## Install

The current install URL is on the project's GitHub repo. Rob will have sent you the link directly — it's a `https://github.com/...` URL.

### If you're using Cowork

1. Open Cowork.
2. Settings → Plugins → Install from URL.
3. Paste the URL Rob sent you.
4. Approve the install.
5. Start a new conversation and say: **"Set up my Obsidian company memory."**

### If you're using Claude Code

1. Open a terminal.
2. Clone the repo Rob linked into `~/.claude/skills/obsidian-company-memory/`:
   ```
   git clone <repo-url> ~/.claude/skills/obsidian-company-memory
   ```
3. Restart Claude Code.
4. Start a session in any folder (it doesn't matter where) and say: **"Set up my Obsidian company memory."**

---

## What you should see during install

The skill walks you through nine steps. Pay attention to each — they're designed to be visible, not magical.

1. **Compliance gate (3 checkboxes).** The skill won't write anything until you tick three boxes confirming the folder is yours, your cloud sync is allowed for the content, and Absolution Labs has no access. Take a moment to read each.
2. **Refuse-to-scaffold check.** If your folder isn't empty, the skill refuses. This is intentional. If it refuses incorrectly: tell us.
3. **Two questions.** Company name (any test name — "Acme Co" is fine) and your sync provider (pick whichever applies).
4. **Telemetry surface.** The skill explains a single anonymous install ping it sends to a Supabase database we run in London (EU). It contains no personal data. You can opt out with one click. **Whether you opt in or out, please note your choice** — we'd like to see this surface read clearly.
5. **Scaffold writes.** About 20 files land in your folder over a few seconds. The skill names each one.
6. **Round-trip test.** The skill creates one welcome page and asks you to open it in Obsidian to confirm everything works.
7. **Phase 2 handoff.** The skill points you at `HOW-TO-USE-THIS.md` in your vault for ongoing use.

If at any step something feels confusing, scary, or broken: **note it** and tell us. There are no stupid observations.

If you'd rather **read** the install procedure step-by-step before running it (some people prefer this to watching it happen live), see [docs/install-walkthrough.md](docs/install-walkthrough.md) in the bundle. It mirrors what the skill does, in plain prose.

---

## What we'd like you to do once installed

1. **Open the vault in Obsidian.** File → Open vault → pick your folder.
2. **Read `HOW-TO-USE-THIS.md`** (about 10 min). It's the guide to using the system day-to-day.
3. **Try one real thing.** Pick a fact about your company you've explained ten times before — your typical lead time, your pricing rule, your product positioning — and ask your AI to capture it as a wiki page. Watch what lands. Open the file in Obsidian. Click the wikilinks.
4. **Run a lint.** Ask your AI: "run a lint on the vault." See what it does, what it flags.
5. **End the session with `/close-full`** (or just say "let's close out"). See whether the close protocol works for you.

That's it. About 30 minutes total.

---

## What we'd like you to send back

Email `info@absolutionlabs.com` with subject line: **`Tester feedback — Obsidian Company Memory`**.

There's no form. Just write whatever you noticed, in plain English. The 6 questions below are a prompt — don't feel obliged to answer all of them.

1. **Did the install work?** Where did you pause? Where did you get stuck (if anywhere)?
2. **The compliance gate** — did it feel reassuring, friction-tax, or somewhere between?
3. **The refuse-to-scaffold gate** — did you trigger it accidentally? If so, what did you try to install into?
4. **The round-trip test** — did Obsidian show you what the skill said it would?
5. **The Phase 2 guide (`HOW-TO-USE-THIS.md`)** — anything missing, confusing, or wrong?
6. **The overall vibe** — did the skill feel like something a serious publisher made? Or did it feel rough? What specifically gave you each impression?

Three more questions we'd love to know but don't expect everyone to address:

7. If you've used Obsidian before — does the three-layer architecture (raw / wiki / schema) feel sensible or alien?
8. If you're in a regulated sector — does the compliance gate go far enough, too far, or about right?
9. Would you send this skill to a peer? With or without a caveat?

---

## A few practical notes

- **Your vault is yours.** Anything you create stays on your disk. We don't see it. We can't see it. If you delete the folder, it's gone — and that's the only way to "uninstall" the data.
- **The telemetry, if you don't opt out, is one HTTPS ping containing eight anonymous fields.** Full text of what gets sent is in `docs/privacy-policy.md` inside the bundle. UUID is shown to you at the end of install; email `privacy@absolutionlabs.com` with that UUID to request deletion at any time.
- **You can run the skill on multiple folders.** Each one is a fresh, independent vault. Useful if you want to try once with your real company name and once with a throwaway name.
- **If you find a bug or hit an error, please send the exact message** (screenshot or paste) along with: which AI tool, which OS, which sync provider. That gives us everything we need to reproduce.
- **You don't need to write up your feedback formally.** A 100-word email beats a polished report — we'd rather have your raw reactions in the first hour than something considered after a week.

---

## What we'll do with your feedback

- Read every email within one business day.
- Use it to revise the bundle before public ship.
- Mention you in the public release thank-you (with your permission) if your feedback materially shaped what shipped.
- Not send you marketing follow-up. You're a tester, not a lead.

If you want, after the tester round, we'll send you a short note when the public version ships. Mention it in your feedback email if so.

---

## Direct support during your test

If you get genuinely stuck and don't want to wait for an email reply:

- **WhatsApp Rob directly** — he's reachable on the number you have for him already. Same-day response on test days.
- **Or just write back to `info@absolutionlabs.com`** — Rob monitors it during the test window.

Thanks for trying this. We owe you one.

— Rob, Absolution Labs LTD
