# Post-launch backlog

Destination for Bucket C items from private-beta triage per [private-beta-gate.md](private-beta-gate.md) Stage 3, plus any post-public-ship items deliberately deferred to a future minor version.

**Bucket C definition:** one-off tester suggestion, style preference not materially affecting trust, or feature idea that would expand scope. Logged here so it isn't lost; does NOT block public ship.

**Bucket B "deferred to v1.1" items also land here** with explicit decision per Stage 4 criterion 2. Mark those rows with `deferred-from-B` so the audit trail is unambiguous.

---

## Open items

| # | Date | Source (feedback-run file or thread) | Tester | Item (verbatim or close paraphrase) | Class | Disposition | Owner |
|---|---|---|---|---|---|---|---|
| | | | | | bucket-C / deferred-from-B | open / v1.1 / declined | |

---

## Closed items

| # | Date opened | Date closed | Item | Resolution | Linked version / commit |
|---|---|---|---|---|---|
| | | | | done / declined / superseded | |

---

## Triage rules for this file

1. **Every row must reference its origin** — the `<YYYY-MM-DD>.md` feedback-run file, or an email thread / WhatsApp message stamped with date. No anonymous entries.
2. **"Declined" is a valid resolution** but requires a one-sentence rationale in the resolution cell. Silent decline = lost institutional memory.
3. **Class column is immutable once set.** A C item escalated later by additional signal is a NEW row with `escalated-from-#N` in the disposition cell; the original stays.
4. **Review cadence:** scan this file at the start of every minor-version planning session. The first such session is post-public-ship + 2 weeks per the gate's soft-launch window.
