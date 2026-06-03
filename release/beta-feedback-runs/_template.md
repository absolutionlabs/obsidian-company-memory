# Beta feedback — YYYY-MM-DD

Copy this file to `release/beta-feedback-runs/<YYYY-MM-DD>.md` when the first tester replies. One run-file per private-beta cohort; capture every tester into the same file as their feedback arrives. Holds the raw feedback verbatim, the bucket call, and the audit trail back to the action taken.

Spec: [private-beta-gate.md](../private-beta-gate.md) Stage 2 (capture) + Stage 3 (triage).

---

## Cohort

| Field | Value |
|---|---|
| Cohort opened | YYYY-MM-DD (date first invitation sent) |
| Cohort closed | YYYY-MM-DD (7-day window per Stage 2) |
| Testers invited | N (target 3-5) |
| Testers replied | N |
| Regulated-sector tester | name (per Stage 1 — exactly one) |
| Triage decision held | YYYY-MM-DD (2-3 days after last reply per Stage 4) |
| Decision | proceed / fix-and-re-test / delay |

---

## Capture rules (apply before triage)

1. **Verbatim.** Tester's actual words. No paraphrase. Quote blocks for anything > one sentence.
2. **One row per discrete piece of feedback.** A tester saying "the compliance gate was confusing and the Loom was too long" is two rows.
3. **Tag column** uses one of: `bug` / `friction` / `cut suggestion` / `add suggestion` / `vibe`.
4. **Acknowledge within 1 business day** (the SLA the install page promises) BEFORE capturing here. Tick the ack column after.
5. **WhatsApp threads** captured manually into the same table; note `WA` in the source column.

---

## Feedback

| # | Tester | Source | Ack'd | Tag | Verbatim quote | Bucket (A/B/C) | Action | Linked artefact |
|---|---|---|---|---|---|---|---|---|
| 1 | | email / WA | ☐ | bug / friction / cut / add / vibe | "..." | | | |
| 2 | | | ☐ | | | | | |

---

## Bucket triage rubric (cheat-sheet)

Mechanical classification from [private-beta-gate.md](../private-beta-gate.md) Stage 3. When in doubt, escalate one bucket (B before C, A before B).

### Bucket A — Ship-blocking → fix, bump version, re-run affected persona, DO NOT proceed to public ship

- Any **reported data loss** (even single tester, even small)
- Any **silent failure** (skill exits cleanly but didn't do what it said)
- **Pattern of confusion** at the compliance gate (≥2 testers stuck on the same checkbox)
- **Pattern of confusion** at the round-trip test (Obsidian state vs scaffold state mismatch)
- Any reported **partial scaffold** left on disk
- A **privacy concern** the policy text does not already address

### Bucket B — Address-before-ship → schedule fix, re-test affected surface, bump version, proceed

- **Friction points multiple testers mentioned** (less than blocking but worth one fix)
- **Documentation gaps testers explicitly flagged**
- **README clarity issues**
- **Loom segments testers paused on or re-watched** (trust signal)
- Anything where the **regulated-sector tester** said "I wouldn't trust this with X"

### Bucket C — Public-launch nice-to-have → log to `post-launch-backlog.md`, DO NOT block ship

- **One-off suggestions from one tester only**
- **Style preferences** (typography, colour, copy tone) not materially affecting trust
- **Feature ideas that would expand scope**

### Edge calls

- A single-tester bug report on the install path = **A** (single = enough; install is the artefact).
- A single-tester friction-or-vibe comment = **C** by default; **B** if the tester is the regulated-sector seat.
- "I wouldn't send this to a peer" from any tester = **B** (counts against Stage 4 criterion 4).
- Compliance gate confusion from the regulated-sector tester only = **B** (single tester, but weighted seat).

---

## Aggregate signals against Stage 4 decision criteria

Tick once at triage (Stage 4, held 2-3 days after last reply).

| Criterion | Status | Evidence |
|---|---|---|
| Zero items in Bucket A (or all A items fixed + re-tested) | ☐ | |
| All Bucket B items either fixed or have a documented "deferred to v1.1" decision in `post-launch-backlog.md` | ☐ | |
| ≥3 of 5 testers said something explicitly positive about the install experience | ☐ | quote # rows from above |
| ≥1 tester said they'd send the skill to a peer (TESTERS.md Q9) | ☐ | quote # row |
| Zero testers reported lasting concerns about data residency or compliance | ☐ | |

**If all 5 are true** → proceed to public ship (record date below).
**If any is false** → fix what's blocking OR delay; record decision below.

---

## Decision

- **Held:** YYYY-MM-DD
- **Decision:** proceed / fix-and-re-test / delay
- **Rationale:** one paragraph
- **Next action:**

---

## Linked Bucket A fixes (if any)

| Date | Fix | Skill version bump | Re-test persona | Result |
|---|---|---|---|---|
| | | | | |

## Linked Bucket B fixes (if any)

| Date | Fix | Skill version bump | Surface re-tested | Result |
|---|---|---|---|---|
| | | | | |

## Linked Bucket C items pushed to backlog

See [post-launch-backlog.md](../post-launch-backlog.md). Backlog rows must reference this feedback-run file by date.
