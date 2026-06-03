# Private beta gate

The process for moving the skill from private beta (handful of friendly testers) to public ship. Designed to catch the failures the test matrix didn't surface — the human-in-the-loop signals that no checklist captures.

The bundle survives this gate or it doesn't ship publicly. There is no fast path through this; sales-tool framing per [brief.md](../brief.md) Decision #18 means per-install quality is absolute.

---

## Prerequisites (must be true before this gate begins)

- [ ] All 7 personas in [test-matrix.md](test-matrix.md) PASSED
- [ ] Manifest lint (`python scripts/lint_manifest.py`) → 10/10 passing
- [ ] Recovery Drill completed and passed (see [recovery-drill.md](recovery-drill.md))
- [ ] Privacy policy published at `absolutionlabs.com/privacy`
- [ ] Telemetry endpoint live, smoke-tested in production state
- [ ] info@absolutionlabs.com mailbox monitored daily
- [ ] Skill bundle hosted on a public GitHub repo (or equivalent install surface)
- [ ] Loom guided-install recorded and embedded on `absolutionlabs.com/obsidian`

If any of the above is false, the private beta is not ready to start. **Do not invite testers** until they're all green.

---

## Stage 1 — Invite the testers

**Target:** 3–5 testers. More than 5 dilutes the signal; fewer than 3 doesn't sample enough variance.

**Recruit from:**

- Existing Absolution Labs clients with whom you have a candid relationship (Asterley Bros team, etc.)
- Prospects who've expressed interest in the skill (informally; no sales-conversation-conversion gate)
- Peer founders in the drinks / FMCG space
- ONE tester from a regulated sector (finance, legal, healthcare) — this tester's specific feedback weights heavily on the compliance gate's adequacy

**Avoid:**

- Strangers (the feedback loop won't close)
- Anyone for whom this install is part of a sales conversation (their feedback is biased toward saying nice things)
- Anyone you wouldn't WhatsApp directly if they got stuck mid-install

**Invitation format:** personal email + WhatsApp follow-up. NO bulk send, NO mail-merge. Each tester gets their own paragraph.

**What you send each tester:**

1. The install URL (public GitHub repo)
2. The [TESTERS.md](../TESTERS.md) file (paste verbatim or link to the repo)
3. A one-paragraph personal note: why you specifically asked them, what timeline you'd like, what specifically you want to hear
4. Your WhatsApp number for direct support during the test

**Time expected from each tester:** ~30 min install + feedback. Tell them that explicitly.

---

## Stage 2 — Receive feedback

**Window:** 7 days from first invitation.

**Surface:** Email to `info@absolutionlabs.com`. Some testers will WhatsApp instead — capture those threads into the feedback record manually.

**As feedback arrives:**

1. Reply to acknowledge within 1 business day (per the SLA the install page promises).
2. Log each piece of feedback into a triage document at `release/beta-feedback-runs/<YYYY-MM-DD>.md`. Don't paraphrase; capture the tester's actual words.
3. Tag each piece: `bug` / `friction` / `cut suggestion` / `add suggestion` / `vibe`.
4. After receiving 3 testers' feedback, hold a triage decision (alone or with a peer): what's blocking, what's nice-to-have, what's a "no."

---

## Stage 3 — Triage feedback

Three buckets for every piece of feedback:

### Bucket A — Ship-blocking

- Any reported data loss
- Any silent failure
- Any pattern of confusion at the compliance gate (multiple testers stuck on the same checkbox)
- Any pattern of confusion at the round-trip test (Obsidian state vs scaffold state mismatch)
- Any reported install that left a partial scaffold
- A privacy concern that the policy text doesn't already address

**Action:** fix, bump the skill version, re-run the affected test-matrix persona, do not proceed to public ship.

### Bucket B — Address-before-ship

- Friction points multiple testers mentioned (less than blocking but worth one fix)
- Documentation gaps testers explicitly flagged
- README clarity issues
- Loom segments testers paused on or re-watched
- Anything where a regulated-sector tester said "I wouldn't trust this with X"

**Action:** schedule the fix; re-test the affected surface; bump version; proceed to public ship.

### Bucket C — Public-launch nice-to-haves

- One-off suggestions from one tester only
- Style preferences (typography, colour, copy tone) that don't materially affect trust
- Feature ideas that would expand scope

**Action:** log in a backlog file at `release/post-launch-backlog.md`. Do NOT block public ship.

---

## Stage 4 — Decision

Hold the decision 2-3 days after the last tester reply. Don't decide same-day; give the feedback time to settle.

**To proceed to public ship, all of the following must be true:**

- Zero items in Bucket A (or all Bucket A items fixed + re-tested)
- All Bucket B items either fixed or have a documented "deferred to v1.1" decision in the post-launch backlog
- At least 3 of 5 testers said something explicitly positive about the install experience
- At least 1 tester said they'd send the skill to a peer (per the TESTERS.md question 9)
- Zero testers reported lasting concerns about data residency or compliance

**If any of those is false:**

- Fix what's blocking
- Document the deferral
- OR delay public ship

Public ship is binary. "Soft launch" is not a thing; sales-tool framing means every public install is part of the trust artifact.

---

## Stage 5 — Thank-yous and acknowledgements

For testers who gave permission to be named (per the TESTERS.md question on "permission to thank publicly"):

- Mention by name in the public release announcement
- Send a personal thank-you email separately from the announcement
- Send a one-line note when v1.1 ships (only if they opted into the launch notification)

For testers who didn't opt in:

- Personal thank-you email regardless
- No public mention, no follow-up beyond the thank-you

The bar for "what counts as a thank-you-worthy contribution" is intentionally low; finding 5 willing testers is not common, and they bear the cost of being early.

---

## Cadence after public ship

The first 2 weeks after public ship are still "soft" — the install URL is public but the launch announcement hasn't gone out. During this window:

- Daily check of `install_events` in Supabase
- Daily check of info@ mailbox
- Any failure spike → revert public install URL to the previous version (per `docs/upgrading.md`) until investigated
- Tester thread stays open for follow-up; testers' feedback at install + 14 days is the most useful signal

After 2 weeks of clean operation: weekly cadence is enough.

---

*This gate is the difference between a sales tool and a free-skill-the-publisher-shipped-and-walked-away-from. The cost of running it carefully is days; the cost of skipping it is a prospect's first impression of Absolution Labs.*
