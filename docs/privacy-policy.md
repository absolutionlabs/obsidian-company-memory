# Privacy Policy — Obsidian Company Memory Skill

**Effective date:** *(to be set when published)*
**Publisher:** Absolution Labs LTD, registered in England and Wales *(company number to be filled in)*, registered address *(to be filled in)*
**Contact for privacy matters:** `privacy@absolutionlabs.com`

> **Draft status — not yet published.** This text is the canonical source for the privacy page that will live at `absolutionlabs.com/privacy`. It covers ONLY the Obsidian Company Memory install telemetry; the wider Absolution Labs privacy policy (covering the website, contact forms, the sales pipeline, Hermes operations, client engagements, etc.) is a separate document. This text should be reviewed by a UK GDPR / data protection lawyer before publication. The author of this draft is not a lawyer.

---

## 1. What this policy covers

This policy describes the data Absolution Labs LTD ("we", "us") collects when you install the **Obsidian Company Memory** skill, and what we do with it.

It does **not** cover:

- the contents of the vault the skill scaffolds (we never see them)
- anything you do with the vault after install (we never see it)
- your use of the Absolution Labs website, sales conversations, or other engagements (covered by our main privacy policy)
- data handled by Obsidian, your AI assistant (Cowork, Claude Code, Codex, opencode, etc.), or your cloud sync provider (each governed by their own policies)

---

## 2. The short version

When you install the skill, we receive **one anonymous ping** per install attempt. The ping contains a random identifier, the skill version, your OS family, the install surface, the cloud sync provider you chose, and whether the install succeeded or failed. **It contains no other data.** It is stored in an EU data centre for 24 months, then deleted. You can opt out at install time with one click, or request deletion at any time by emailing `privacy@absolutionlabs.com` with the random identifier shown to you at install.

The rest of this document is the long version of the same statement.

---

## 3. What we collect

When the skill runs, it sends one HTTPS request per install event to a Supabase PostgREST endpoint we operate (`https://vujwcvqiwwpncnhgxjsu.supabase.co/rest/v1/install_events`). The body of that request is a JSON object containing exactly nine fields:

| Field | Example value | Why we collect it |
|---|---|---|
| `uuid` | `7c2e3a14-9b8d-4f12-bc55-2e0c41d8a9b3` | Random v4 UUID generated on your machine at install time. The only handle you have to request deletion. **Not linked to your name, email, IP, company, or vault contents.** |
| `skill` | `obsidian-company-memory` | Identifies which skill produced the ping. We may publish other skills later; this field disambiguates. |
| `version` | `1.0.0` | The version of the skill you installed. Lets us detect installs failing on a specific version. |
| `os` | `darwin` / `win32` / `linux` | OS family only, not the specific version. Lets us detect installs failing on a specific platform. |
| `surface` | `cowork` / `code` | Whether you installed via Cowork or Claude Code. Lets us prioritise fixes by surface. |
| `sync_provider` | `dropbox` / `icloud` / `onedrive` / `google-drive` / `local-only` | The sync provider you confirmed in the install dialog. Lets us detect installs failing on a specific provider. |
| `outcome` | `attempted` / `success` / `failed` | Whether the install completed. Failed installs are the most valuable signal — they tell us to dispatch a fix. |
| `failure_step` | `round_trip` (optional) | If the install failed, a short string naming which step failed. Capped at 64 characters; categorical only. |
| `ts` | `2026-06-03T12:34:56Z` | When the ping was sent, in UTC. |

We do **not** collect:

- your name, email, or any direct contact details
- your IP address (it is visible to Supabase's load balancer in transit but is not stored in our database; Supabase's platform-level rate limiting may use it, but we do not retain it)
- the name of your company, your vault contents, or any document in your vault
- any identifier from your machine other than the random UUID generated specifically for this install
- analytics events, browser fingerprints, cookies, or tracking pixels
- anything else

The server enforces this list by schema-validating every incoming ping and rejecting any payload containing fields outside the table above.

## 4. Lawful basis

We process the data described in §3 under the **legitimate interests** lawful basis (UK GDPR Article 6(1)(f)). The legitimate interest is: detecting and fixing installs that fail, so that the skill works reliably for the people who use it.

We have assessed this against the necessity and balancing tests. The data is fully anonymous, the volume is minimal (one ping per install), the impact on you is effectively zero, and the alternative (no telemetry) would let preventable install failures persist undetected. We consider the balance struck in your favour.

If you disagree with this balance, you can opt out at install time (§7) or request deletion afterwards (§8). Either action is honoured immediately and without penalty.

## 5. Where the data is stored

The endpoint and database run on Supabase, with our project hosted in West Europe (London, `eu-west-2`). Supabase Inc. is our processor for this data; their infrastructure runs on Amazon Web Services in the same region. We have a Data Processing Agreement (DPA) with Supabase.

We do not transfer this data outside the UK / EEA. If we ever need to (we have no current plan to), we will update this policy and rely on UK IDTA + EU SCCs as the transfer mechanism.

## 6. How long we keep it

Each ping is retained for **24 months from its timestamp**, after which it is automatically deleted by a monthly prune query. Aggregated counts derived from the data may be retained longer (e.g. "10,000 installs in 2026") but contain no individual UUIDs.

DSAR audit records — UUIDs that have been deleted on request, with the date of deletion — are retained indefinitely as required by UK GDPR Article 30 record-keeping obligations. These records contain only the UUID + timestamp + a short operator note; they do not contain the deleted data itself.

## 7. Opting out

At install time, the skill shows you the telemetry surface and a single checkbox: "I prefer NOT to send this ping." If you tick it, no telemetry is sent for that install, and the install proceeds identically.

Opt-out is per-install. If you re-install the skill later and want to opt out again, tick the box again — the skill does not remember the previous choice.

## 8. Your rights (Data Subject Access Rights)

Under UK GDPR you have the right to:

- **Access** the data we hold about you. Email `privacy@absolutionlabs.com` with your UUID and we will return the rows.
- **Rectify** inaccurate data. There is little to rectify — the only fields are technical — but the right exists.
- **Erase** the data. Email `privacy@absolutionlabs.com` with your UUID and we will delete all rows tagged with that UUID within one business day. The DSAR audit log (§6) will record the deletion.
- **Object** to processing. Same mechanism as erasure.
- **Restrict** processing. Same mechanism.
- **Lodge a complaint** with the UK Information Commissioner's Office (`ico.org.uk`) if you believe we have mishandled your data.

If you lose your UUID, we cannot identify your rows after the fact — they are by design unlinkable to any other identifier. In that case the right to erasure cannot be exercised against your specific data, but it also cannot be exercised against anyone else's, because we cannot tell whose is whose. This is the privacy / DSAR trade-off of true anonymisation; we have chosen anonymisation.

## 9. Sharing with third parties

We do not share this data with any third party other than our infrastructure provider (Supabase, as processor — see §5) and their underlying cloud provider (AWS, as sub-processor). We do not sell, license, or trade it. There are no advertising partners.

## 10. Security

The endpoint:

- accepts only HTTPS
- enforces a server-side payload schema via Postgres CHECK constraints on every column; non-conforming payloads are rejected with HTTP 400
- rate-limits to 5 inserts per 60 seconds per install UUID (Postgres trigger)
- restricts the public anon key to INSERT-only on the `install_events` table via Row Level Security; anon cannot SELECT, UPDATE, or DELETE anything
- stores no IP addresses
- stores no secrets in the data path (the Supabase service-role key, used only for DSAR + retention prune, lives in 1Password)

The full security & privacy threat model is documented in the skill's `brief.md` (Threat & Recovery Map, six surfaces).

## 11. Children

The skill is a business / operations tool. We do not knowingly process data from anyone under 16. If we discover such data, we will delete it.

## 12. Changes to this policy

If we change this policy in any material way (changing what we collect, where it is stored, how long we keep it, who we share it with), we will:

- update the "Effective date" at the top
- update the published version at `absolutionlabs.com/privacy` with a clearly-marked change-log
- not retroactively apply the change to data collected under the previous version

You do not need to do anything in response to such changes. The skill's behaviour does not change retroactively — only future installs are governed by the updated policy.

## 13. Contact

For all privacy matters relating to this policy:

- **Email:** `privacy@absolutionlabs.com`
- **Subject line for deletion requests:** "DSAR — Obsidian Company Memory — [UUID]"
- **Response time:** one business day

For general support of the skill itself: `info@absolutionlabs.com`.

For all other Absolution Labs LTD matters: `hello@absolutionlabs.com` and the main privacy policy at `absolutionlabs.com/privacy-policy`.

---

## Internal notes (remove before publishing)

- This text covers ONLY the install-telemetry use case. If absolutionlabs.com has an existing privacy policy covering the website / sales / Hermes / client work, this should be merged in as a clearly-titled section, NOT replace it.
- Required pre-publication checks:
  - [ ] UK GDPR lawyer review (legitimate-interests assessment + DSAR mechanism + retention period)
  - [ ] Company-number + registered-address fields filled in
  - [ ] Effective date set
  - [ ] ICO registration confirmed (Absolution Labs LTD should be on the data-protection-fee register)
  - [ ] DPA with Supabase verified (signed copy in 1P or equivalent)
  - [ ] `privacy@absolutionlabs.com` mailbox provisioned + monitored
  - [ ] One-paragraph summary of this policy linked from the install landing page
  - [ ] Cross-reference from main privacy policy ("for the Obsidian Company Memory skill specifically, see [link]")
- This document is the canonical version. The published page at `absolutionlabs.com/privacy` should be regenerated from this file, not edited in-place — drift between the two would be a Threat-Map #2 finding.

*Drafted 2026-06-02 as Chunk 5b deliverable.*

---

## Use at your own risk

This privacy policy covers the install-telemetry surface only. For the full set of disclaimers covering the bundle (use at own risk, educational purpose only, AI-output verification responsibility, limitation of liability with £100 floor, UK statutory carve-outs, indemnity for forks, governing law and jurisdiction, formal-notice address), **read [DISCLAIMERS.md](../DISCLAIMERS.md) in full before installing, forking, or relying on anything in this repository.**

*© 2026 Absolution Labs. AbsolutionLabs Ltd, registered in England and Wales (Company No. 17091663). Registered office: 15 Westbury Road, London SE20 7QL.*
