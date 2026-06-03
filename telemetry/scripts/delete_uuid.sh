#!/usr/bin/env bash
# DSAR helper — delete all install_events rows for one UUID and log the request.
#
# Usage:
#   ./scripts/delete_uuid.sh <uuid> [operator-note]
#
# Example:
#   ./scripts/delete_uuid.sh 7c2e3a14-9b8d-4f12-bc55-2e0c41d8a9b3 "DSAR via privacy@ inbox 2026-07-15"
#
# Pre-flight (the operator's discipline, not enforced by code):
#   - Confirm the requester's email + UUID match a real DSAR request in
#     the privacy@absolutionlabs.com inbox. Forwarded screenshots from
#     unknown senders are not sufficient; require reply-from-original-sender
#     confirmation.
#
# Mechanism:
#   - Reads the Supabase service-role key from 1Password (op://).
#   - Calls the dsar_delete_uuid() Postgres function via PostgREST.
#   - The function is SECURITY DEFINER and atomically:
#       * DELETEs all install_events rows matching the UUID
#       * INSERTs a row in dsar_log with the UUID + timestamp + operator note
#     in a single transaction — rollback-safe.
#   - Service-role key never touches disk; held in an environment variable
#     for the duration of this script only.

set -euo pipefail

# Clear the service-role key on any exit path (including Ctrl-C, SIGTERM).
# Without this trap, the key could remain in the parent shell's environment
# while the curl runs, visible via /proc/<pid>/environ on Linux during the
# brief window. Defence-in-depth per OP #18 (never persist secrets).
SVC_KEY=""
trap 'SVC_KEY=""; unset SVC_KEY' EXIT INT TERM

PROJECT_REF="vujwcvqiwwpncnhgxjsu"
PROJECT_URL="https://${PROJECT_REF}.supabase.co"
OP_REF="op://API Keys/Supabase - Obsidian Telemetry - service role/credential"

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <uuid> [operator-note]" >&2
  exit 64
fi

UUID="$1"
NOTE="${2:-no note}"

# Validate UUID v4 shape (case-insensitive)
if ! [[ "$UUID" =~ ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$ ]]; then
  echo "error: not a valid UUID: $UUID" >&2
  exit 65
fi

UUID_LC="$(printf '%s' "$UUID" | tr '[:upper:]' '[:lower:]')"
REQUESTED_AT="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"

# Confirmation prompt — destructive, defence-in-depth
echo "About to delete all install_events rows for UUID: $UUID_LC"
echo "DSAR log will be appended with note: $NOTE"
read -rp "Proceed? (type 'yes' to confirm) " CONFIRM
if [[ "$CONFIRM" != "yes" ]]; then
  echo "aborted." >&2
  exit 1
fi

# Fetch service-role key from 1P — runtime only, never persisted
SVC_KEY="$(op read "$OP_REF")"
if [[ -z "$SVC_KEY" || ${#SVC_KEY} -lt 100 ]]; then
  echo "error: failed to read service-role key from 1Password" >&2
  exit 70
fi

# Call the dsar_delete_uuid() function via PostgREST RPC
RESPONSE="$(
  curl -sS -X POST \
    "$PROJECT_URL/rest/v1/rpc/dsar_delete_uuid" \
    -H "apikey: $SVC_KEY" \
    -H "Authorization: Bearer $SVC_KEY" \
    -H "Content-Type: application/json" \
    -d "$(printf '{"target_uuid":"%s","requested_at":"%s","operator_note":%s}' \
            "$UUID_LC" \
            "$REQUESTED_AT" \
            "$(printf '%s' "$NOTE" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')")"
)"

echo "Response: $RESPONSE"

# The function returns an integer (rows_deleted)
if [[ "$RESPONSE" =~ ^[0-9]+$ ]]; then
  echo "rows deleted: $RESPONSE"
  echo ""
  echo "Reply to the DSAR requester confirming deletion. Suggested text:"
  echo
  echo "  Your install telemetry record for UUID $UUID_LC has been deleted from"
  echo "  our system as of $REQUESTED_AT. No further data tied to that UUID"
  echo "  exists in our database. The deletion is logged in our DSAR audit"
  echo "  table (UUID + timestamp only) per UK GDPR Article 30 record-keeping"
  echo "  requirements; no other personal data was retained."
else
  echo "error: unexpected response from dsar_delete_uuid (expected integer)" >&2
  exit 71
fi
